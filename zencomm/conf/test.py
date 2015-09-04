#!/usr/bin/python

from zencomm.conf import cfg

service_opts = [
    cfg.StrOpt('school',
               required=True,
               default='bupt',
               help='Interval, in seconds, between nodes reporting state '
                    'to datastore'),
    cfg.StrOpt('classes',
               default='grade 3',
               help='class name'),
    cfg.IntOpt('number_of_students',
               default=50,
               help='number of students in a class'),
]

# 1) get global CONF
CONF = cfg.CONF
# 2) register options, must be before step 3)
# if not, required=True will not work
CONF.register_opts(service_opts, group='education')
# 3) start parsing configuration files and check required parameters
CONF()  # this will load configuration files
# CONF(validate_default_values=True)

print CONF.education.school

'''
configuration file example:

    [education]
    school='Beijing University of Posts & Telecommunications'
    classes='Grade 3'
    [api]
    ip='222.222.222.222'
    port='444'
    name='zenapi server'
'''
