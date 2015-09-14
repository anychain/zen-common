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

# 0) request type
APIREQ_SESSION = 'session'
APIREQ_ZENWEB = 'zenweb'


# ACTIONS
# 0) ACTION RESOURCE
# resource_constant = RESOURCE + resource.upper()
RESOURCE_SESSION = 'session'
RESOURCE_ACTIVITY = 'activity'
RESOURCE_CHILD = 'child'
RESOURCE_MEMBER = 'member'
RESOURCE_FAMILY = 'family'
RESOURCE_DATADICT = 'datadict'
RESOURCE_BRANCH = 'branch'
RESOURCE_ORGANIZATION = 'organization'
RESOURCE_ADDRCODE = 'addrcode'
RESOURCE_ADMIN = 'admin'
RESOURCE_NEWS = 'news'
RESOURCE_CAROUSEL = 'carousel'
RESOURCE_BUG = 'bug'
RESOURCE_CATEGORY = 'category'
RESOURCE_AMY = 'amy'
RESOURCE_PRODUCT = 'product'
RESOURCE_ORDER = 'order'


# singlar map for special resources
# others just remove 's' from plural api url
RESOURCE_SINGLAR_TABLE = {
    'activities': RESOURCE_ACTIVITY,
    'children': RESOURCE_CHILD,
    'families': RESOURCE_FAMILY,
    'news': RESOURCE_NEWS,
    'branches': RESOURCE_BRANCH,
    'categories': RESOURCE_CATEGORY,
}

# 1) FAMILY ACTION
# all action value must start with resource_name
ACTION_FAMILY_CREATE = '%s_create' % RESOURCE_FAMILY
ACTION_FAMILY_UPDATE = '%s_update' % RESOURCE_FAMILY
ACTION_FAMILY_DELETE = '%s_delete' % RESOURCE_FAMILY
ACTION_FAMILY_LIST = '%s_list' % RESOURCE_FAMILY
ACTION_FAMILY_DETAIL = '%s_detail' % RESOURCE_FAMILY
ACTION_FAMILY_RESET_PASSWD = '%s_resetpass' % RESOURCE_FAMILY
ACTION_FAMILY_CHILD_LIST = '%s_%s_list' % (RESOURCE_FAMILY, RESOURCE_CHILD)
ACTION_FAMILY_MEMBER_LIST = '%s_%s_list' % (RESOURCE_FAMILY, RESOURCE_MEMBER)
ACTION_FAMILY_ACTIVITY_LIST = '%s_%s_list' % (RESOURCE_FAMILY, RESOURCE_ACTIVITY)


RESOURCE_FAMILY_STATUS_INACTIVE = 'INACTIVE'
RESOURCE_FAMILY_STATUS_ACTIVE = 'ACTIVE'

# 2) SESSION ACTION
ACTION_SESSION_CREATE = 'session_create'
ACTION_SESSION_DELETE = 'session_delete'
ACTION_SESSION_RENEW = 'session_renew'

# 3) ACTIVITY ACTION
ACTION_ACTIVITY_CREATE = '%s_create' % RESOURCE_ACTIVITY
ACTION_ACTIVITY_UPDATE = '%s_update' % RESOURCE_ACTIVITY
ACTION_ACTIVITY_DELETE = '%s_delete' % RESOURCE_ACTIVITY
ACTION_ACTIVITY_LIST = '%s_list' % RESOURCE_ACTIVITY
ACTION_ACTIVITY_DETAIL = '%s_detail' % RESOURCE_ACTIVITY
ACTION_ACTIVITY_JOIN = '%s_join' % (RESOURCE_ACTIVITY)
ACTION_ACTIVITY_FAMILY_LIST = '%s_%s_list' % (RESOURCE_ACTIVITY, RESOURCE_FAMILY)

# 4) CHILD_ACTION
ACTION_CHILD_LIST = 'child_list'
ACTION_CHILD_CREATE = 'child_create'
ACTION_CHILD_UPDATE = 'child_update'
ACTION_CHILD_DELETE = 'child_delete'
ACTION_CHILD_DETAIL = 'child_detail'


# 4) MEMBER_ACTION
ACTION_MEMBER_LIST = 'member_list'
ACTION_MEMBER_CREATE = 'member_create'
ACTION_MEMBER_UPDATE = 'member_update'
ACTION_MEMBER_DELETE = 'member_delete'
ACTION_MEMBER_DETAIL = 'member_detail'


