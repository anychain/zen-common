# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#


def get_resource_from_action(action):
    '''
        action: in format RESOURCE_OPERATION, like
            family_update
    '''
    resource = action.split('_')[0].lower()
    return resource
