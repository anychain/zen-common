'''
@copyright:      Copyright esse.io. 2015 All Rights Reserved
@license:        Property of esse.io
@author:         Frank Han (frank@esse.io)
@version:        created at 2015-07-28

get file metadata

'''

import magic
from zencomm.log import log as logging

LOG = logging.getLogger(__name__)


def get_file_type(filename):
    '''
        @return: images types like image/jpeg, image/png
    '''

    try:
        ftype = magic.from_file(filename, mime=True)
    except Exception as e:
        LOG.error("failed to file type for file %s with error: %s"
                  % (filename, e))
    return ftype


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print "please input the file to check"
        sys.exit(1)
    filename = sys.argv[1]
    print get_file_type(filename)
