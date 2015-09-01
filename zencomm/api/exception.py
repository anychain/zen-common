# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#


import zencomm.api.error_code as ErrCode
from zencomm.exception import ZenException


# 1) user creation exception

class UserCreateFailure(ZenException):
    msg_fmt = "Failed to create user: %(reason)s"
    error_code = ErrCode.USER_REGISTRATION_FAILURE


class UserAlreadyExist(ZenException):
    msg_fmt = "User already exist: %(reason)s"
    error_code = ErrCode.USER_ALREADY_REGISTERED


class UserModifyFailure(ZenException):
    msg_fmt = "Failed to create user: %(reason)s"


# 2) handle session exception
class SessionCreateFailure(ZenException):
    msg_fmt = "Failed to create session for user %(user)s: %(reason)s"
    error_code = ErrCode.SESSION_CREATION_FAILURE


class SessionDeleteFailure(ZenException):
    msg_fmt = "Failed to delete session: %(reason)s"
    error_code = ErrCode.SESSION_DELETE_FAILURE


class ActivityCreateFailure(ZenException):
    msg_fmt = "Failed to create activity: %(reason)s"
    error_code = ErrCode.ACTIVITY_REGISTRATION_FAILURE


class ActivityModifyFailure(ZenException):
    msg_fmt = "Failed to modify activity: %(reason)s"


class ChildCreateFailure(ZenException):
    msg_fmt = "Failed to create child: %(reason)s"
    error_code = ErrCode.CHILD_CREATION_FAILURE


class ChildAlreadyExist(ZenException):
    msg_fmt = "Child already exist: %(reason)s"
    error_code = ErrCode.USER_ALREADY_REGISTERED


class FamilyCreateFailure(ZenException):
    msg_fmt = "Failed to create family: %(reason)s"
    error_code = ErrCode.FAMILY_CREATION_FAILURE


class InvalidSortKey(ZenException):
    msg_fmt = "Sort key supplied for db query was not valid."
    error_code = ErrCode.UNKNOWN_SERVER_FAILUER


class InternalServerFailuer(ZenException):
    msg_fmt = "Internal service failure: %(reason)s"
    error_code = ErrCode.UNKNOWN_SERVER_FAILUER
