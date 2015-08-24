# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#


'''
    api request constant
'''

# ACTIONS

# 0) ACTION RESOURCE
RESOURCE_USER = 'user'
RESOURCE_SESSION = 'session'
RESOURCE_ACTIVITY = 'activity'
RESOURCE_CHILD = 'child'
RESOURCE_FAMILY = 'family'
RESOURCE_DATADICT = 'datadict'
RESOURCE_BRANCH = 'branch'
RESOURCE_ORGANIZATION = 'organization'
RESOURCE_ADDRCODE = 'addrcode'
RESOURCE_ADMIN = 'admin'
RESOURCE_NEWS = 'news'

# 1) USER ACTION
ACTION_USER_CREATE = 'ACTION_USER_CREATE'
ACTION_USER_UPDATE = 'ACTION_USER_UPDATE'
ACTION_USER_DELETE = 'ACTION_USER_DELETE'
ACTION_USER_LIST = 'ACTION_USER_LIST'
ACTION_USER_DETAIL = 'ACTION_USER_DETAIL'
ACTION_USER_RESET_PASSWD = 'ACTION_USER_RESET_PASSWD'
ACTION_USER_CHILD_LIST = 'ACTION_USER_CHILD_LIST'
ACTION_USER_ATTEND_ACTIVITY_LIST = 'ACTION_USER_ATTEND_ACTIVITY_LIST'


RESOURCE_USER_STATUS_INACTIVE = 'INACTIVE'
RESOURCE_USER_STATUS_ACTIVE = 'ACTIVE'

# 2) SESSION ACTION
ACTION_SESSION_CREATE = 'ACTION_SESSION_CREATE'
ACTION_SESSION_DELETE = 'ACTION_SESSION_DELETE'
ACTION_SESSION_RENEW = 'ACTION_SESSION_RENEW'

# 3) ACTIVITY ACTION
ACTION_ACTIVITY_CREATE = 'ACTION_ACTIVITY_CREATE'
ACTION_ACTIVITY_UPDATE = 'ACTION_ACTIVITY_UPDATE'
ACTION_ACTIVITY_DELETE = 'ACTION_ACTIVITY_DELETE'
ACTION_ACTIVITY_LIST = 'ACTION_ACTIVITY_LIST'
ACTION_ACTIVITY_DETAIL = 'ACTION_ACTIVITY_DETAIL'

# 4) CHILD_ACTION
ACTION_CHILD_LIST = 'ACTION_CHILD_LIST'
ACTION_CHILD_CREATE = 'ACTION_CHILD_CREATE'
ACTION_CHILD_UPDATE = 'ACTION_CHILD_UPDATE'
ACTION_CHILD_DELETE = 'ACTION_CHILD_DELETE'
ACTION_CHILD_DETAIL = 'ACTION_CHILD_DETAIL'

# 5) FAMILY_ACTION
ACTION_FAMILY_LIST = 'ACTION_FAMILY_LIST'
ACTION_FAMILY_CREATE = 'ACTION_FAMILY_CREATE'
ACTION_FAMILY_UPDATE = 'ACTION_FAMILY_UPDATE'
ACTION_FAMILY_DELETE = 'ACTION_FAMILY_DELETE'
ACTION_FAMILY_DETAIL = 'ACTION_FAMILY_DETAIL'

# 6) DATADICT ACTION
ACTION_DATADICT_CREATE = 'ACTION_DATADICT_CREATE'
ACTION_DATADICT_UPDATE = 'ACTION_DATADICT_UPDATE'
ACTION_DATADICT_DELETE = 'ACTION_DATADICT_DELETE'
ACTION_DATADICT_LIST = 'ACTION_DATADICT_LIST'
ACTION_DATADICT_DETAIL = 'ACTION_DATADICT_DETAIL'

# 7) BRANCH ACTION
ACTION_BRANCH_CREATE = 'ACTION_BRANCH_CREATE'
ACTION_BRANCH_UPDATE = 'ACTION_BRANCH_UPDATE'
ACTION_BRANCH_DELETE = 'ACTION_BRANCH_DELETE'
ACTION_BRANCH_LIST = 'ACTION_BRANCH_LIST'
ACTION_BRANCH_DETAIL = 'ACTION_BRANCH_DETAIL'

# 8) ORGANIZATION ACTION
ACTION_ORGANIZATION_CREATE = 'ACTION_ORGANIZATION_CREATE'
ACTION_ORGANIZATION_UPDATE = 'ACTION_ORGANIZATION_UPDATE'
ACTION_ORGANIZATION_DELETE = 'ACTION_ORGANIZATION_DELETE'
ACTION_ORGANIZATION_LIST = 'ACTION_ORGANIZATION_LIST'
ACTION_ORGANIZATION_DETAIL = 'ACTION_ORGANIZATION_DETAIL'
ACTION_ORGANIZATION_ADMIN_LIST = 'ACTION_ORGANIZATION_ADMIN_LIST'
ACTION_ORGANIZATION_ADMIN_SEARCH = 'ACTION_ORGANIZATION_ADMIN_SEARCH'
ACTION_ORGANIZATION_ADMIN_ADD = 'ACTION_ORGANIZATION_ADMIN_ADD'
ACTION_ORGANIZATION_ADMIN_DELETE = 'ACTION_ORGANIZATION_ADMIN_DELETE'
ACTION_ORGANIZATION_ACTIVITY_LIST = 'ACTION_ORGANIZATION_ACTIVITY_LIST'

# 9) ATTACHMENT
ATTACHMENT_MAX_SIZE = 5242880   # max attachment size 5M
ATTACHMENT_VALID_IMG_TYPE = ['jpeg', 'png']

# 10) ADDRCODE ACTION
ACTION_ADDRCODE_CREATE = 'ACTION_ADDRCODE_CREATE'
ACTION_ADDRCODE_UPDATE = 'ACTION_ADDRCODE_UPDATE'
ACTION_ADDRCODE_DELETE = 'ACTION_ADDRCODE_DELETE'
ACTION_ADDRCODE_LIST = 'ACTION_ADDRCODE_LIST'
ACTION_ADDRCODE_DETAIL = 'ACTION_ADDRCODE_DETAIL'

# 11) ADMIN ACTION
ACTION_ADMIN_CREATE = 'ACTION_ADMIN_CREATE'
ACTION_ADMIN_UPDATE = 'ACTION_ADMIN_UPDATE'
ACTION_ADMIN_DELETE = 'ACTION_ADMIN_DELETE'
ACTION_ADMIN_LIST = 'ACTION_ADMIN_LIST'
ACTION_ADMIN_DETAIL = 'ACTION_ADMIN_DETAIL'
ACTION_ADMIN_RESET_PASSWD = 'ACTION_ADMIN_RESET_PASSWD'
ACTION_ADMIN_ORGANIZATION_LIST = 'ACTION_ADMIN_ORGANIZATION_LIST'
ACTION_ADMIN_BRANCH_LIST = 'ACTION_ADMIN_BRANCH_LIST'

RESOURCE_ADMIN_STATUS_INACTIVE = 'INACTIVE'
RESOURCE_ADMIN_STATUS_ACTIVE = 'ACTIVE'


# 3) NEWS ACTION
ACTION_NEWS_CREATE = 'ACTION_NEWS_CREATE'
ACTION_NEWS_UPDATE = 'ACTION_NEWS_UPDATE'
ACTION_NEWS_DELETE = 'ACTION_NEWS_DELETE'
ACTION_NEWS_LIST = 'ACTION_NEWS_LIST'
ACTION_NEWS_DETAIL = 'ACTION_NEWS_DETAIL'
