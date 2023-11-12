#-------------------------------------------------------------------------------
# Name:        module2, Created: 2023-11-11
#-------------------------------------------------------------------------------
import re
from myNSX4 import *
from pprint import pprint
def getAPI(self, api=""):
    res = self._myNSX__do(method="GET", api=api)
    return res

myNSX.getAPI = getAPI

def get_sp_all(self):
    api = f"/infra/domains/default/security-policies"
    res = self.getAPI(api=api)
    if "results" in res:
        self.sp_all = {item["display_name"]: item for item in res["results"]}
    return self.sp_all
myNSX.get_sp_all = get_sp_all

def get_sp_detail(self, spid=None):
    api = f"/infra/domains/default/security-policies/{spid}"
    res = self.getAPI(api=api)
    if "rules" in res:
        self.sp_all_rules = {item["display_name"]: item for item in res["rules"]}
        return self.sp_all_rules
    else:
        None
myNSX.get_sp_detail = get_sp_detail

def create_sp_rule(self, spID=None, ruleName="", sGrp =[], dGrp=[], service=[], scope=[], action="Allow"):
    _ruleName = toUnderscore(ruleName)
    sGrpID = []
    for item in sGrp:
        (status, temp) = self.checkGRP(item)
        if status:
            sGrpID.append(temp)
        else:
            print(f"{item} is not found!!")
    ### DEST Groups
    dGrpID = []
    for item in dGrp:
        (status, temp) = self.checkGRP(item)
        if status:
            dGrpID.append(temp)
        else:
            print(f"{item} is not found!!")
    scopes = []
    for item in scope:
        (status, temp) = self.checkGRP(item)
        if status:
            scopes.append(temp)
        else:
            print(f"{item} is not found!!")

    payload =  self.getRulePayload(spID, sGrpID, dGrpID, service, action, scopes, ruleName)
    payload=json.dumps(payload)
    api = f"/infra/domains/default/security-policies/{spID}/rules/{_ruleName}"
    print(f"Rule Payload: {payload}")
    self._myNSX__do(method="PUT", api=api, payload=payload)

myNSX.create_sp_rule = create_sp_rule

def addSgrp2Rule():
    pass
def addDgrp2Rule():
    pass
def addScope2Rule():
    pass
def addService2Rule():
    pass
def removeService2Rule():
    pass
def removeSgrp2Rule():
    pass
def removeDgrp2Rule():
    pass
def removeScope2Rule():
    pass



def main():
    nx = myNSX(nsxmgr="192.168.1.36")
    nx.getGroups()
##    res = nx.getAPI(api="/infra/domains/default/security-policies")
    sp = nx.get_sp_all()

##    print(sp)
    spName = "TST_RSAM - UAT"
    if spName in sp:
        pprint(sp[spName])
    else:
        print(f"SP {spName} not found please check name again !!")
    pass

    # check rules in the SP
    rules = nx.get_sp_detail(spid=sp[spName]['id'])
    print(rules)
    nx.create_sp_rule(sp[spName]['id'], ruleName="CA_To_RSAM - UAT", sGrp =["ANY"], dGrp=["sg_TST_RSAM - UAT"], service=["/infra/services/HTTPS"], scope=["sg_TST_RSAM - UAT"], action="Allow" )


if __name__ == '__main__':
    main()
