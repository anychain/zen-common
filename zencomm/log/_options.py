from zencomm.conf import cfg


_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


log_opts = [
    cfg.BoolOpt('debug',
                default=True,
                help='debug'),
    cfg.BoolOpt('verbose',
                default=True,
                help='info'),
    cfg.StrOpt('log_dir',
               default='/opt/zen/logs/',
               help='(Optional) Name of log file to output to. '
                    'If no default is set, logging will go to stdout.'),
    cfg.StrOpt('log_date_format',
               default=_DEFAULT_LOG_DATE_FORMAT,
               help='Format string for %%(asctime)s in log records. '
                    'Default: %(default)s .'),
    cfg.StrOpt('log_format',
               default='%(asctime)s.%(msecs)03d %(thread)d %(levelname)s '
                       '%(name)s [-] %(message)s [-] '
                       '%(module)s %(funcName)s:%(lineno)d',
               help='log format'),
    cfg.StrOpt('logging_debug_format',
               default='%(funcName)s %(pathname)s:%(lineno)d',
               help='Data to append to log format when level is DEBUG.'),
    cfg.BoolOpt('use_stderr',
                default=True,
                help='Log output to standard error.'),
    cfg.BoolOpt('use-syslog',
                default=False,
                help='Use syslog for logging. '
                     'Existing syslog format is DEPRECATED '
                     'and will be changed later to honor RFC5424.'),
]

cfg.CONF.register_opts(log_opts)
