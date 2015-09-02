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
    This files records all the error messages for api
'''

from zencomm.api.constants import LANG_EN
from zencomm.api.constants import LANG_ZH_CN


ERRMSG_UNKNOWN_SERVER_FAILUER = {LANG_EN: "unknow server failure",
                                 LANG_ZH_CN: u"未知错误"}
ERRMSG_INVALID_REQUEST_METHOD = {LANG_EN: "invalid request method",
                                 LANG_ZH_CN: u"请求方法错误"}
ERRMSG_POST_ACTION_NOT_ALLOWED = {LANG_EN: "post action not allowed",
                                 LANG_ZH_CN: u"不支持post方法"}
ERRMSG_INVALID_REQUEST_PARAMS = {LANG_EN: "invalid api request parameters",
                                 LANG_ZH_CN: u"api请求参数不正确"}