# 6) DATADICT ACTION
ACTION_DATADICT_CREATE = 'datadict_create'
ACTION_DATADICT_UPDATE = 'datadict_update'
ACTION_DATADICT_DELETE = 'datadict_delete'
ACTION_DATADICT_LIST = 'datadict_list'
ACTION_DATADICT_DETAIL = 'datadict_detail'

# 7) BRANCH ACTION
ACTION_BRANCH_CREATE = 'branch_create'
ACTION_BRANCH_UPDATE = 'branch_update'
ACTION_BRANCH_DELETE = 'branch_delete'
ACTION_BRANCH_LIST = 'branch_list'
ACTION_BRANCH_DETAIL = 'branch_detail'

# 8) ORGANIZATION ACTION
ACTION_ORGANIZATION_CREATE = 'organization_create'
ACTION_ORGANIZATION_UPDATE = 'organization_update'
ACTION_ORGANIZATION_DELETE = 'organization_delete'
ACTION_ORGANIZATION_LIST = 'organization_list'
ACTION_ORGANIZATION_DETAIL = 'organization_detail'
ACTION_ORGANIZATION_ADMIN_LIST = 'organization_admin_list'
ACTION_ORGANIZATION_ADMIN_SEARCH = 'organization_admin_search'
ACTION_ORGANIZATION_ADMIN_ADD = 'organization_admin_add'
ACTION_ORGANIZATION_ADMIN_DELETE = 'organization_admin_delete'
ACTION_ORGANIZATION_ACTIVITY_LIST = 'organization_activity_list'

# 9) ATTACHMENT
ATTACHMENT_MAX_SIZE = 5242880   # max attachment size 5M
ATTACHMENT_VALID_IMG_TYPE = ['jpeg', 'png']

# 10) ADDRCODE ACTION
ACTION_ADDRCODE_CREATE = 'addrcode_create'
ACTION_ADDRCODE_UPDATE = 'addrcode_update'
ACTION_ADDRCODE_DELETE = 'addrcode_delete'
ACTION_ADDRCODE_LIST = 'addrcode_list'
ACTION_ADDRCODE_DETAIL = 'addrcode_detail'

# 11) ADMIN ACTION
ACTION_ADMIN_CREATE = 'admin_create'
ACTION_ADMIN_UPDATE = 'admin_update'
ACTION_ADMIN_DELETE = 'admin_delete'
ACTION_ADMIN_LIST = 'admin_list'
ACTION_ADMIN_DETAIL = 'admin_detail'
ACTION_ADMIN_RESET_PASSWD = 'admin_resetpass'
ACTION_ADMIN_ORGANIZATION_LIST = 'admin_organization_list'
ACTION_ADMIN_BRANCH_LIST = 'admin_branch_list'

RESOURCE_ADMIN_STATUS_INACTIVE = 'INACTIVE'
RESOURCE_ADMIN_STATUS_ACTIVE = 'ACTIVE'


# 12) NEWS ACTION
ACTION_NEWS_CREATE = 'news_create'
ACTION_NEWS_UPDATE = 'news_update'
ACTION_NEWS_DELETE = 'news_delete'
ACTION_NEWS_LIST = 'news_list'
ACTION_NEWS_DETAIL = 'news_detail'


# 13) CAROUSEL ACTION
ACTION_CAROUSEL_CREATE = 'carousel_create'
ACTION_CAROUSEL_DELETE = 'carousel_delete'
ACTION_CAROUSEL_LIST = 'carousel_list'
ACTION_CAROUSEL_DETAIL = 'carousel_detail'

# 14) review status
REVIEW_STATUS_PENDING = 'pending'
REVIEW_STATUS_APPROVED = 'approved'
REVIEW_STATUS_REJECTED = 'rejected'


# 15) Language constants
LANG_SUPPORTED = ['en', 'zh_cn']
LANG_DFT = 'zh_cn'
LANG_EN = 'en'
LANG_ZH_CN = 'zh_cn'


# 16) BUG ACTION
ACTION_BUG_CREATE = 'bug_create'
ACTION_BUG_UPDATE = 'bug_update'
ACTION_BUG_DELETE = 'bug_delete'
ACTION_BUG_LIST = 'bug_list'
ACTION_BUG_DETAIL = 'bug_detail'


