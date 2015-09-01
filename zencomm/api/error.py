#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: Frank Han (frank@esse.io)
#
#


from zencomm.api.constants import LANG_DFT, LANG_SUPPORTED
from zencomm.api import error_code as ErrCode
from zencomm.api import error_msg as ErrMsg


ERROR_MAP = {
    ErrCode.INVALID_PARAMETERS_PROVIDED: ErrMsg.INVALID_PARAMETERS_PROVIDED,
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.USER_REGISTRATION_FAILURE: ErrMsg.USER_REGISTRATION_FAILURE,
    ErrCode.SESSION_CREATION_FAILURE: ErrMsg.SESSION_CREATION_FAILURE,
    ErrCode.SESSION_DELETE_FAILURE: ErrMsg.SESSION_DELETE_FAILURE,
    ErrCode.ACTIVITY_REGISTRATION_FAILURE:
    ErrMsg.ACTIVITY_REGISTRATION_FAILURE,
    ErrCode.CHILD_CREATION_FAILURE: ErrMsg.CHILD_CREATION_FAILURE,
    ErrCode.FAMILY_CREATION_FAILURE: ErrMsg.FAMILY_CREATION_FAILURE,
    ErrCode.FAMILY_DELETE_FAILURE: ErrMsg.FAMILY_DELETE_FAILURE,
    ErrCode.UNKNOWN_SERVER_FAILUER: ErrMsg.ERRMSG_UNKNOWN_SERVER_FAILUER,
}


class ErrorInfo():
    '''
        Format error information, including:
            error_code and error_msg
    '''

    def __init__(self, errcode, message=None, args=None):
        '''
            @param errcode: error code
            @param message: detailed error message if needed
        '''
        self.errcode = errcode
        self.message = message
        self.args = args

    def get_errcode(self):
        return self.errcode

    def get_errmsg(self, lang=None):
        '''
            get error message
        '''
        lang = LANG_DFT if lang not in LANG_SUPPORTED else lang

        default_msg = ERROR_MAP.get(self.errcode, {}).get(lang, "")
        if not self.message:
            return default_msg
        if self.args is not None:
            msg = self.message.get(lang) % self.args
        else:
            msg = self.message.get(lang)
        return default_msg + ", " + msg
