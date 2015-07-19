import sys
import zencomm.api.error_code as ErrCode

class APIException(Exception):
    """Base zen-api Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = "An unknown exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                '''
                LOG.exception(_LE('Exception in string format operation'))
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))    # noqa

                message = self.msg_fmt
                '''
        self.message = message
        super(APIException, self).__init__(message)


class UserCreateFailure(APIException):
    msg_fmt = "Failed to create user: %(reason)s"
    error_code = ErrCode.USER_REGISTRATION_FAILURE

class UserModifyFailure(APIException):
    msg_fmt = "Failed to create user: %(reason)s"

class SessionCreateFailure(APIException):
    msg_fmt = "Failed to create session for user %(user)s: %(reason)s"
    error_code = ErrCode.SESSION_CREATION_FAILURE

class SessionDeleteFailure(APIException):
    msg_fmt = "Failed to delete session: %(reason)s"
    error_code = ErrCode.SESSION_DELETE_FAILURE


class ActivityCreateFailure(APIException):
    msg_fmt = "Failed to create activity: %(reason)s"
    error_code = ErrCode.ACTIVITY_REGISTRATION_FAILURE

class ActivityModifyFailure(APIException):
    msg_fmt = "Failed to modify activity: %(reason)s"

    
class ChildCreateFailure(APIException):
    msg_fmt = "Failed to create child: %(reason)s"
    error_code = ErrCode.CHILD_CREATION_FAILURE
    
class FamilyCreateFailure(APIException):
    msg_fmt = "Failed to create family: %(reason)s"
    error_code = ErrCode.FAMILY_CREATION_FAILURE
