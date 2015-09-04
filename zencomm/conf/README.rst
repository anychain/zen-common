understanding of config module
------------------------------
* each option must be registered before it can be used
* relation ship between Opt and configuration files? 

   + namespace

      if there are configuration files available, configuration files will be
      read and loaded into MultiOpt as sections and normalized. Then namespace
      will be created and it will use MultiOpt to get sections or normalized

   + Opt

      After options are registered, program will use the register options to get
      option value, there is a map between opt and namespace, like when when access
      CONF.api.server_addr, finally it will be mapped to following config in
      configuration file:
         [api]
         server_addr = '192.168.22.1'

      If ther is no such config in configuration file, default value(set when
      registering options) will be used, else OptGroup.Opt will be mapped to 
      Section.Key in Namespace
      

zencomm.conf.cfg
----------------

Configuration options may be set in configuration files.

    from zencomm.conf import cfg
    from zencomm.conf import types

    PortType = types.Integer(1, 65535)

    common_opts = [
        cfg.StrOpt('bind_host',
                   default='0.0.0.0',
                   help='IP address to listen on.'),
        cfg.Opt('bind_port',
                type=PortType,
                default=9292,
                help='Port number to listen on.')
    ]

Option Types
------------

There are predefined types in :class:`zencomm.conf.cfg` :
strings, integers, floats, booleans, lists, 'multi strings'
and 'key/value pairs' (dictionary) ::

    enabled_apis_opt = cfg.ListOpt('enabled_apis',
                                   default=['ec2', 'osapi_compute'],
                                   help='List of APIs to enable by default.')

Registering Options
-------------------

Option schemas are registered with the config manager at runtime, but before
the option is referenced::

    class ExtensionManager(object):

        enabled_apis_opt = cfg.ListOpt(...)

        def __init__(self, conf):
            self.conf = conf
            self.conf.register_opt(enabled_apis_opt)
            ...

        def _load_extensions(self):
            for ext_factory in self.conf.osapi_compute_extension:
                ....

A common usage pattern is for each option schema to be defined in the module or
class which uses the option::

    opts = ...

    def add_common_opts(conf):
        conf.register_opts(opts)

    def get_bind_host(conf):
        return conf.bind_host

    def get_bind_port(conf):
        return conf.bind_port

Loading Config Files
--------------------

Option values are parsed from any supplied config files using
zencomm.conf.iniparser. If none are specified, a default set is used
for example glance-api.conf and glance-common.conf::

    glance-api.conf:
      [DEFAULT]
      bind_port = 9292

    glance-common.conf:
      [DEFAULT]
      bind_host = 0.0.0.0

Option values in config files and those on the command line are parsed
in order. The same option can appear many times in config files.
Later values always override earlier ones.

The order of configuration files inside the same configuration directory is
defined by the alphabetic sorting order of their file names.


Option Groups
-------------

Options can be registered as belonging to a group::

    rabbit_group = cfg.OptGroup(name='rabbit',
                                title='RabbitMQ options')

    rabbit_host_opt = cfg.StrOpt('host',
                                 default='localhost',
                                 help='IP/hostname to listen on.'),
    rabbit_port_opt = cfg.IntOpt('port',
                                 default=5672,
                                 help='Port number to listen on.')

    def register_rabbit_opts(conf):
        conf.register_group(rabbit_group)
        # options can be registered under a group in either of these ways:
        conf.register_opt(rabbit_host_opt, group=rabbit_group)
        conf.register_opt(rabbit_port_opt, group='rabbit')

If no group attributes are required other than the group name, the group
need not be explicitly registered for example::

    def register_rabbit_opts(conf):
        # The group will automatically be created, equivalent calling::
        #   conf.register_group(OptGroup(name='rabbit'))
        conf.register_opt(rabbit_port_opt, group='rabbit')

If no group is specified, options belong to the 'DEFAULT' section of config
files::

    glance-api.conf:
      [DEFAULT]
      bind_port = 9292
      ...

      [rabbit]
      host = localhost
      port = 5672
      use_ssl = False
      userid = guest
      password = guest
      virtual_host = /

Accessing Option Values In Your Code
------------------------------------

Option values in the default group are referenced as attributes/properties on
the config manager; groups are also attributes on the config manager, with
attributes for each of the options associated with the group::

    server.start(app, conf.bind_port, conf.bind_host, conf)

    self.connection = kombu.connection.BrokerConnection(
        hostname=conf.rabbit.host,
        port=conf.rabbit.port,
        ...)


Special Handling Instructions
-----------------------------

Options may be declared as required so that an error is raised if the user
does not supply a value for the option::

    opts = [
        cfg.StrOpt('service_name', required=True),
        cfg.StrOpt('image_id', required=True),
        ...
    ]

Options may be declared as secret so that their values are not leaked into
log files::

     opts = [
        cfg.StrOpt('s3_store_access_key', secret=True),
        cfg.StrOpt('s3_store_secret_key', secret=True),
        ...
     ]

Global ConfigOpts
-----------------

This module also contains a global instance of the ConfigOpts class
in order to support a common usage pattern in OpenStack::

    from oslo_config import cfg

    opts = [
        cfg.StrOpt('bind_host', default='0.0.0.0'),
        cfg.IntOpt('bind_port', default=9292),
    ]

    CONF = cfg.CONF
    CONF.register_opts(opts)

    def start(server, app):
        server.start(app, CONF.bind_port, CONF.bind_host)
