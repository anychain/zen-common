from zencomm.api import error_code as ErrCode
from zencomm.api import error_msg as ErrMsg

error_map = {
    ErrCode.INVALID_PARAMETERS_PROVIDED: ErrMsg.INVALID_PARAMETERS_PROVIDED,
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.SESSION_CREATION_FAILURE: ErrMsg.SESSION_CREATION_FAILURE,
    ErrCode.SESSION_DELETE_FAILURE: ErrMsg.SESSION_DELETE_FAILURE,
    ErrCode.ACTIVITY_REGISTRATION_FAILURE:
    ErrMsg.ACTIVITY_REGISTRATION_FAILURE,
    ErrCode.CHILD_CREATION_FAILURE: ErrMsg.CHILD_CREATION_FAILURE,
    ErrCode.CHILD_DELETE_FAILURE: ErrMsg.CHILD_DELETE_FAILURE,
    ErrCode.FAMILY_CREATION_FAILURE: ErrMsg.FAMILY_CREATION_FAILURE,
    ErrCode.FAMILY_DELETE_FAILURE: ErrMsg.FAMILY_DELETE_FAILURE,
    ErrCode.UNKNOWN_SERVER_FAILUER: ErrMsg.UNKNOWN_SERVER_FAILUER,
}


class Error():
    '''
        error code and error message
    '''
    def __init__(self, errcode, errmsg=None):
        '''
        '''
        self.errcode = errcode
        if errmsg is None:
            return error_map[errcode]

    def get_errcode(self):
        return self.errcode

    def get_errmsg(self):
        return self.errmsg
