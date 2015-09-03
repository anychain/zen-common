# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#

from zencomm.conf import types


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
    :param positional: True if the option is a positional CLI argument
    :param metavar: the option argument to show in --help
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

    .. py:attribute:: positional

        True if the option is a positional CLI argument

    .. py:attribute:: metavar

        the name shown as the argument to a CLI option in --help output

    .. py:attribute:: help

        a string explaining how the option's value is used
    """

    multi = False

    def __init__(self, name, type=None, dest=None, short=None,
                 default=None, positional=False, metavar=None, help=None,
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
        self.metavar = metavar
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

        value = namespace._get_value(names, self.multi, self.positional,
                                     current_name)
        # The previous line will raise a KeyError if no value is set in the
        # config file, so we'll only log deprecations for set options.
        if self.deprecated_for_removal and not self._logged_deprecation:
            self._logged_deprecation = True
            pretty_group = group_name or 'DEFAULT'
            LOG.warning('Option "%s" from group "%s" is deprecated for '
                        'removal.  Its value may be silently ignored in the '
                        'future.', self.dest, pretty_group)
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

