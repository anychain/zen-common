"""
=================================
Multiple DB API backend support.
=================================

A DB backend module should implement a method named 'get_backend' which
takes no arguments. The method can return any object that implements DB
API methods.
"""

import logging
import threading
import time

from zencomm.utils import excutils
from zencomm.utils import importutils
import six

from zencomm.db import exception


LOG = logging.getLogger(__name__)


def safe_for_db_retry(f):
    """Indicate api method as safe for re-connection to database.

    Database connection retries will be enabled for the decorated api method.
    Database connection failure can have many causes, which can be temporary.
    In such cases retry may increase the likelihood of connection.

    Usage::

        @safe_for_db_retry
        def api_method(self):
            self.engine.connect()


    :param f: database api method.
    :type f: function.
    """
    f.__dict__['enable_retry_on_disconnect'] = True
    return f


def retry_on_deadlock(f):
    """Retry a DB API call if Deadlock was received.

    wrap_db_entry will be applied to all db.api functions marked with this
    decorator.
    """
    f.__dict__['enable_retry_on_deadlock'] = True
    return f


def retry_on_request(f):
    """Retry a DB API call if RetryRequest exception was received.

    wrap_db_entry will be applied to all db.api functions marked with this
    decorator.
    """
    f.__dict__['enable_retry_on_request'] = True
    return f


class wrap_db_retry(object):
    """Retry db.api methods, if db_error raised

    Retry decorated db.api methods. This decorator catches db_error and retries
    function in a loop until it succeeds, or until maximum retries count
    will be reached.

    Keyword arguments:

    :param retry_interval: seconds between transaction retries
    :type retry_interval: int

    :param max_retries: max number of retries before an error is raised
    :type max_retries: int

    :param inc_retry_interval: determine increase retry interval or not
    :type inc_retry_interval: bool

    :param max_retry_interval: max interval value between retries
    :type max_retry_interval: int

    :param exception_checker: checks if an exception should trigger a retry
    :type exception_checker: callable
    """

    def __init__(self, retry_interval=0, max_retries=0, inc_retry_interval=0,
                 max_retry_interval=0, retry_on_disconnect=False,
                 retry_on_deadlock=False, retry_on_request=False,
                 exception_checker=lambda exc: False):
        super(wrap_db_retry, self).__init__()

        self.db_error = ()
        # default is that we re-raise anything unexpected
        self.exception_checker = exception_checker
        if retry_on_disconnect:
            self.db_error += (exception.DBConnectionError, )
        if retry_on_deadlock:
            self.db_error += (exception.DBDeadlock, )
        if retry_on_request:
            self.db_error += (exception.RetryRequest, )
        self.retry_interval = retry_interval
        self.max_retries = max_retries
        self.inc_retry_interval = inc_retry_interval
        self.max_retry_interval = max_retry_interval

    def __call__(self, f):
        @six.wraps(f)
        def wrapper(*args, **kwargs):
            next_interval = self.retry_interval
            remaining = self.max_retries

            while True:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    with excutils.save_and_reraise_exception() as ectxt:
                        if remaining > 0:
                            ectxt.reraise = not self._is_exception_expected(e)
                        else:
                            LOG.exception('DB exceeded retry limit.')
                            # if it's a RetryRequest, we need to unpack it
                            if isinstance(e, exception.RetryRequest):
                                ectxt.type_ = type(e.inner_exc)
                                ectxt.value = e.inner_exc
                    # NOTE(vsergeyev): We are using patched time module, so
                    #                  this effectively yields the execution
                    #                  context to another green thread.
                    time.sleep(next_interval)
                    if self.inc_retry_interval:
                        next_interval = min(
                            next_interval * 2,
                            self.max_retry_interval
                        )
                    remaining -= 1

        return wrapper

    def _is_exception_expected(self, exc):
        if isinstance(exc, self.db_error):
            # RetryRequest is application-initated exception
            # and not an error condition in case retries are
            # not exceeded
            if not isinstance(exc, exception.RetryRequest):
                LOG.exception('DB error.')
            return True
        return self.exception_checker(exc)


