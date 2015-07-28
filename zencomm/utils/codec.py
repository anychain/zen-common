'''
@copyright:      Copyright esse.io. 2015 All Rights Reserved
@license:        Property of esse.io
@author:         Frank Han (frank@esse.io)
@version:        created at 2015-07-28

common encoding utils

'''

import base64
import zencomm.log as logging


def base64_encode(src):
    '''
        encode src with base64
    '''
    result = ''
    try:
        result = base64.standard_b64encode(src)
    except Exception as e:
        logging.error('encode base64string error: [%s]' % e)
    return result

def base64_decode(src):
    '''
        decode base64 encoded string
    '''
    result = ''
    try:
        result = base64.standard_b64decode(src)
    except Exception, e:
        logging.error('decode base64string error: [%s]' % e)
    return result

if __name__ == "__main__":
    import sys
    input_str = "hello,world"
    if len(sys.argv) == 2:
        input_str = sys.argv[1]
    print "Source string is %s" % input_str
    b64str = base64_encode(input_str)
    print "After base64 encode, the string is %s" % b64str
    source_str = base64_decode(b64str)
    print "After base64 decode, the source string is %s" % source_str
