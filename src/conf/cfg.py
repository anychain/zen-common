import argparse
import collections
import copy
import errno
import functools
import glob
import itertools
import logging
import os
import string
import sys

from conf import yamlparser


LOG = logging.getLogger(__name__)


class Error(Exception):
    """Base class for cfg exceptions."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class NotInitializedError(Error):
    """Raised if parser is not initialized yet."""

    def __str__(self):
        return "call expression on parser has not been invoked"

def _get_config_file(project):
    """Return zen configuration file locations
    """
    return '/etc/zen/zen.conf'

class ParseError(yamlparser.ParseError):
    def __init__(self, msg, lineno, line, filename):
        super(ParseError, self).__init__(msg, lineno, line)
        self.filename = filename

    def __str__(self):
        return 'at %s:%d, %s: %r' % (self.filename, self.lineno,
                                     self.msg, self.line)


class ConfigParser(yamlparser.BaseParser):
    def __init__(self, filename, sections):
        super(ConfigParser, self).__init__()
        self.filename = filename
        self.sections = sections
        self._normalized = None
        self.section = None

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
        except yamlparser.ParseError as pe:
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

    def __init__(self):
        """Construct a ConfigOpts object."""
        self._opts = {}  # dict of dicts of (opt:, override:, default:)
        self._groups = {}

        self._args = None

        self._oparser = None
        self._namespace = None
        self.__cache = {}
        self._config_opts = []
        self._cli_opts = collections.deque()
        self._validate_default_values = False

    def _pre_setup(self, project, prog, version, usage, default_config_files):
        """Initialize a ConfigCliParser object for option parsing."""

        if prog is None:
            prog = os.path.basename(sys.argv[0])

        if default_config_files is None:
            default_config_files = find_config_files(project, prog)

        self._oparser = _CachedArgumentParser(prog=prog, usage=usage)
        self._oparser.add_parser_argument(self._oparser,
                                          '--version',
                                          action='version',
                                          version=version)

        return prog, default_config_files

    def _setup(self, project, prog, version, usage, default_config_files):
        """Initialize a ConfigOpts object for option parsing."""

        self._config_opts = [
            _ConfigFileOpt('config-file',
                           default=default_config_files,
                           metavar='PATH',
                           help=('Path to a config file to use. Multiple '
                                 'config files can be specified, with values '
                                 'in later files taking precedence. The '
                                 'default files used are: %(default)s.')),
            _ConfigDirOpt('config-dir',
                          metavar='DIR',
                          help='Path to a config directory to pull *.conf '
                               'files from. This file set is sorted, so as to '
                               'provide a predictable parse order if '
                               'individual options are over-ridden. The set '
                               'is parsed after the file(s) specified via '
                               'previous --config-file, arguments hence '
                               'over-ridden options in the directory take '
                               'precedence.'),
        ]
        self.register_cli_opts(self._config_opts)

        self.project = project
        self.prog = prog
        self.version = version
        self.usage = usage
        self.default_config_files = default_config_files

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
                 args=None,
                 project=None,
                 prog=None,
                 version=None,
                 usage=None,
                 default_config_files=None,
                 validate_default_values=False):
        """Parse command line arguments and config files.

        Calling a ConfigOpts object causes the supplied command line arguments
        and config files to be parsed, causing opt values to be made available
        as attributes of the object.

        The object may be called multiple times, each time causing the previous
        set of values to be overwritten.

        Automatically registers the --config-file option with either a supplied
        list of default config files, or a list from find_config_files().

        If the --config-dir option is set, any *.conf files from this
        directory are pulled in, after all the file(s) specified by the
        --config-file option.

        :param args: command line arguments (defaults to sys.argv[1:])
        :param project: the toplevel project name, used to locate config files
        :param prog: the name of the program (defaults to sys.argv[0] basename)
        :param version: the program version (for --version)
        :param usage: a usage string (%prog will be expanded)
        :param default_config_files: config files to use by default
        :param validate_default_values: whether to validate the default values
        :returns: the list of arguments left over after parsing options
        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        self.clear()

        self._validate_default_values = validate_default_values

        prog, default_config_files = self._pre_setup(project,
                                                     prog,
                                                     version,
                                                     usage,
                                                     default_config_files)

        self._setup(project, prog, version, usage, default_config_files)

        self._namespace = self._parse_cli_opts(args if args is not None
                                               else sys.argv[1:])
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
        :raises: NoSuchOptError
        """
        try:
            return self._get(name)
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
        self._unset_defaults_and_overrides()
        self.clear()

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

    def _parse_config_files(self):
        """Parse configure files options.

        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        namespace = _Namespace(self)
        for arg in self._args:
            if arg == '--config-file' or arg.startswith('--config-file='):
                break
        else:
            for config_file in self.default_config_files:
                ConfigParser._parse_file(config_file, namespace)

        self._oparser.parse_args(self._args, namespace)

        self._validate_cli_options(namespace)

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

CONF = ConfigOpts()