class DBAPI(object):
    """Initialize the chosen DB API backend.

    After initialization API methods is available as normal attributes of
    ``DBAPI`` subclass. Database API methods are supposed to be called as
    DBAPI instance methods.

    :param backend_name: name of the backend to load
    :type backend_name: str

    :param backend_mapping: backend name -> module/class to load mapping
    :type backend_mapping: dict
    :default backend_mapping: None

    :param lazy: load the DB backend lazily on the first DB API method call
    :type lazy: bool
    :default lazy: False

    :keyword use_db_reconnect: retry DB transactions on disconnect or not
    :type use_db_reconnect: bool

    :keyword retry_interval: seconds between transaction retries
    :type retry_interval: int

    :keyword inc_retry_interval: increase retry interval or not
    :type inc_retry_interval: bool

    :keyword max_retry_interval: max interval value between retries
    :type max_retry_interval: int

    :keyword max_retries: max number of retries before an error is raised
    :type max_retries: int
    """

    def __init__(self, backend_name, backend_mapping=None, lazy=False,
                 **kwargs):

        self._backend = None
        self._backend_name = backend_name
        self._backend_mapping = backend_mapping or {}
        self._lock = threading.Lock()

        if not lazy:
            self._load_backend()

        self.use_db_reconnect = kwargs.get('use_db_reconnect', False)
        self.retry_interval = kwargs.get('retry_interval', 1)
        self.inc_retry_interval = kwargs.get('inc_retry_interval', True)
        self.max_retry_interval = kwargs.get('max_retry_interval', 10)
        self.max_retries = kwargs.get('max_retries', 20)

    def _load_backend(self):
        with self._lock:
            if not self._backend:
                # Import the untranslated name if we don't have a mapping
                backend_path = self._backend_mapping.get(self._backend_name,
                                                         self._backend_name)
                LOG.debug('Loading backend %(name)r from %(path)r',
                          {'name': self._backend_name,
                           'path': backend_path})
                backend_mod = importutils.import_module(backend_path)
                self._backend = backend_mod.get_backend()

    def __getattr__(self, key):
        if not self._backend:
            self._load_backend()

        attr = getattr(self._backend, key)
        if not hasattr(attr, '__call__'):
            return attr
        # NOTE(vsergeyev): If `use_db_reconnect` option is set to True, retry
        #                  DB API methods, decorated with @safe_for_db_retry
        #                  on disconnect.
        retry_on_disconnect = self.use_db_reconnect and attr.__dict__.get(
            'enable_retry_on_disconnect', False)
        retry_on_deadlock = attr.__dict__.get('enable_retry_on_deadlock',
                                              False)
        retry_on_request = attr.__dict__.get('enable_retry_on_request', False)

        if retry_on_disconnect or retry_on_deadlock or retry_on_request:
            attr = wrap_db_retry(
                retry_interval=self.retry_interval,
                max_retries=self.max_retries,
                inc_retry_interval=self.inc_retry_interval,
                max_retry_interval=self.max_retry_interval,
                retry_on_disconnect=retry_on_disconnect,
                retry_on_deadlock=retry_on_deadlock,
                retry_on_request=retry_on_request)(attr)

        return attr

    @classmethod
    def from_config(cls, conf, backend_mapping=None, lazy=False):
        """Initialize DBAPI instance given a config instance.

        :param conf: oslo.config config instance
        :type conf: oslo.config.cfg.ConfigOpts

        :param backend_mapping: backend name -> module/class to load mapping
        :type backend_mapping: dict

        :param lazy: load the DB backend lazily on the first DB API method call
        :type lazy: bool

        """
        '''
        conf.register_opts(options.database_opts, 'database')

        return cls(backend_name=conf.database.backend,
                   backend_mapping=backend_mapping,
                   lazy=lazy,
                   use_db_reconnect=conf.database.use_db_reconnect,
                   retry_interval=conf.database.db_retry_interval,
                   inc_retry_interval=conf.database.db_inc_retry_interval,
                   max_retry_interval=conf.database.db_max_retry_interval,
                   max_retries=conf.database.db_max_retries)
        '''

        return cls(backend_name=conf.database.backend,
                   backend_mapping=backend_mapping,
                   lazy=lazy,
                   use_db_reconnect=False,
                   retry_interval=1,
                   inc_retry_interval=True,
                   max_retry_interval=10,
                   max_retries=20)


def _get_regexp_op_for_connection(dbtype):
    #db_string = db_connection.split(':')[0].split('+')[0]
    regexp_op_map = {
        'postgresql': '~',
        'mysql': 'REGEXP',
        'sqlite': 'REGEXP'
    }
    return regexp_op_map.get(dbtype, 'LIKE')


