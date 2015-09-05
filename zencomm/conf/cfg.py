# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#

import collections
import copy
import errno
import functools
import itertools
import logging
import os
from zencomm.conf.exception import *
from zencomm.conf import types

LOG = logging.getLogger(__name__)


def _fixpath(p):
    """Apply tilde expansion and absolutization to a path."""
    return os.path.abspath(os.path.expanduser(p))


def _is_opt_registered(opts, opt):
    """Check whether an opt with the same name is already registered.

    The same opt may be registered multiple times, with only the first
    registration having any effect. However, it is an error to attempt
    to register a different opt with the same name.

    :param opts: the set of opts already registered
    :param opt: the opt to be registered
    :returns: True if the opt was previously registered, False otherwise
    :raises: DuplicateOptError if a naming conflict is detected
    """
    if opt.dest in opts:
        if opts[opt.dest]['opt'] != opt:
            raise DuplicateOptError(opt.name)
        return True
    else:
        return False


def set_defaults(opts, **kwargs):
    for opt in opts:
        if opt.dest in kwargs:
            opt.default = kwargs[opt.dest]


def _normalize_group_name(group_name):
    if group_name == 'DEFAULT':
        return group_name
    return group_name.lower()


class Opt(object):

    """Base class for all configuration options.

    The only required parameter is the option's name. However, it is
    common to also supply a default and help string for all options.

    :param name: the option's name
    :param type: the option's type. Must be a callable object that takes string
                 and returns converted and validated value
    :param dest: the name of the corresponding ConfigOpts property
    :param short: a single character CLI option name
    :param default: the default value of the option
    :param help: an explanation of how the option is used
    :param secret: true if the value should be obfuscated in log output
    :param required: true if a value must be supplied for this option
    :param sample_default: a default string for sample config files

    An Opt object has no public methods, but has a number of public properties:

    .. py:attribute:: name

        the name of the option, which may include hyphens

    .. py:attribute:: type

        a callable object that takes string and returns converted and
        validated value.  Default types are available from
        :class:`oslo_config.types`

    .. py:attribute:: dest

        the (hyphen-less) ConfigOpts property which contains the option value

    .. py:attribute:: short

        a single character CLI option name

    .. py:attribute:: default

        the default value of the option

    .. py:attribute:: help

        a string explaining how the option's value is used
    """

    multi = False

    def __init__(self, name, type=None, dest=None, short=None,
                 default=None, help=None,
                 secret=False, required=False):
        if name.startswith('_'):
            raise ValueError('illegal name %s with prefix _' % (name,))
        self.name = name

        if type is None:
            type = types.String()

        if not callable(type):
            raise TypeError('type must be callable')
        self.type = type

        if dest is None:
            self.dest = self.name.replace('-', '_')
        else:
            self.dest = dest
        self.short = short
        self.default = default
        self.help = help
        self.secret = secret
        self.required = required

        self._assert_default_is_of_opt_type()

    def _assert_default_is_of_opt_type(self):
        if (self.default is not None
                and hasattr(self.type, 'is_base_type')
                and not self.type.is_base_type(self.default)):
            expected_types = ", ".join(
                [t.__name__ for t in self.type.BASE_TYPES])
            LOG.debug(('Expected default value of type(s) %(extypes)s but got '
                       '%(default)r of type %(deftypes)s'),
                      {'extypes': expected_types,
                       'default': self.default,
                       'deftypes': type(self.default).__name__})

    def __ne__(self, another):
        return vars(self) != vars(another)

    def __eq__(self, another):
        return vars(self) == vars(another)

    __hash__ = object.__hash__

    def _get_from_namespace(self, namespace, group_name):
        """Retrieves the option value from a _Namespace object.

        :param namespace: a _Namespace object
        :param group_name: a group name
        """
        names = [(group_name, self.dest)]
        current_name = (group_name, self.name)

        value = namespace._get_value(names, self.multi, current_name)

        return value

    def __lt__(self, another):
        return hash(self) < hash(another)


class StrOpt(Opt):
    """Option with String type

    Option with ``type`` :class:`oslo_config.types.String`

    `Kept for backward-compatibility with options not using Opt directly`.

    :param choices: Optional sequence of valid values.
    """

    def __init__(self, name, choices=None, **kwargs):
        super(StrOpt, self).__init__(name,
                                     type=types.String(choices=choices),
                                     **kwargs)


