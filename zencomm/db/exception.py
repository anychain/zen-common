"""DB related custom exceptions.

"""

import six


class DBError(Exception):

    """Base exception for all custom database exceptions.

    :kwarg inner_exception: an original exception which was wrapped with
        DBError or its subclasses.
    """

    def __init__(self, inner_exception=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(six.text_type(inner_exception))


class DBDuplicateEntry(DBError):
    """Duplicate entry at unique column error.

    Raised when made an attempt to write to a unique column the same entry as
    existing one. :attr: `columns` available on an instance of the exception
    and could be used at error handling::

       try:
           instance_type_ref.save()
       except DBDuplicateEntry as e:
           if 'colname' in e.columns:
               # Handle error.

    :kwarg columns: a list of unique columns have been attempted to write a
        duplicate entry.
    :type columns: list
    :kwarg value: a value which has been attempted to write. The value will
        be None, if we can't extract it for a particular database backend. Only
        MySQL and PostgreSQL 9.x are supported right now.
    """
    def __init__(self, columns=None, inner_exception=None, value=None):
        self.columns = columns or []
        self.value = value
        super(DBDuplicateEntry, self).__init__(inner_exception)


class DBConstraintError(DBError):
    """Check constraint fails for column error.

    Raised when made an attempt to write to a column a value that does not
    satisfy a CHECK constraint.

    :kwarg table: the table name for which the check fails
    :type table: str
    :kwarg check_name: the table of the check that failed to be satisfied
    :type check_name: str
    """
    def __init__(self, table, check_name, inner_exception=None):
        self.table = table
        self.check_name = check_name
        super(DBConstraintError, self).__init__(inner_exception)


class DBReferenceError(DBError):
    """Foreign key violation error.

    :param table: a table name in which the reference is directed.
    :type table: str
    :param constraint: a problematic constraint name.
    :type constraint: str
    :param key: a broken reference key name.
    :type key: str
    :param key_table: a table name which contains the key.
    :type key_table: str
    """

    def __init__(self, table, constraint, key, key_table,
                 inner_exception=None):
        self.table = table
        self.constraint = constraint
        self.key = key
        self.key_table = key_table
        super(DBReferenceError, self).__init__(inner_exception)


class DBDeadlock(DBError):

    """Database dead lock error.

    Deadlock is a situation that occurs when two or more different database
    sessions have some data locked, and each database session requests a lock
    on the data that another, different, session has already locked.
    """

    def __init__(self, inner_exception=None):
        super(DBDeadlock, self).__init__(inner_exception)


class DBInvalidUnicodeParameter(Exception):

    """Database unicode error.

    Raised when unicode parameter is passed to a database
    without encoding directive.
    """

    message = ("Invalid Parameter: "
               "Encoding directive wasn't provided.")


class DbMigrationError(DBError):

    """Wrapped migration specific exception.

    Raised when migrations couldn't be completed successfully.
    """

    def __init__(self, message=None):
        super(DbMigrationError, self).__init__(message)


class DBConnectionError(DBError):

    """Wrapped connection specific exception.

    Raised when database connection is failed.
    """

    pass


class DBDataError(DBError):
    """Raised for errors that are due to problems with the processed data.

    E.g. division by zero, numeric value out of range, incorrect data type, etc

    """


class InvalidSortKey(Exception):
    """A sort key destined for database query usage is invalid."""

    message = "Sort key supplied was not valid."


class ColumnError(Exception):
    """Error raised when no column or an invalid column is found."""


class BackendNotAvailable(Exception):
    """Error raised when a particular database backend is not available

    within a test suite.

    """


class RetryRequest(Exception):
    """Error raised when DB operation needs to be retried.

    That could be intentionally raised by the code without any real DB errors.
    """
    def __init__(self, inner_exc):
        self.inner_exc = inner_exc


class NoEngineContextEstablished(AttributeError):
    """Error raised for non-present enginefacade attribute access.


    This applies to the ``session`` and ``connection`` attributes
    of a user-defined context and/or RequestContext object, when they
    are accessed outside of the scope of an enginefacade decorator
    or context manager.

    The exception is a subclass of AttributeError so that
    normal Python missing attribute behaviors are maintained, such
    as support for ``getattr(context, 'session', None)``.


    """

class InvalidInput(DBError):
    message = "Invalid input for db operation: %(error_message)s."