# 17) BUG status
BUG_STATUS_NEW = 'new'
BUG_STATUS_WORKING = 'working'
BUG_STATUS_RESOLVED = 'resolved'
BUG_STATUS_VERIFIED = 'verified'


# 18) CATEGORY ACTION
ACTION_CATEGORY_CREATE = 'category_create'
ACTION_CATEGORY_UPDATE = 'category_update'
ACTION_CATEGORY_DELETE = 'category_delete'
ACTION_CATEGORY_LIST = 'category_list'
ACTION_CATEGORY_DETAIL = 'category_detail'


# 19) AMY ACTION
ACTION_AMY_CREATE = 'amy_create'
ACTION_AMY_UPDATE = 'amy_update'
ACTION_AMY_DELETE = 'amy_delete'
ACTION_AMY_LIST = 'amy_list'
ACTION_AMY_DETAIL = 'amy_detail'


# 20) PRODUCT ACTION
ACTION_PRODUCT_CREATE = 'product_create'
ACTION_PRODUCT_UPDATE = 'product_update'
ACTION_PRODUCT_DELETE = 'product_delete'
ACTION_PRODUCT_LIST = 'product_list'
ACTION_PRODUCT_DETAIL = 'product_detail'


# 21) ORDER ACTION
ACTION_ORDER_CREATE = 'order_create'
ACTION_ORDER_UPDATE = 'order_update'
ACTION_ORDER_DELETE = 'order_delete'
ACTION_ORDER_LIST = 'order_list'
ACTION_ORDER_DETAIL = 'order_detail'