class BoolOpt(Opt):

    """Boolean options.
      In config files, boolean values are cast with Boolean type.
    """

    def __init__(self, name, **kwargs):
        super(BoolOpt, self).__init__(name, type=types.Boolean(), **kwargs)


class IntOpt(Opt):

    """Option with Integer type

    Option with ``type`` :class:`oslo_config.types.Integer`

    `Kept for backward-compatibility with options not using Opt directly`.
    """

    def __init__(self, name, min=None, max=None, **kwargs):
        super(IntOpt, self).__init__(name, type=types.Integer(min, max),
                                     **kwargs)


class FloatOpt(Opt):

    """Option with Float type

    Option with ``type`` :class:`oslo_config.types.Float`

    `Kept for backward-communicability with options not using Opt directly`.
    """

    def __init__(self, name, **kwargs):
        super(FloatOpt, self).__init__(name, type=types.Float(), **kwargs)


class ListOpt(Opt):

    """Option with List(String) type

    Option with ``type`` :class:`oslo_config.types.List`

    `Kept for backward-compatibility with options not using Opt directly`.
    """

    def __init__(self, name, **kwargs):
        super(ListOpt, self).__init__(name, type=types.List(), **kwargs)


class DictOpt(Opt):

    """Option with Dict(String) type

    Option with ``type`` :class:`oslo_config.types.Dict`

    `Kept for backward-compatibility with options not using Opt directly`.
    """

    def __init__(self, name, **kwargs):
        super(DictOpt, self).__init__(name, type=types.Dict(), **kwargs)


class IPOpt(Opt):

    """Opt with IPAddress type

    Option with ``type`` :class:`oslo_config.types.IPAddress`

    :param version: one of either ``4``, ``6``, or ``None`` to specify
       either version.
    """

    def __init__(self, name, version=None, **kwargs):
        super(IPOpt, self).__init__(name, type=types.IPAddress(version),
                                    **kwargs)


class MultiOpt(Opt):

    """Multi-value option.

    Multi opt values are typed opts which may be specified multiple times.
    The opt value is a list containing all the values specified.

    :param name: Name of the config option
    :param item_type: Type of items (see :class:`oslo_config.types`)

    For example::

       cfg.MultiOpt('foo',
                    item_type=types.Integer(),
                    default=None,
                    help="Multiple foo option")

    The command line ``--foo=1 --foo=2`` would result in ``cfg.CONF.foo``
    containing ``[1,2]``
    """
    multi = True

    def __init__(self, name, item_type, **kwargs):
        super(MultiOpt, self).__init__(name, item_type, **kwargs)


class MultiStrOpt(MultiOpt):

    """MultiOpt with a MultiString ``item_type``.

    MultiOpt with a default :class:`oslo_config.types.MultiString` item
    type.

    `Kept for backwards-compatibility for options that do not use
    MultiOpt directly`.

    """

    def __init__(self, name, **kwargs):
        super(MultiStrOpt, self).__init__(name,
                                          item_type=types.MultiString(),
                                          **kwargs)


class OptGroup(object):

    """Represents a group of opts.

    Each group corresponds to a section in config files.

    An OptGroup object has no public methods, but has a number of public string
    properties:

    .. py:attribute:: name

        the name of the group

    .. py:attribute:: title

        the group title as displayed in --help

    .. py:attribute:: help

        the group description as displayed in --help
    """

    def __init__(self, name, title=None, help=None):
        """Constructs an OptGroup object.

        :param name: the group name
        :param title: the group title for --help
        :param help: the group description for --help
        """
        self.name = name
        self.title = "%s options" % name if title is None else title
        self.help = help

        self._opts = {}  # dict of dicts of (opt:, override:, default:)

    def _register_opt(self, opt):
        """Add an opt to this group.

        :param opt: an Opt object
        :returns: False if previously registered, True otherwise
        :raises: DuplicateOptError if a naming conflict is detected
        """
        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.dest] = {'opt': opt}

        return True

    def _unregister_opt(self, opt):
        """Remove an opt from this group.

        :param opt: an Opt object
        """
        if opt.dest in self._opts:
            del self._opts[opt.dest]

    def _get_argparse_group(self, parser):
        if self._argparse_group is None:
            """Build an argparse._ArgumentGroup for this group."""
            self._argparse_group = parser.add_argument_group(self.title,
                                                             self.help)
        return self._argparse_group

    def _clear(self):
        """Clear this group's option parsing state."""
        self._argparse_group = None


