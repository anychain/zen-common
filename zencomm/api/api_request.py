# -*- coding: utf-8 -*-

#
# Licensed Materials - Property of esse.io
#
# (C) Copyright esse.io. 2015 All Rights Reserved
#
# Author: frank (frank@esse.io)
#
#


import json

from zencomm.api import constants as CONST
from zencomm.log import log as logging
LOG = logging.getLogger(__name__)


class APIReq():
    """Base zen api request
    """
    resource = ''
    action = ''
    required_params = []

    def __init__(self, params={}):
        '''
            init request with resource, action, params
            @param param: parameters needed by the request
            @type params: dict
        '''
        self.params = params
        self.req = {
            'resource': self.resource,
            'action': self.action,
            'params': self.params
        }

    def verify_api_request(self):
        '''
            verify params got from api request is correct
            @return: whether the api request is valid and
                     the error message send back to client
        '''

        print self.resource
        errmsg = None
        if self.resource not in self.params:
            errmsg = ('Invalid parameters, resource %s not included'
                      'in api request') % self.resource
        else:
            for rp in self.required_params:
                if rp not in self.params[self.resource]:
                    errmsg = ('Invalid parameters, parameter %s not '
                              'included in %s api request') % (rp,
                                                               self.resource)
                    break
        if errmsg:
            LOG.error("Api request validation failed with error %s"
                      % errmsg)
            return False, errmsg
        else:
            return True, "The api request is valid"

    def to_json(self):
        '''
            convert the request to a json object
        '''
        return json.dumps(self.req)


# 1) family request
class FamilyCreateReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_CREATE
    required_params = ['passwd', 'phone']


class FamilyUpdateReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_UPDATE
    required_params = ['id']


class FamilyDeleteReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_DELETE


class FamilyListReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_LIST


class FamilyDetailReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_DETAIL
    required_params = ['id']


class FamilyResetPasswdReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_RESET_PASSWD


