#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: Frank Han (frank@esse.io)
#
#


from zencomm.api.constants import LANG_DFT, LANG_SUPPORTED
from zencomm.api import error_code as ErrCodes
from zencomm.api import error_msg as ErrMsg


ERROR_MAP = {
    # new defined error message
    ErrCodes.UNKNOWN_SERVER_FAILUER: ErrMsg.ERRMSG_UNKNOWN_SERVER_FAILUER,
    ErrCodes.INVALID_REQUEST_METHOD: ErrMsg.ERRMSG_INVALID_REQUEST_METHOD,
    ErrCodes.POST_ACTION_NOT_ALLOWED: ErrMsg.ERRMSG_POST_ACTION_NOT_ALLOWED,
    ErrCodes.INVALID_REQUEST_FORMAT: ErrMsg.ERRMSG_INVALID_REQUEST_FORMAT,
    ErrCodes.USER_SESSION_EXPIRED: ErrMsg.ERRMSG_INVALID_REQUEST_FORMAT
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