class ConfigParser(iniparser.BaseParser):
    def __init__(self, filename, sections):
        super(ConfigParser, self).__init__()
        self.filename = filename
        self.sections = sections
        self._normalized = None
        self.section = None

    def _add_normalized(self, normalized):
        self._normalized = normalized

    def parse(self):
        with open(self.filename) as f:
            return super(ConfigParser, self).parse(f)

    def new_section(self, section):
        self.section = section
        self.sections.setdefault(self.section, {})

        if self._normalized is not None:
            self._normalized.setdefault(_normalize_group_name(self.section),
                                        {})

    def assignment(self, key, value):
        if not self.section:
            raise self.error_no_section()

        value = '\n'.join(value)

        def append(sections, section):
            sections[section].setdefault(key, [])
            sections[section][key].append(value)

        append(self.sections, self.section)
        if self._normalized is not None:
            append(self._normalized, _normalize_group_name(self.section))

    def parse_exc(self, msg, lineno, line=None):
        return ParseError(msg, lineno, line, self.filename)

    def error_no_section(self):
        return self.parse_exc('Section must be started before assignment',
                              self.lineno)

    @classmethod
    def _parse_file(cls, config_file, namespace):
        """Parse a config file and store any values in the namespace.

        :raises: ConfigFileParseError, ConfigFileValueError
        """
        config_file = _fixpath(config_file)

        sections = {}
        normalized = {}
        parser = cls(config_file, sections)
        parser._add_normalized(normalized)

        try:
            parser.parse()
        except iniparser.ParseError as pe:
            raise ConfigFileParseError(pe.filename, str(pe))
        except IOError as err:
            if err.errno == errno.ENOENT:
                namespace._file_not_found(config_file)
                return
            if err.errno == errno.EACCES:
                namespace._file_permission_denied(config_file)
                return
            raise

        namespace._add_parsed_config_file(sections, normalized)


class MultiConfigParser(object):
    '''
        parser for multiple files
    '''

    def __init__(self):
        self.parsed = []
        self._normalized = []
        self._emitted_deprecations = set()

    def read(self, config_files):
        read_ok = []

        for filename in config_files:
            sections = {}
            normalized = {}
            parser = ConfigParser(filename, sections)
            parser._add_normalized(normalized)

            try:
                parser.parse()
            except IOError:
                continue
            self._add_parsed_config_file(sections, normalized)
            read_ok.append(filename)

        return read_ok

    def _add_parsed_config_file(self, sections, normalized):
        """Add a parsed config file to the list of parsed files.

        :param sections: a mapping of section name to dicts of config values
        :param normalized: sections mapping with section names normalized
        :raises: ConfigFileValueError
        """
        self.parsed.insert(0, sections)
        self._normalized.insert(0, normalized)

    def get(self, names, multi=False):
        return self._get(names, multi=multi)

    def _get(self, names, multi=False, normalized=False, current_name=None):
        """Fetch a config file value from the parsed files.

        :param names: a list of (section, name) tuples
        :param multi: a boolean indicating whether to return multiple values
        :param normalized: whether to normalize group names to lowercase
        """
        rvalue = []

        def normalize(name):
            return _normalize_group_name(name) if normalized else name

        names = [(normalize(section), name) for section, name in names]

        for sections in (self._normalized if normalized else self.parsed):
            for section, name in names:
                if section not in sections:
                    continue
                if name in sections[section]:
                    current_name = current_name or names[0]
                    val = sections[section][name]
                    if multi:
                        rvalue = val + rvalue
                    else:
                        return val
        if multi and rvalue != []:
            return rvalue
        raise KeyError


class _Namespace():

    """An namespace which also stores config file values.
    """

    def __init__(self, conf):
        '''
            @param conf: ConfigOpts
        '''
        self._conf = conf
        self._parser = MultiConfigParser()
        self._files_not_found = []
        self._files_permission_denied = []

    def _add_parsed_config_file(self, sections, normalized):
        """Add a parsed config file to the list of parsed files.

        :param sections: a mapping of section name to dicts of config values
        :param normalized: sections mapping with section names normalized
        :raises: ConfigFileValueError
        """

        self._parser._add_parsed_config_file(sections, normalized)

    def _file_not_found(self, config_file):
        """Record that we were unable to open a config file.

        :param config_file: the path to the failed file
        """
        self._files_not_found.append(config_file)

    def _file_permission_denied(self, config_file):
        """Record that we have no permission to open a config file.

        :param config_file: the path to the failed file
        """
        self._files_permission_denied.append(config_file)

    def _get_value(self, names, multi, current_name):
        """Fetch a value from config files.

        Multiple names for a given configuration option may be supplied so
        that we can transparently handle files containing deprecated option
        names or groups.

        :param names: a list of (section, name) tuples
        :param multi: a boolean indicating whether to return multiple values
        """

        names = [(g if g is not None else 'DEFAULT', n) for g, n in names]
        values = self._parser._get(names, multi=multi, normalized=True,
                                   current_name=current_name)
        return values if multi else values[-1]


