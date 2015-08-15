# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#


from rest_framework.response import Response
from rest_framework import status
import json
from zencomm.log import logger
from zencomm.api import exception


HTTP_SUCCESS_STATUS = {
    'POST': status.HTTP_201_CREATED,
    'GET': status.HTTP_200_OK,
    'PUT': status.HTTP_204_NO_CONTENT,
    'DELETE': status.HTTP_204_NO_CONTENT
}


def build_reply(retbody={}, retcode=0):
    '''
        build json reply according to retcode and data
    '''
    reply = {
        'retcode': retcode,
        'retbody': retbody
    }
    return reply


def parse_api_repy(reply_json):
    '''
        @param reply_json: reply from api side, should be in following format:
            {'retcode': '', 'retbody': ''}
        @return: api reply in json format
    '''
    reply = ''
    try:
        reply = json.loads(reply_json)
    except Exception as e:
        errmsg = ("api reply<type:%s>: <%s> is not in json format"
                  % (type(reply_json), reply_json))
        logger.error(errmsg)
        logger.exception(e)
        raise exception.InternalServerFailuer(reason=errmsg)
    return reply


def reply_error_to_client(request, retcode, retbody_dict,
                          status=status.HTTP_400_BAD_REQUEST):
    '''
        api reply error message to client
    '''
    reply = build_reply(retbody_dict, retcode)
    response = Response(reply, status)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def reply_success_to_client(request, reply_dict):
    '''
        api reply error message to client
        @type reply: dict
    '''
    status = HTTP_SUCCESS_STATUS[request.method]
    reply = build_reply(reply_dict)
    response = Response(reply, status)

    response['Access-Control-Allow-Origin'] = '*'
    return response


def check_reply_to_client(request, reply_json):
    '''
        check reply(json) from ws and reply to client
    '''
    ret = json.loads(reply_json)

    if ret['retcode'] != 0:
        return reply_error_to_client(request, ret['retcode'], ret['retbody'],
                                     status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return reply_success_to_client(request, ret['retbody'])
