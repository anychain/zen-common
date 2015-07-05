"""Zen logging handler.

This module adds to logging functionality by adding the option to specify
a context object when calling the various log methods.  If the context object
is not specified, default formatting is used. Additionally, an instance uuid
may be passed as part of the log message, which is intended to make it easier
for admins to find messages related to a specific instance.

It also allows setting of formatting information through conf.

"""

import logging
import logging.config
import logging.handlers
import os
import sys
try:
    import syslog
except ImportError:
    syslog = None
import traceback

import six
from six import moves

from logger import formatters
from logger import handlers

def _get_log_file_path(conf, binary=None):
    logfile = conf.log_file
    logdir = conf.log_dir

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)

    if logdir:
        binary = binary or handlers._get_binary_name()
        return '%s.log' % (os.path.join(logdir, binary),)

    return None


class BaseLoggerAdapter(logging.LoggerAdapter):

    warn = logging.LoggerAdapter.warning

    @property
    def handlers(self):
        return self.logger.handlers

    def isEnabledFor(self, level):
        if _PY26:
            # This method was added in python 2.7 (and it does the exact
            # same logic, so we need to do the exact same logic so that
            # python 2.6 has this capability as well).
            return self.logger.isEnabledFor(level)
        else:
            return super(BaseLoggerAdapter, self).isEnabledFor(level)

class KeywordArgumentAdapter(BaseLoggerAdapter):
    """Logger adapter to add keyword arguments to log record's extra data

    Keywords passed to the log call are added to the "extra"
    dictionary passed to the underlying logger so they are emitted
    with the log message and available to the format string.

    Special keywords:

    extra
      An existing dictionary of extra values to be passed to the
      logger. If present, the dictionary is copied and extended.

    """

    def process(self, msg, kwargs):
        extra = {}
        extra.update(self.extra)
        if 'extra' in kwargs:
            extra.update(kwargs.pop('extra'))
        # Move any unknown keyword arguments into the extra
        # dictionary.
        for name in list(kwargs.keys()):
            if name == 'exc_info':
                continue
            extra[name] = kwargs.pop(name)
        kwargs['extra'] = extra

        return msg, kwargs


def _create_logging_excepthook(product_name):
    def logging_excepthook(exc_type, value, tb):
        extra = {'exc_info': (exc_type, value, tb)}
        getLogger(product_name).critical(
            "".join(traceback.format_exception_only(exc_type, value)),
            **extra)
    return logging_excepthook


class LogConfigError(Exception):

    message = 'Error loading logging config %(log_config)s: %(err_msg)s'

    def __init__(self, log_config, err_msg):
        self.log_config = log_config
        self.err_msg = err_msg

    def __str__(self):
        return self.message % dict(log_config=self.log_config,
                                   err_msg=self.err_msg)


def setup(conf, product_name, version='unknown'):
    """Setup logging for the current application."""
    setup_logging_from_conf(conf, product_name, version)
    sys.excepthook = _create_logging_excepthook(product_name)


def set_defaults(logging_context_format_string=None,
                 default_log_levels=None):
    """Set default values for the configuration options used by oslo.log."""
    # Just in case the caller is not setting the
    # default_log_level. This is insurance because
    # we introduced the default_log_level parameter
    # later in a backwards in-compatible change
    if default_log_levels is not None:
        cfg.set_defaults(
            _options.log_opts,
            default_log_levels=default_log_levels)
    if logging_context_format_string is not None:
        cfg.set_defaults(
            _options.log_opts,
            logging_context_format_string=logging_context_format_string)

def _find_facility(facility):
    # NOTE(jd): Check the validity of facilities at run time as they differ
    # depending on the OS and Python version being used.
    valid_facilities = [f for f in
                        ["LOG_KERN", "LOG_USER", "LOG_MAIL",
                         "LOG_DAEMON", "LOG_AUTH", "LOG_SYSLOG",
                         "LOG_LPR", "LOG_NEWS", "LOG_UUCP",
                         "LOG_CRON", "LOG_AUTHPRIV", "LOG_FTP",
                         "LOG_LOCAL0", "LOG_LOCAL1", "LOG_LOCAL2",
                         "LOG_LOCAL3", "LOG_LOCAL4", "LOG_LOCAL5",
                         "LOG_LOCAL6", "LOG_LOCAL7"]
                        if getattr(syslog, f, None)]

    facility = facility.upper()

    if not facility.startswith("LOG_"):
        facility = "LOG_" + facility

    if facility not in valid_facilities:
        raise TypeError('syslog facility must be one of: %s' %
                        ', '.join("'%s'" % fac
                                  for fac in valid_facilities))

    return getattr(syslog, facility)

def _setup_logging_from_conf(conf, project, version):
    log_root = getLogger(None).logger
    for handler in log_root.handlers:
        log_root.removeHandler(handler)

    logpath = _get_log_file_path(conf)
    if logpath:
        filelog = logging.handlers.WatchedFileHandler(logpath)
        log_root.addHandler(filelog)

    if conf.use_stderr:
        streamlog = handlers.ColorHandler()
        log_root.addHandler(streamlog)

    elif not logpath:
        # pass sys.stdout as a positional argument
        # python2.6 calls the argument strm, in 2.7 it's stream
        streamlog = logging.StreamHandler(sys.stdout)
        log_root.addHandler(streamlog)

    if conf.use_syslog:
        global syslog
        if syslog is None:
            raise RuntimeError("syslog is not available on this platform")
        facility = _find_facility(conf.syslog_log_facility)
        # TODO(bogdando) use the format provided by RFCSysLogHandler after
        # existing syslog format deprecation in J
        syslog = handlers.OSSysLogHandler(
            facility=facility,
            use_syslog_rfc_format=conf.use_syslog_rfc_format)
        log_root.addHandler(syslog)

    datefmt = conf.log_date_format
    for handler in log_root.handlers:
        handler.setFormatter(formatters.ContextFormatter(project=project,
                                                         version=version,
                                                         datefmt=datefmt,
                                                         config=conf))

    if conf.debug:
        log_root.setLevel(logging.DEBUG)
    elif conf.verbose:
        log_root.setLevel(logging.INFO)
    else:
        log_root.setLevel(logging.WARNING)

_loggers = {}


def getLogger(name=None, project='unknown', version='unknown'):
    """Build a logger with the given name.

    :param name: The name for the logger. This is usually the module
                 name, ``__name__``.
    :type name: string
    :param project: The name of the project, to be injected into log
                    messages. For example, ``'nova'``.
    :type project: string
    :param version: The version of the project, to be injected into log
                    messages. For example, ``'2014.2'``.
    :type version: string
    """
    if name not in _loggers:
        _loggers[name] = KeywordArgumentAdapter(logging.getLogger(name),
                                                {'project': project,
                                                 'version': version})
    return _loggers[name]