class ConfigOpts(collections.Mapping):

    """Config options which is set in configuration files.

    ConfigOpts is a configuration option manager with APIs for registering
    option schemas, grouping options, parsing option values and retrieving
    the values of options.
    """

    def __init__(self):
        """Construct a ConfigOpts object."""
        self._opts = {}  # dict of dicts of (opt:, default:)
        self._groups = {}
        self._namespace = None

        self.__cache = {}
        self._config_opts = []
        self._validate_default_values = False

    def __clear_cache(f):
        @functools.wraps(f)
        def __inner(self, *args, **kwargs):
            if kwargs.pop('clear_cache', True):
                result = f(self, *args, **kwargs)
                self.__cache.clear()
                return result
            else:
                return f(self, *args, **kwargs)

        return __inner

    def __call__(self,
                 default_config_files=['/opt/zen/conf/zen.conf'],
                 validate_default_values=False):
        """Parse config files.

        Calling a ConfigOpts object causes the config files to be parsed,
        causing opt values to be made available as attributes of the object.

        The object may be called multiple times, each time causing the previous
        set of values to be overwritten.

        Automatically registers the --config-file option with either a supplied
        list of default config files, or a list from find_config_files().

        If the --config-dir option is set, any *.conf files from this
        directory are pulled in, after all the file(s) specified by the
        --config-file option.

        :param default_config_files: config files to use by default
        :param validate_default_values: whether to validate the default values
        :returns: the list of arguments left over after parsing options
        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        self.clear()

        self._validate_default_values = validate_default_values
        self.default_config_files = default_config_files
        self._namespace = self._parse_config_files()

        if self._namespace._files_not_found:
            raise ConfigFilesNotFoundError(self._namespace._files_not_found)
        if self._namespace._files_permission_denied:
            raise ConfigFilesPermissionDeniedError(
                self._namespace._files_permission_denied)

        self._check_required_opts()

    def __getattr__(self, name):
        """Look up an option value and perform string substitution.

        :param name: the opt name (or 'dest', more precisely)
        :returns: the option value (after string substitution) or a GroupAttr
        :raises: ValueError or NoSuchOptError
        """
        try:
            return self._get(name)
        except ValueError:
            raise
        except Exception:
            raise NoSuchOptError(name)

    def __getitem__(self, key):
        """Look up an option value and perform string substitution."""
        return self.__getattr__(key)

    def __contains__(self, key):
        """Return True if key is the name of a registered opt or group."""
        return key in self._opts or key in self._groups

    def __iter__(self):
        """Iterate over all registered opt and group names."""
        for key in itertools.chain(self._opts.keys(), self._groups.keys()):
            yield key

    def __len__(self):
        """Return the number of options and option groups."""
        return len(self._opts) + len(self._groups)

    def reset(self):
        """Clear the object state and unset overrides and defaults."""
        self._unset_defaults()
        self.clear()

    @__clear_cache
    def clear(self):
        """Clear the state of the object to before it was called.

        Any subparsers added using the add_cli_subparsers() will also be
        removed as a side-effect of this method.
        """
        self._namespace = None
        self._validate_default_values = False
        self.unregister_opts(self._config_opts)
        for group in self._groups.values():
            group._clear()

    @__clear_cache
    def register_opt(self, opt, group=None):
        """Register an option schema.

        Registering an option schema makes any option value which is previously
        or subsequently parsed from the command line or config files available
        as an attribute of this object.

        :param opt: an instance of an Opt sub-class
        :param cli: whether this is a CLI option
        :param group: an optional OptGroup object or group name
        :return: False if the opt was already registered, True otherwise
        :raises: DuplicateOptError
        """
        if group is not None:
            group = self._get_group(group, autocreate=True)

            return group._register_opt(opt)

        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.dest] = {'opt': opt}

        return True

    @__clear_cache
    def register_opts(self, opts, group=None):
        """Register multiple option schemas at once."""
        for opt in opts:
            self.register_opt(opt, group, clear_cache=False)

    def register_group(self, group):
        """Register an option group.

        An option group must be registered before options can be registered
        with the group.

        :param group: an OptGroup object
        """
        if group.name in self._groups:
            return

        self._groups[group.name] = copy.copy(group)

    @__clear_cache
    def unregister_opt(self, opt, group=None):
        """Unregister an option.

        :param opt: an Opt object
        :param group: an optional OptGroup object or group name
        """

        if group is not None:
            self._get_group(group)._unregister_opt(opt)
        elif opt.dest in self._opts:
            del self._opts[opt.dest]

    @__clear_cache
    def unregister_opts(self, opts, group=None):
        """Unregister multiple CLI option schemas at once."""
        for opt in opts:
            self.unregister_opt(opt, group, clear_cache=False)

    @__clear_cache
    def set_default(self, name, default, group=None):
        """Override an opt's default value.

        Override the default value of given option. A command line or
        config file value will still take precedence over this default.

        :param name: the name/dest of the opt
        :param default: the default value
        :param group: an option OptGroup object or group name
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info['default'] = default

    @__clear_cache
    def clear_default(self, name, group=None):
        """Clear an override an opt's default value.

        Clear a previously set override of the default value of given option.

        :param name: the name/dest of the opt
        :param group: an option OptGroup object or group name
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info.pop('default', None)

    def _all_opt_infos(self):
        """A generator function for iteration opt infos."""
        for info in self._opts.values():
            yield info, None
        for group in self._groups.values():
            for info in group._opts.values():
                yield info, group

    def _unset_defaults(self):
        """Unset any default or override on all options."""
        for info, group in self._all_opt_infos():
            info.pop('default', None)

    def log_opt_values(self, logger, lvl):
        """Log the value of all registered opts.

        It's often useful for an app to log its configuration to a log file at
        startup for debugging. This method dumps to the entire config state to
        the supplied logger at a given log level.

        :param logger: a logging.Logger object
        :param lvl: the log level (for example logging.DEBUG) arg to
                    logger.log()
        """
        logger.log(lvl, "*" * 80)
        logger.log(lvl, "Configuration options gathered from:")
        logger.log(lvl, "command line args: %s", self._args)
        logger.log(lvl, "config files: %s", self.config_file)
        logger.log(lvl, "=" * 80)

        def _sanitize(opt, value):
            """Obfuscate values of options declared secret."""
            return value if not opt.secret else '*' * 4

        for opt_name in sorted(self._opts):
            opt = self._get_opt_info(opt_name)['opt']
            logger.log(lvl, "%-30s = %s", opt_name,
                       _sanitize(opt, getattr(self, opt_name)))

        for group_name in self._groups:
            group_attr = self.GroupAttr(self, self._get_group(group_name))
            for opt_name in sorted(self._groups[group_name]._opts):
                opt = self._get_opt_info(opt_name, group_name)['opt']
                logger.log(lvl, "%-30s = %s",
                           "%s.%s" % (group_name, opt_name),
                           _sanitize(opt, getattr(group_attr, opt_name)))

        logger.log(lvl, "*" * 80)

    def _get(self, name, group=None, namespace=None):
        if isinstance(group, OptGroup):
            key = (group.name, name)
        else:
            key = (group, name)
        try:
            if namespace is not None:
                raise KeyError

            return self.__cache[key]
        except KeyError:
            value = self._do_get(name, group, namespace)
            self.__cache[key] = value
            return value

    def _do_get(self, name, group=None, namespace=None):
        """Look up an option value.

        :param name: the opt name (or 'dest', more precisely)
        :param group: an OptGroup
        :param namespace: the namespace object that retrieves the option
                            value from
        :returns: the option value, or a GroupAttr object
        :raises: NoSuchOptError, NoSuchGroupError, ConfigFileValueError,
                 TemplateSubstitutionError
        """

        if group is None and name in self._groups:
            return self.GroupAttr(self, self._get_group(name))

        info = self._get_opt_info(name, group)
        opt = info['opt']

        if namespace is None:
            namespace = self._namespace

        def convert(value):
            return self._convert_value(value, opt)

        if namespace is not None:
            group_name = group.name if group else None

            try:
                return convert(opt._get_from_namespace(namespace, group_name))
            except KeyError:
                pass
            except ValueError as ve:
                raise ConfigFileValueError(
                    "Value for option %s is not valid: %s"
                    % (opt.name, str(ve)))

        if self._validate_default_values:
            if opt.default is not None:
                try:
                    convert(opt.default)
                except ValueError as e:
                    raise ConfigFileValueError(
                        "Default value for option %s is not valid: %s"
                        % (opt.name, str(e)))

        if opt.default is not None:
            return convert(opt.default)

        return None

    def _convert_value(self, value, opt):
        """Perform value type conversion.

        Converts values using option's type. Handles cases when value is
        actually a list of values (for example for multi opts).

        :param value: the string value, or list of string values
        :param opt: option definition (instance of Opt class or its subclasses)
        :returns: converted value
        """
        if opt.multi:
            return [opt.type(v) for v in value]
        else:
            return opt.type(value)

    def _get_group(self, group_or_name, autocreate=False):
        """Looks up a OptGroup object.

        Helper function to return an OptGroup given a parameter which can
        either be the group's name or an OptGroup object.

        The OptGroup object returned is from the internal dict of OptGroup
        objects, which will be a copy of any OptGroup object that users of
        the API have access to.

        If autocreate is True, the group will be created if it's not found. If
        group is an instance of OptGroup, that same instance will be
        registered, otherwise a new instance of OptGroup will be created.

        :param group_or_name: the group's name or the OptGroup object itself
        :param autocreate: whether to auto-create the group if it's not found
        :raises: NoSuchGroupError
        """
        group = group_or_name if isinstance(group_or_name, OptGroup) else None
        group_name = group.name if group else group_or_name

        if group_name not in self._groups:
            if not autocreate:
                raise NoSuchGroupError(group_name)

            self.register_group(group or OptGroup(name=group_name))

        return self._groups[group_name]

    def _get_opt_info(self, opt_name, group=None):
        """Return the (opt, override, default) dict for an opt.

        :param opt_name: an opt name/dest
        :param group: an optional group name or OptGroup object
        :raises: NoSuchOptError, NoSuchGroupError
        """
        if group is None:
            opts = self._opts
        else:
            group = self._get_group(group)
            opts = group._opts

        if opt_name not in opts:
            raise NoSuchOptError(opt_name, group)

        return opts[opt_name]

    def _check_required_opts(self, namespace=None):
        """Check that all opts marked as required have values specified.

        :param namespace: the namespace object be checked the required options
        :raises: RequiredOptError
        """
        for info, group in self._all_opt_infos():
            opt = info['opt']

            if opt.required:
                if 'default' in info:
                    continue

                if self._get(opt.dest, group, namespace) is None:
                    raise RequiredOptError(opt.name, group)

    def _parse_config_files(self):
        """Parse configure files options.

        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        namespace = _Namespace(self)

        for config_file in self.default_config_files:
            ConfigParser._parse_file(config_file, namespace)

        return namespace

    @__clear_cache
    def reload_config_files(self):
        """Reload configure files and parse all options

        :return False if reload configure files failed or else return True
        """
        try:
            namespace = self._parse_config_files()
            if namespace._files_not_found:
                raise ConfigFilesNotFoundError(namespace._files_not_found)
            if namespace._files_permission_denied:
                raise ConfigFilesPermissionDeniedError(
                    namespace._files_permission_denied)
            self._check_required_opts(namespace)

        except SystemExit as exc:
            LOG.warn("Caught SystemExit while reloading configure files "
                     "with exit code: %d", exc.code)
            return False
        except Error as err:
            LOG.warn("Caught Error while reloading configure files: %s",
                     err)
            return False
        else:
            self._namespace = namespace
            return True

    def list_all_sections(self):
        """List all sections from the configuration.

        Returns an iterator over all section names found in the
        configuration files, whether declared beforehand or not.
        """
        for sections in self._namespace._parser.parsed:
            for section in sections:
                yield section

    class GroupAttr(collections.Mapping):

        """Helper class.

        Represents the option values of a group as a mapping and attributes.
        """

        def __init__(self, conf, group):
            """Construct a GroupAttr object.

            :param conf: a ConfigOpts object
            :param group: an OptGroup object
            """
            self._conf = conf
            self._group = group

        def __getattr__(self, name):
            """Look up an option value and perform template substitution."""
            return self._conf._get(name, self._group)

        def __getitem__(self, key):
            """Look up an option value and perform string substitution."""
            return self.__getattr__(key)

        def __contains__(self, key):
            """Return True if key is the name of a registered opt or group."""
            return key in self._group._opts

        def __iter__(self):
            """Iterate over all registered opt and group names."""
            for key in self._group._opts.keys():
                yield key

        def __len__(self):
            """Return the number of options and option groups."""
            return len(self._group._opts)

CONF = ConfigOpts()
