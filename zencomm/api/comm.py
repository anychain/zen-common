from rest_framework.response import Response
from rest_framework import status
import json

HTTP_STATUS = {
    'POST': status.HTTP_201_CREATED,
    'GET': status.HTTP_200_OK,
    'PUT': status.HTTP_204_NO_CONTENT,
    'DELETE': status.HTTP_204_NO_CONTENT
}

def build_reply(retcode=0, retbody={}):
    '''
        build json reply according to retcode and data
    '''
    reply = {
        'retcode': retcode,
        'retbody': retbody
    }
    return json.dumps(reply)

def reply_error_to_client(request, retcode, retbody, status=status.HTTP_400_BAD_REQUEST):
    '''
        api reply error message to client
    '''
    reply = build_reply(retcode, retbody)
    response = Response(reply, status)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def reply_success_to_client(request, reply):
    '''
        api reply error message to client
        @param data: request recevied from ws in json format
    '''
    status = HTTP_STATUS[request.method]
    response = Response(reply, status)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def check_reply_to_client(request, reply):
    '''
        check reply(json) from ws and reply to client
    '''
    ret = json.loads(reply)

    if ret['retcode'] != 0:
        return reply_error_to_client(request, ret['retcode'], ret['retbody'], status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return reply_success_to_client(request, reply)
