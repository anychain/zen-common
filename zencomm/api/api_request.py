'''
    api request 
'''

import json

from zencomm.api import constants as CONST


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
            @return: whether the api request is valid and the error message send back to client
        '''

        print self.resource
        errmsg = None
        if self.resource not in self.params:
            errmsg = 'Invalid parameters, resource %s not included in api request' % self.resource
        else:
            for rp in self.required_params:
                if rp not in self.params[self.resource]:
                    errmsg = 'Invalid parameters, parameter %s not included in %s api request' % (rp, self.resource)
                    break
        if errmsg:
            return False, errmsg
        else:
            return True, "The api request is valid"

    def to_json(self):
        '''
            convert the request to a json object
        '''
        return json.dumps(self.req)

# 1) user request
class UserCreateReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_CREATE
    required_params = ['passwd', 'phone']

class UserUpdateReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_UPDATE

class UserDeleteReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_DELETE

class UserListReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_LIST

class UserDetailReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_DETAIL
    required_params = ['phone']

class UserResetPasswdReq(APIReq):
    resource = CONST.RESOURCE_USER
    action = CONST.ACTION_USER_RESET_PASSWD

# 2) session request
class SessionCreateReq(APIReq):
    resource = CONST.RESOURCE_SESSION
    action = CONST.ACTION_SESSION_CREATE
    required_params = ['user_id', 'password']

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
    required_params = ['name', 'topic', 'address']

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
    required_params = ['name']

class ChildUpdateReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_UPDATE

class ChildDeleteReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_DELETE

class ChildDetailReq(APIReq):
    resource = CONST.RESOURCE_CHILD
    action = CONST.ACTION_CHILD_DETAIL
    
# 5) family request
class FamilyListReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_LIST
    
class FamilyCreateReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_CREATE
    required_params = ['family_id']

class FamilyUpdateReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_UPDATE

class FamilyDeleteReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_DELETE

class FamilyDetailReq(APIReq):
    resource = CONST.RESOURCE_FAMILY
    action = CONST.ACTION_FAMILY_DETAIL


# 6) branch request
class BranchListReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_LIST

class BranchCreateReq(APIReq):
    resource = CONST.RESOURCE_BRANCH
    action = CONST.ACTION_BRANCH_CREATE
    required_params = ['name', 'type', 'address', 'address_code']

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
    required_params = ['name', 'type', 'address', 'address_code']

class OrganizationUpdateReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_UPDATE

class OrganizationDeleteReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_DELETE

class OrganizationDetailReq(APIReq):
    resource = CONST.RESOURCE_ORGANIZATION
    action = CONST.ACTION_ORGANIZATION_DETAIL

# 8) state request
class StateListReq(APIReq):
    resource = CONST.RESOURCE_STATE
    action = CONST.ACTION_STATE_LIST

class StateCreateReq(APIReq):
    resource = CONST.RESOURCE_STATE
    action = CONST.ACTION_STATE_CREATE
    required_params = ['name', 'description']

class StateUpdateReq(APIReq):
    resource = CONST.RESOURCE_STATE
    action = CONST.ACTION_STATE_UPDATE

class StateDeleteReq(APIReq):
    resource = CONST.RESOURCE_STATE
    action = CONST.ACTION_STATE_DELETE

class StateDetailReq(APIReq):
    resource = CONST.RESOURCE_STATE
    action = CONST.ACTION_STATE_DETAIL


#if __name__ == '__main__':
#    user_create_req = UserCreateReq({'name': 'zen-dev', 'age': '30', 'phone': '1366688888', 'email': 'dev@esse.io'})
#    print user_create_req.to_json()
