from zencomm.api import error_code as ErrCode
from zencomm.api import error_msg as ErrMsg

error_map = {
    ErrCode.INVALID_PARAMETERS_PROVIDED : ErrMsg.INVALID_PARAMETERS_PROVIDED, 
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.SESSION_CREATION_FAILURE: ErrMsg.SESSION_CREATION_FAILURE,
    ErrCode.SESSION_DELETE_FAILURE: ErrMsg.SESSION_DELETE_FAILURE,
    ErrCode.ACTIVITY_REGISTRATION_FAILURE: ErrMsg.ACTIVITY_REGISTRATION_FAILURE,
    ErrCode.CHILD_CREATION_FAILURE: ErrMsg.CHILD_CREATION_FAILURE,
    ErrCode.CHILD_DELETE_FAILURE: ErrMsg.CHILD_DELETE_FAILURE,
    ErrCode.FAMILY_CREATION_FAILURE: ErrMsg.FAMILY_CREATION_FAILURE,
    ErrCode.FAMILY_DELETE_FAILURE: ErrMsg.FAMILY_DELETE_FAILURE,
    ErrCode.UNKNOWN_SERVER_FAILUER: ErrMsg.UNKNOWN_SERVER_FAILUER,
}


def get_errmsg(error_code):
    '''
        get error message according to error code
    '''
    return error_map[error_code]
    