def _exact_query_filter(model, query, filters, legal_keys):
    """Applies exact match filtering to an model query.

    Returns the updated query.  Modifies filters argument to remove
    filters consumed.

    :param query: query to apply filters to
    :param filters: dictionary of filters; values that are lists,
                    tuples, sets, or frozensets cause an 'IN' test to
                    be performed, while exact matching ('==' operator)
                    is used for other values
    :param legal_keys: list of keys to apply exact filtering to
    """

    filter_dict = {}

    # Walk through all the keys
    for key in legal_keys:
        # Skip ones we're not filtering on
        if key not in filters:
            continue

        # OK, filtering on this key; what value do we search for?
        value = filters.pop(key)

        if isinstance(value, (list, tuple, set, frozenset)):
            # Looking for values in a list; apply to query directly
            column_attr = getattr(model, key)
            query = query.filter(column_attr.in_(value))
        else:
            # OK, simple exact match; save for later
            filter_dict[key] = value

    # Apply simple exact matches
    if filter_dict:
        query = query.filter_by(**filter_dict)

    return query


def _regex_query_filter(model, query, filters):
    """Applies regular expression filtering to an model query.

    Returns the updated query.

    :param query: query to apply filters to
    :param filters: dictionary of filters with regex values
    """

    #db_regexp_op = _get_regexp_op_for_connection(CONF.database.connection)
    db_regexp_op = _get_regexp_op_for_connection('postgresql')
    for filter_name in filters:
        try:
            column_attr = getattr(model, filter_name)
        except AttributeError:
            continue
        if db_regexp_op == 'LIKE':
            query = query.filter(column_attr.op(db_regexp_op)(
                                 '%' + str(filters[filter_name]) + '%'))
        else:
            query = query.filter(column_attr.op(db_regexp_op)(
                                 str(filters[filter_name])))
    return query


def process_sort_params(sort_keys, sort_dirs,
                        default_keys=['created_at', 'id'],
                        default_dir='asc'):
    """Process the sort parameters to include default keys.

    Creates a list of sort keys and a list of sort directions. Adds the default
    keys to the end of the list if they are not already included.

    When adding the default keys to the sort keys list, the associated
    direction is:
    1) The first element in the 'sort_dirs' list (if specified), else
    2) 'default_dir' value (Note that 'asc' is the default value since this is
    the default in sqlalchemy.utils.paginate_query)

    :param sort_keys: List of sort keys to include in the processed list
    :param sort_dirs: List of sort directions to include in the processed list
    :param default_keys: List of sort keys that need to be included in the
                         processed list, they are added at the end of the list
                         if not already specified.
    :param default_dir: Sort direction associated with each of the default
                        keys that are not supplied, used when they are added
                        to the processed list
    :returns: list of sort keys, list of sort directions
    :raise exception.InvalidInput: If more sort directions than sort keys
                                   are specified or if an invalid sort
                                   direction is specified
    """
    # Determine direction to use for when adding default keys
    if sort_dirs and len(sort_dirs) != 0:
        default_dir_value = sort_dirs[0]
    else:
        default_dir_value = default_dir

    # Create list of keys (do not modify the input list)
    if sort_keys:
        result_keys = list(sort_keys)
    else:
        result_keys = []

    # If a list of directions is not provided, use the default sort direction
    # for all provided keys
    if sort_dirs:
        result_dirs = []
        # Verify sort direction
        for sort_dir in sort_dirs:
            if sort_dir not in ('asc', 'desc'):
                msg = "Unknown sort direction, must be 'desc' or 'asc'"
                raise exception.InvalidInput(error_message=msg)
            result_dirs.append(sort_dir)
    else:
        result_dirs = [default_dir_value for _sort_key in result_keys]

    # Ensure that the key and direction length match
    while len(result_dirs) < len(result_keys):
        result_dirs.append(default_dir_value)
    # Unless more direction are specified, which is an error
    if len(result_dirs) > len(result_keys):
        msg = "Sort direction size exceeds sort key size"
        raise exception.InvalidInput(error_message=msg)

    # Ensure defaults are included
    for key in default_keys:
        if key not in result_keys:
            result_keys.append(key)
            result_dirs.append(default_dir_value)

    return result_keys, result_dirs
