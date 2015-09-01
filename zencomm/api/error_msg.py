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
    This files records all the error code for api
'''
from zencomm.api.constants import LANG_EN
from zencomm.api.constants import LANG_ZH_CN


INVALID_PARAMETERS_PROVIDED = 'INVALID_PARAMETERS_PROVIDED'
USER_REGISTRATION_FAILURE = 'USER_REGISTRATION_FAILURE'

SESSION_CREATION_FAILURE = 'SESSION_CREATION_FAILURE'
SESSION_DELETE_FAILURE = 'SESSION_CREATION_FAILURE'

ACTIVITY_REGISTRATION_FAILURE = 'ACTIVITY_REGISTRATION_FAILURE'

CHILD_CREATION_FAILURE = 'CHILD_CREATION_FAILURE'
CHILD_DELETE_FAILURE = 'CHILD_CREATION_FAILURE'

FAMILY_CREATION_FAILURE = 'CHILD_CREATION_FAILURE'
FAMILY_DELETE_FAILURE = 'CHILD_CREATION_FAILURE'

ERRMSG_UNKNOWN_SERVER_FAILUER = {LANG_EN: "unknow server failure",
                                 LANG_ZH_CN: u"未知错误"}
