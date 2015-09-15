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
ERRMSG_INVALID_REQUEST_FORMAT = {LANG_EN: "invalid api request format",
                                 LANG_ZH_CN: u"请求格式不正确"}
ERRMSG_MISSED_REQUEST_PARAM = {LANG_EN: "missed parameter: %s in request",
                               LANG_ZH_CN: u"请求缺失参数: %s"}
ERRMSG_USER_SESSION_EXPIRED = {LANG_EN: "user session has expired, "
                                        "please login again",
                               LANG_ZH_CN: u"用户会话过期, 请重新登陆"}
ERRMSG_INVALID_REQUEST_URL = {LANG_EN: "invalid api request url",
                              LANG_ZH_CN: u"api 请求url不正确"}
ERRMSG_USER_OR_PASSWD_INCORRECT = {LANG_EN: "incorrect user or password",
                                   LANG_ZH_CN: u"用户名或者密码不对"}
ERRMSG_SESSION_CREATE_FAILURE = {LANG_EN: "failed to create user session",
                                   LANG_ZH_CN: u"创建用户会话失败"}
ERRMSG_SESSION_DELETE_FAILURE = {LANG_EN: "failed to delete user session",
                                   LANG_ZH_CN: u"删除用户会话失败"}
