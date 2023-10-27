import requests, json
import requests.packages
from typing import List, Dict
from pprint import pprint

# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings()

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
      'Authorization': 'Basic YWRtaW46Vk13YXJlMSFWTXdhcmUxIQ=='
    }
    self.baseUrl = f"https://{self.hostname }/policy/api/v1"
    self.getallServices()

  def __do(self, method="GET", api="", payload={}):
    url = f"{self.baseUrl}{api}"
    if method == "GET":
      response = self.s.get(url, headers = self.headers)
      if response.status_code >= 200 and response.status_code <= 299:
        return response.json()
    if method == "POST":
      response = self.s.post(url, data = payload, headers = self.headers)
      if response.status_code >= 200 and response.status_code <= 299:
        return response.json()
    if method == "PUT":
      response = self.s.put(url, data = payload, headers = self.headers)
      if response.status_code >= 200 and response.status_code <= 299:
        return response.json()
    if method == "DELETE":
      response = self.s.delete(url, data = payload, headers = self.headers)
      if response.status_code >= 200 and response.status_code <= 299:
        return "Deleted Successfully"
      else:
        return "Error in Deletion"

  def getServices(self):
    api = '/infra/services'
    res = self.__do(method="GET", api=api, payload={})
    if "results" in res:
      self.allservices =  res['results']
      return self.allservices

    #service['service_entries'][0]['unique_id'], service['id'], service['display_name'], service['service_entries'][0]['path'], service['service_entries'][0]['l4_protocol'], service['service_entries'][0]['destination_ports']
    #('41e12a74-7888-4982-af7e-d6d7a33466e8',
     #'AD_Server',
     #'AD Server',
     #'/infra/services/AD_Server/service-entries/AD_Server',
     #'TCP',
     #['1024'])


  def getallServices(self):
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
      print(f"All Rules are disabled now for Security Policy {securityID}")
      return True
    

def main():
  a =  myNSX(nsxmgr="192.168.1.26")
  #services = a.getServices()
  #for service in  services:
    #print(service['id'], service['display_name'], service['id'], service['id'], service['id'], service['id'], )
  #servicesDB = a.getallServices()
  print("_"*180)
  # pprint(servicesDB)
  #(name, proto, port) = ("myHttp", "TCP", 4567)
  #a.createService(name, proto, port)
  #print("Delete Server: yes/no: ")
  #ans = input()
  #if ans.upper() == "YES" or   ans.upper() == "Y":
    #a.deleteService(name)
  
  a.readSecurityPolicy("AD_NTP_SERVER")
  a.disableRules("AD_NTP_SERVER", rules="all")
if __name__ == "__main__":
  main()