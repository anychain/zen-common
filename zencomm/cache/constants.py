#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: Frank Han (frank@esse.io)
#
#

'''
    constants that will be stored in memcache as key
'''

# preoject name
PROJECT_PREFIX = 'Zen'

SESSION_KEY_PREFIX_MEMCACHE = '%s.SessionKey' % PROJECT_PREFIX


MEMCACHE_KEY_TIMEOUT = {
    SESSION_KEY_PREFIX_MEMCACHE: 10800, # 3 hours
}