# APIREQ_TYPE_MAP = {
APIREQ_ATTRIBUTE = {
    ACTION_FAMILY_CREATE: {'type': APIREQ_SESSION,
                           'required_params': ['phone', 'passwd']},
    ACTION_FAMILY_UPDATE: {'type': APIREQ_SESSION,
                           'required_params': ['phone']},
    ACTION_FAMILY_DELETE: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_FAMILY_LIST: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_FAMILY_DETAIL: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_FAMILY_RESET_PASSWD: {'type': APIREQ_SESSION,
                                 'required_params': []},
    ACTION_FAMILY_CHILD_LIST: {'type': APIREQ_SESSION,
                               'required_params': []},
    ACTION_FAMILY_MEMBER_LIST: {'type': APIREQ_SESSION,
                                'required_params': []},
    ACTION_FAMILY_ACTIVITY_LIST: {'type': APIREQ_SESSION,
                                         'required_params': ['id']},
    ACTION_SESSION_CREATE: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_SESSION_DELETE: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_SESSION_RENEW: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_ACTIVITY_CREATE: {'type': APIREQ_SESSION,
                             'required_params': ['name', 'addrcode', 'address',
                                                 'size', 'type', 'subject',
                                                 'poster', 'content',
                                                 'begin_time', 'end_time']},
    ACTION_ACTIVITY_UPDATE: {'type': APIREQ_SESSION,
                             'required_params': ['id']},
    ACTION_ACTIVITY_DELETE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ACTIVITY_LIST: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_ACTIVITY_DETAIL: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ACTIVITY_JOIN: {'type': APIREQ_SESSION,
                             'required_params': ['id', 'family_id']},                    
    ACTION_CHILD_LIST: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_CHILD_CREATE: {'type': APIREQ_SESSION,
                          'required_params': ['name', 'birthday',
                                              'gender']},
    ACTION_CHILD_UPDATE: {'type': APIREQ_SESSION,
                          'required_params': ['name', 'birthday',
                                              'gender']},
    ACTION_CHILD_DELETE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_CHILD_DETAIL: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_MEMBER_LIST: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_MEMBER_CREATE: {'type': APIREQ_SESSION,
                           'required_params': ['name', 'birthday',
                                               'gender']},
    ACTION_MEMBER_UPDATE: {'type': APIREQ_SESSION,
                           'required_params': ['name', 'birthday',
                                               'gender']},
    ACTION_MEMBER_DELETE: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_MEMBER_DETAIL: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_DATADICT_CREATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_DATADICT_UPDATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_DATADICT_DELETE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_DATADICT_LIST: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_DATADICT_DETAIL: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_BRANCH_CREATE: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_BRANCH_UPDATE: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_BRANCH_DELETE: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_BRANCH_LIST: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_BRANCH_DETAIL: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_ORGANIZATION_CREATE: {'type': APIREQ_SESSION,
                                 'required_params': []},
    ACTION_ORGANIZATION_UPDATE: {'type': APIREQ_SESSION,
                                 'required_params': []},
    ACTION_ORGANIZATION_DELETE: {'type': APIREQ_SESSION,
                                 'required_params': []},
    ACTION_ORGANIZATION_LIST: {'type': APIREQ_SESSION,
                               'required_params': []},
    ACTION_ORGANIZATION_DETAIL: {'type': APIREQ_SESSION,
                                 'required_params': []},
    ACTION_ORGANIZATION_ADMIN_LIST: {'type': APIREQ_SESSION,
                                     'required_params': []},
    ACTION_ORGANIZATION_ADMIN_SEARCH: {'type': APIREQ_SESSION,
                                       'required_params': []},
    ACTION_ORGANIZATION_ADMIN_ADD: {'type': APIREQ_SESSION,
                                    'required_params': []},
    ACTION_ORGANIZATION_ADMIN_DELETE: {'type': APIREQ_SESSION,
                                       'required_params': []},
    ACTION_ORGANIZATION_ACTIVITY_LIST: {'type': APIREQ_SESSION,
                                        'required_params': []},
    ACTION_ADDRCODE_CREATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ADDRCODE_UPDATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ADDRCODE_DELETE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ADDRCODE_LIST: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_ADDRCODE_DETAIL: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_ADMIN_CREATE: {'type': APIREQ_SESSION,
                          'required_params': ['phone', 'passwd']},
    ACTION_ADMIN_UPDATE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ADMIN_DELETE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ADMIN_LIST: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_ADMIN_DETAIL: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ADMIN_RESET_PASSWD: {'type': APIREQ_SESSION,
                                'required_params': []},
    ACTION_ADMIN_ORGANIZATION_LIST: {'type': APIREQ_SESSION,
                                     'required_params': []},
    ACTION_ADMIN_BRANCH_LIST: {'type': APIREQ_SESSION,
                               'required_params': []},
    ACTION_NEWS_CREATE: {'type': APIREQ_SESSION,
                         'required_params': ['name', 'summary',
                                             'poster', 'content']},
    ACTION_NEWS_UPDATE: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_NEWS_DELETE: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_NEWS_LIST: {'type': APIREQ_SESSION,
                       'required_params': []},
    ACTION_NEWS_DETAIL: {'type': APIREQ_SESSION,
                         'required_params': []},
    ACTION_CAROUSEL_CREATE: {'type': APIREQ_SESSION,
                             'required_params': ['object_id', 'object_type',
                                                 'name', 'poster']},
    ACTION_CAROUSEL_DELETE: {'type': APIREQ_SESSION, 'required_params': []},
    ACTION_CAROUSEL_LIST: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_CAROUSEL_DETAIL: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_BUG_CREATE: {'type': APIREQ_SESSION,
                        'required_params': ['title', 'description', 'type',
                                            'target', 'operation']},
    ACTION_BUG_UPDATE: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_BUG_DELETE: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_BUG_LIST: {'type': APIREQ_SESSION,
                      'required_params': []},
    ACTION_BUG_DETAIL: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_CATEGORY_CREATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_CATEGORY_UPDATE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_CATEGORY_DELETE: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_CATEGORY_LIST: {'type': APIREQ_SESSION,
                           'required_params': []},
    ACTION_CATEGORY_DETAIL: {'type': APIREQ_SESSION,
                             'required_params': []},
    ACTION_AMY_CREATE: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_AMY_UPDATE: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_AMY_DELETE: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_AMY_LIST: {'type': APIREQ_SESSION,
                      'required_params': []},
    ACTION_AMY_DETAIL: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_PRODUCT_CREATE: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_PRODUCT_UPDATE: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_PRODUCT_DELETE: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_PRODUCT_LIST: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_PRODUCT_DETAIL: {'type': APIREQ_SESSION,
                            'required_params': []},
    ACTION_ORDER_CREATE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ORDER_UPDATE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ORDER_DELETE: {'type': APIREQ_SESSION,
                          'required_params': []},
    ACTION_ORDER_LIST: {'type': APIREQ_SESSION,
                        'required_params': []},
    ACTION_ORDER_DETAIL: {'type': APIREQ_SESSION,
                          'required_params': []},
}

