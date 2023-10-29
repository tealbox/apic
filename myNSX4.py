import requests, json, re
import requests.packages
from typing import List, Dict
from pprint import pprint
# from casUtils import *

# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings()
def toUnderscore(s):
    pat = """\s|\W"""
    s = re.sub(pat,'_',s)
    return s
def removeSpecialChar(s):
    # will remove all special characters
    # all alphabets, so remining will be
    # numbers and comma and hyphen not working for -(hyphen)
    pat = """(?!,)\W|\s|[A-Za-z]"""
    s = re.sub(pat,'',s)
    return s

class myNSX:
    # create for the ops of NSX4 tasks
    # required requests
    def __init__(self, nsxmgr, username = "admin", password = ""):
        self.s = requests.Session()
        self.hostname = nsxmgr
        self.username = username
        self.password = password
        self.s.verify = False
        self.headers = {
          'Accept-Encoding': 'gzip',
          'Content-Type': "application/json",
          'Accept': 'application/json',
          # 'Authorization': "Basic dnBhbmthajpCbHVlYmVycnkjMTQyMjA="
          'Authorization': 'Basic YWRtaW46Vk13YXJlMSFWTXdhcmUxIQ=='
        }
        self.baseUrl = f"https://{self.hostname }/policy/api/v1"
        # self.getallServices()
        self.spPrefix = 'TST_'
        self.grpPrefix = 'sg_TST_'
        self.svcPrefix = 'svc_TCP_' # svc_UDP_

    def __do(self, method="GET", api="", payload={}):
        url = f"{self.baseUrl}{api}"
        if method == "GET":
          response = self.s.get(url, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
          else:
            return "Not able to GET api, please check for login/ip/credentials!!"
        if method == "POST":
          response = self.s.post(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
        if method == "PUT":
          response = self.s.put(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
        if method == "PATCH":
          response = self.s.patch(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            # print(response.content)
            return "Success" # .json()
          else:
            return "Error in PATCHing %s"%url
        if method == "DELETE":
          response = self.s.delete(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return "Deleted Successfully"
          else:
            return "Error in Deletion"

    def getServices(self):
        api = "/infra/services"

        res = self.__do(method="GET", api=api, payload={})
        if "results" in res:
          self.allservices =  res['results']
          self.svcDB = self.allservices
          return self.allservices
        else:
            return None

        #service['service_entries'][0]['unique_id'], service['id'], service['display_name'], service['service_entries'][0]['path'], service['service_entries'][0]['l4_protocol'], service['service_entries'][0]['destination_ports']
        #('41e12a74-7888-4982-af7e-d6d7a33466e8',
         #'AD_Server',
         #'AD Server',
         #'/infra/services/AD_Server/service-entries/AD_Server',
         #'TCP',
         #['1024'])


    def getallServices(self):
        print("-*-"*25)
        print("Collecting All Services ...")
        self.getServices()
        self.servicesDB = {}
        for service in self.allservices:
          temprec =  {
            # 'id': service['id'],
            'unique_id': service['service_entries'][0]['unique_id'],
            'display_name': service['display_name'],
            'path': service['service_entries'][0]['path']
            }
          if 'l4_protocol' in  service['service_entries'][0]:
            temprec.setdefault('l4_protocol', service['service_entries'][0]['l4_protocol'])
            temprec.setdefault('destination_ports', service['service_entries'][0]['destination_ports'])
          elif "protocol" in service['service_entries'][0]:
            temprec.setdefault('protocol', service['service_entries'][0]["protocol"])
            # temprec.setdefault('destination_ports', service['service_entries'][0]['destination_ports'])
          elif "alg" in  service['service_entries'][0]:
            temprec.setdefault('alg', service['service_entries'][0]["alg"])
            temprec.setdefault('destination_ports', service['service_entries'][0]['destination_ports'])
          else:
            temprec.setdefault('NOTFOUND', service['service_entries'][0])
            # temprec.setdefault('destination_ports', service['service_entries'][0]['destination_ports'])
          # self.servicesDB.setdefault(service['service_entries'][0]['unique_id'], temprec)
          self.servicesDB.setdefault(service['id'], temprec)
        return self.servicesDB

    def servicePayload(self, name, proto, port ):
        a = json.dumps( {
        "is_default": True,
        "service_entries": [
            {
                "l4_protocol": proto,
                "source_ports": [],
                "destination_ports": [
                    port,
                ],
                "resource_type": "L4PortSetServiceEntry",
                "id": name,
                "display_name": name,
                "relative_path": name,
                "remote_path": "",
                "marked_for_delete": False,
                "overridden": False,
            }
        ],
        "service_type": "NON_ETHER",
        "resource_type": "Service",
        "id": name,
        "display_name": name,
        "description": name,
        })
        return a

    def createService(self, name, proto, port):
        # check for existing services
        if name in self.servicesDB:
            print(f"{name} Service already exist ignoring...")
            return None
        payload = self.servicePayload(name, proto, port)
        # print(payload)
        api = f"/infra/services/{name}"
        w = self.__do(method="PUT", api=api, payload=payload)
        if 'id' in w and name == w['id']:
            print("Created Service {name}")
            return name
        # print(w)

    def deleteService(self, name):
        api = f"/infra/services/{name}"
        w = self.__do(method="DELETE", api=api)
        print(w)

    def readSecurityPolicy(self, securityID):
        api = f'/infra/domains/default/security-policies/{securityID}'
        w = self.__do(api=api)
        return w

    def disableRules(self, securityID, rules=None):
        #Read Security Policy and rules
        w =  self.readSecurityPolicy(securityID)
        # check if rules are already disabled.
        disabled = 0
        for rule in w['rules']:
          if rule['disabled'] == True:
            print(f"Rule {rule['id']} is already disabled in Security Policy {securityID}")
            rule['disabled'] = True
            disabled = 1
        if disabled and rules != "all":
          return None
        api = f'/infra/domains/default/security-policies/{securityID}'
        for rule in w['rules']:
          rule['disabled'] = True
        w = json.dumps(w)
        # print(w)
        w = self.__do(method="PUT", api=api, payload=w)
        if "rules" in w:
          print(f"All Rules are disabled now for c Policy {securityID}")
          return True

##    def getGroups(self):
##        print("-*-"*25)
##        print("Collecting All Groups ...")
##        api = "/infra/domains/default/groups"
##        # are are securityID
##        w = self.__do(method="GET", api=api)
##        self.grpDB = {}
##        if "results" in w:
##            # collect only name, id, and path
##            # Note::::: Group name are case sensitive
##            w = w["results"]
##            for g in w:
##                self.grpDB.setdefault(g['display_name'], {g['id'], g['path']})
##        # print(w)
##        return self.grpDB

    def getGroups(self):
        print("-*-"*25)
        print("Collecting All Groups ...")
        api = "/infra/domains/default/groups"
        # are are securityID
        w = self.__do(method="GET", api=api)
        self.grpDB = {}
        if "results" in w:
            # collect only name, id, and path
            # Note::::: Group name are case sensitive
            self.grpDB = w["results"]
            return self.grpDB
        else:
            return None

    def getSecurityPolicies(self):
        print("-*-"*25)
        print("Collecting All Security Policies ...")
        api = "/infra/domains/default/security-policies"
        w = self.__do(method="GET", api=api)
        if "results" in w:
            self.spDB = w['results']
            self.allSpDB = {}
            return self.spDB

    def checkSP(self, spName):
        spName = spName.strip()
        # check if SPName contin prefix else it will be a group name
        # if grp name remove grpPrefix

        if self.grpPrefix in spName:
            # remove grp prefix and add SP prefix
            spName = re.sub(f'^{self.grpPrefix}', "", spName)
            spName = f"TST_{spName}"
        elif self.spPrefix != spName[0:4]:
            # not a valid SP Name
            spName = f"TST_{spName}"
        else:
            # this is valid SP name now check
            pass
        # print(self.spDB)
        if self.spDB:
            for item in self.spDB:
                # print(item['display_name'], spName)
                if spName == item['display_name']:
                    return (True, item['id'])
        return (False, None)


    def checkGRP(self, grpName):
        grpName = grpName.strip()
        # check if grpName contin prefix else it will be a Normal name
        # if grp name remove grpPrefix
        if self.grpPrefix != grpName[0:7]:
            # not a valid SP Name
            grpName = f"sg_TST_{grpName}"
        else:
            # this is valid SP name now check
            pass
        # print(self.spDB)
        if self.grpDB:
            for item in self.grpDB:
                # print(item['display_name'])
                if grpName == item['display_name']:
                    return (True, item['path'])
        return (False, None)

    def checkSERVICE(self, proto="TCP", portNum=0):
        proto = proto.strip()
        # service can be custom
        customSVC = 0
        # Assuming that only portnumber are given for query
        # check if svcName contin prefix else it will be a Normal name
        # if grp name remove grpPrefix
        # check if range
        if isinstance(portNum, (str)) and "-" in portNum:
            # remove all spaces
            portNum = re.sub("\s+","",portNum)
            pass
        if proto == 'UDP':
            grpPrefix = "svc_UDP_"
        else:
            grpPrefix = "svc_TCP_"
        svc = f"{grpPrefix}{portNum}"
        if self.svcDB:
            for item in self.svcDB:
                # print(item['display_name'])
                if svc == item['display_name']:
                    return (True, item['path'])
                svcItem = item['service_entries'][0]
                # print([str(portNum),], )
                if 'l4_protocol' in svcItem and 'destination_ports' in svcItem and svcItem['destination_ports'] == [str(portNum),] and svcItem['l4_protocol'] == proto:
                    return (True, item['path'])
            customSVC = 1
        return (False, None)

    def getSP(self, spName):
        # assuing spName already exist in the database
        api = f"/infra/domains/default/security-policies/{spName}"
        w = self.__do(method="GET", api=api)
        if "id" in w:
            return w
        else:
            return None

    def getSecurityPoliciesandRules(self):
        pass

    def createSecurityPolicy(self,spName, payload ={}):
        api = f"/infra/domains/default/security-policies/{spName}"
        w = self.__do(method="PATCH", api=api, payload=payload)
        print(w)
##        if 'id' in w and spName == w['id']:
##            print("Created SP {spName}")
##            return name

    def getGroupPayload(self, grpName, _grpName, ):
        return { \
            "expression": [ \
                { \
                    "member_type": "VirtualMachine", \
                    "key": "OSName",\
                    "operator": "EQUALS",\
                    "value": "RHEL",\
                    "resource_type": "Condition" \
                } \
            ],\
            "extended_expression": [], \
            "reference": False, \
            "resource_type": "Group",\
            "id": _grpName,\
            "display_name": grpName\
        }

    def createGroup(self, grpName, expression=""):
        # remove space
        grpName = grpName.strip()
        _grpName = toUnderscore(grpName)
        # add prefix only if it doesn;t exist
        if not self.grpPrefix in grpName and not "sg_INFRA_" in grpName and not "sg_PRD_" in grpName:
            grpName = self.grpPrefix + grpName
            _grpName = self.grpPrefix + _grpName
        api = f'/infra/domains/default/groups/{_grpName}'
        payload = self.getGroupPayload(grpName,_grpName)
        # print(payload, api)
        payload=json.dumps(payload)
        w = self.__do(method="PATCH", api=api, payload=payload)
        return w
    def deleteGroup(self, grpName, expression=""):
        # remove space
        grpName = grpName.strip()
        api = f'/infra/domains/default/groups/{grpName}'
        w = self.__do(method="DELETE", api=api)
        return w




        pass


  # def createRule(spName: str, sGrp: list, dGrp: list, services: list, action: str, scope: list, ruleName: str)
    def getRulePayload(self, spName: str, sGrp: list, dGrp: list, services: list, action: str, scope: list, ruleName: str):
        # replace space and all special characters with _ underscore
        _ruleName = toUnderscore(ruleName)
        return \
        {\
                "action": "ALLOW",\
                "resource_type": "Rule",\
                "id": f"{ruleName}",\
                "display_name": f"{_ruleName}",\
                "path": f"/infra/domains/default/security-policies/{spName}/rules/{_ruleName}",\
                "relative_path": f"{_ruleName}",\
                "parent_path": f"/infra/domains/default/security-policies/{spName}",\
                "marked_for_delete": False,\
                "overridden": False,\
                "sources_excluded": False,\
                "destinations_excluded": False,\
                "source_groups": sGrp,\
                "destination_groups": dGrp,\
                "services": services,\
                "profiles": [ "ANY" ],\
                "logged": False,\
                "scope": scope,\
                "disabled": True,\
                "notes": "",\
                "direction": "IN_OUT",\
                "tag": "",\
                "disabled": False,\
                "ip_protocol": "IPV4_IPV6",\
                "is_default": False\
            }
    def createRule(self, spName: str, sGrp: list =["Any",] , dGrp: list =["ANY",], services: dict ={"TCP": [0,]} , action: str ="Allow", scope: list =["ANY",], ruleName: str ="Rule_CAS") -> None:
        # spName must be searchable so must be SP ID
        api = f"/infra/domains/default/security-policies/{spName}"
        (status, spID) = self.checkSP(spName)
        ### SRC Groups
        sGrpName = sGrp[0]
        dGrpName = dGrp[0]
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

        ### Services
        # services = {'TCP': [1,2,3,4,5]}
        if "TCP" in services:
            proto = "TCP"
        elif "UDP" in services:
            proto = "UDP"
        service = []
        if isinstance(services[proto], (list,)):
            portNums = services[proto]
            for item in portNums:
                (status, temp) = self.checkSERVICE(proto=proto,portNum=item)
                if status:
                    service.append(temp)
                else:
                    print(f"{item} is not found!!")


        scopes = []
        for item in scope:
            (status, temp) = self.checkGRP(item)
            if status:
                scopes.append(temp)
            else:
                print(f"{item} is not found!!")

        rulePayload =  self.getRulePayload(spID, sGrpID, dGrpID, service, action, scopes, ruleName)
        # pprint(rulePayload)


        sp = self.readSecurityPolicy(spID)
        sp['rules'].append(rulePayload)
        print("-"*90)
        pprint(sp)
        payload=json.dumps(sp)
        print(self.createSecurityPolicy(spID,payload=payload))


def main():
    a =  myNSX(nsxmgr="192.168.1.26")
    services = a.getServices()
    #for service in  services:
    #print(service['id'], service['display_name'], service['id'], service['id'], service['id'], service['id'], )

    print("-"*80)
    # pprint(servicesDB)
    #(name, proto, port) = ("myHttp", "TCP", 4567)
    #a.createService(name, proto, port)
    #print("Delete Server: yes/no: ")
    #ans = input()
    #if ans.upper() == "YES" or   ans.upper() == "Y":
    #a.deleteService(name)

    a.readSecurityPolicy("TST_Active Directory - Development")

    #a.disableRules("AD_NTP_SERVER", rules="")

    # a.createService("svc_TCP_5600-5601","TCP",  "5600-5601")

    # check for SP if exist: sg_TST_IdentityIQ - Development
    # get name by removing sg_TST_ remove prefix of grpname
    # grpPrefix = "sg_TST_"
    # SP Prefix = "TST_"
    # Service Prefix = svcPrefix = svc_TCP/UDP_
    # get DB for service/grps/sp
    svcDB = a.getallServices()
    spDB = a.getSecurityPolicies()
    grpDB = a.getGroups()
    spName = "   IdentityIQ - Development   "
    spName = spName.strip()
    (status, spID) = a.checkSP(spName)
    print(status, spID)
    sp = a.getSP(spID)
    print(sp)
    # now check for all groups used for rule creation
    grpName = "Vocera Voice - Test"
    print(a.checkGRP(grpName))


    print(a.checkSERVICE(proto="TCP",portNum=443))
    spName = "TST_INFRA_CyberArk"
    sGrp = ["IdentityIQ - Development", "sg_TST_Microsoft PKI - Development"]
    dGrp = ["IdentityIQ - Development", "sg_TST_Microsoft PKI - Development"]
    services = {'TCP':  [443, 7890]}
    action = "Allow"
    scope = ["sg_TST_Microsoft PKI - Development"]
    ruleName = "HelloCAS20"
    a.createRule(spName, sGrp, dGrp, services, action, scope, ruleName)
    # a.createGroup(" sg_TST_Imprivata OneSign - Test")










if __name__ == "__main__":
    main()