class FamilyChildList(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_CHILD_LIST


class FamilyAttendActivityList(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_ATTEND_ACTIVITY_LIST


# 2) session request
class SessionCreateReq(APIReq):
    resource = CONST.RESOURCE_SESSION
    action = CONST.ACTION_SESSION_CREATE
    required_params = ['family_id', 'password']


class SessionDeleteReq(APIReq):
    resource = CONST.RESOURCE_SESSION
    action = CONST.ACTION_SESSION_DELETE


class SessionRenewReq(APIReq):
    resource = CONST.RESOURCE_SESSION
    action = CONST.ACTION_SESSION_RENEW


# 3) activity request
class ActivityCreateReq(APIReq):
    resource = CONST.RESOURCE_ACTIVITY
    action = CONST.ACTION_ACTIVITY_CREATE
    required_params = ['name', 'begin_time', 'end_time', 'addrcode',
                       'address', 'size',
                       'type', 'subject', 'content', 'poster']


class ActivityUpdateReq(APIReq):
    resource = CONST.RESOURCE_ACTIVITY
    action = CONST.ACTION_ACTIVITY_UPDATE


class ActivityDeleteReq(APIReq):
    resource = CONST.RESOURCE_ACTIVITY
    action = CONST.ACTION_ACTIVITY_DELETE


class ActivityListReq(APIReq):
    resource = CONST.RESOURCE_ACTIVITY
    action = CONST.ACTION_ACTIVITY_LIST


class ActivityDetailReq(APIReq):
    resource = CONST.RESOURCE_ACTIVITY
    action = CONST.ACTION_ACTIVITY_DETAIL


# 4) child request
class ChildListReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_LIST


class ChildCreateReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_CREATE
    required_params = ['name', 'birthday']


class ChildUpdateReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_UPDATE


class ChildDeleteReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_DELETE


class ChildDetailReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_DETAIL


# 6) branch request
class BranchListReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_LIST


class BranchCreateReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_CREATE
    required_params = ['name', 'type', 'address', 'county']


class BranchUpdateReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_UPDATE


class BranchDeleteReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_DELETE


class BranchDetailReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_DETAIL


# 7) organization request
class OrganizationListReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_LIST


class OrganizationCreateReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_CREATE


class OrganizationUpdateReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_UPDATE


class OrganizationDeleteReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_DELETE


class OrganizationDetailReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_DETAIL


class OrganizationAdminListReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_ADMIN_LIST


class OrganizationAdminAddReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_ADMIN_ADD


class OrganizationAdminDeleteReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_ADMIN_DELETE


class OrganizationActivityListReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_ACTIVITY_LIST


class OrganizationAdminSearchReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_ADMIN_SEARCH


# 8) state request
class DatadictListReq(APIReq):
    resource = CONST.RESOURCE_DATADICT
    action = CONST.ACTION_DATADICT_LIST


class DatadictCreateReq(APIReq):
    resource = CONST.RESOURCE_DATADICT
    action = CONST.ACTION_DATADICT_CREATE
    required_params = ['name', 'type']


class DatadictUpdateReq(APIReq):
    resource = CONST.RESOURCE_DATADICT
    action = CONST.ACTION_DATADICT_UPDATE


class DatadictDeleteReq(APIReq):
    resource = CONST.RESOURCE_DATADICT
    action = CONST.ACTION_DATADICT_DELETE


class DatadictDetailReq(APIReq):
    resource = CONST.RESOURCE_DATADICT
    action = CONST.ACTION_DATADICT_DETAIL


# 8) Address code  request
class AddrcodeListReq(APIReq):
    resource = CONST.RESOURCE_ADDRCODE
    action = CONST.ACTION_ADDRCODE_LIST


class AddrcodeCreateReq(APIReq):
    resource = CONST.RESOURCE_ADDRCODE
    action = CONST.ACTION_ADDRCODE_CREATE
    required_params = ['code', 'address']


class AddrcodeUpdateReq(APIReq):
    resource = CONST.RESOURCE_ADDRCODE
    action = CONST.ACTION_ADDRCODE_UPDATE


class AddrcodeDeleteReq(APIReq):
    resource = CONST.RESOURCE_ADDRCODE
    action = CONST.ACTION_ADDRCODE_DELETE


class AddrcodeDetailReq(APIReq):
    resource = CONST.RESOURCE_ADDRCODE
    action = CONST.ACTION_ADDRCODE_DETAIL


# 9) admin request
class AdminCreateReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_CREATE
    required_params = ['passwd', 'phone']


class AdminUpdateReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_UPDATE
    required_params = ['id']


class AdminDeleteReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_DELETE


class AdminListReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_LIST


class AdminDetailReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_DETAIL
    required_params = ['id']


class AdminResetPasswdReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_RESET_PASSWD


class AdminOrganizationListReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_ORGANIZATION_LIST


class AdminBranchListReq(APIReq):
    resource = CONST.RESOURCE_ADMIN
    action = CONST.ACTION_ADMIN_BRANCH_LIST


# 10) news request
class NewsCreateReq(APIReq):
    resource = CONST.RESOURCE_NEWS
    action = CONST.ACTION_NEWS_CREATE
    required_params = ['name', 'summary', 'content', 'poster']


class NewsUpdateReq(APIReq):
    resource = CONST.RESOURCE_NEWS
    action = CONST.ACTION_NEWS_UPDATE


class NewsDeleteReq(APIReq):
    resource = CONST.RESOURCE_NEWS
    action = CONST.ACTION_NEWS_DELETE


class NewsListReq(APIReq):
    resource = CONST.RESOURCE_NEWS
    action = CONST.ACTION_NEWS_LIST


class NewsDetailReq(APIReq):
    resource = CONST.RESOURCE_NEWS
    action = CONST.ACTION_NEWS_DETAIL


# 11) carousel request
class CarouselCreateReq(APIReq):
    resource = CONST.RESOURCE_CAROUSEL
    action = CONST.ACTION_CAROUSEL_CREATE
    required_params = ['object_type', 'object_id', 'name', 'poster']


class CarouselDeleteReq(APIReq):
    resource = CONST.RESOURCE_CAROUSEL
    action = CONST.ACTION_CAROUSEL_DELETE


class CarouselListReq(APIReq):
    resource = CONST.RESOURCE_CAROUSEL
    action = CONST.ACTION_CAROUSEL_LIST
