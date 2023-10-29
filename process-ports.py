#-------------------------------------------------------------------------------
# Name:        module2, Created: 2023-10-27
#-------------------------------------------------------------------------------
import myXLS
from myNSX4 import *
from time import sleep
import re
# SSGrp    DSGrp    Protocol    Ports    Destination IP Address    Source IP Address    GrpNames

def xxx():
    xl = "C:\\cas\\pankaj-nsx-thr\\ALL-FILTER-RULES.xlsx"
    d = myXLS.fast_openpyxl(xl)
    d = d[1]['sheet_All-Filter-rules']
##    print(d)
    pat = r"\[.*?\]|\s+" # re.sub("\[.*?\]|\s+","",r)
    xlallPorts = []
    for row in d:
        if isinstance(row['Ports'], (str)):
            t1 = re.sub(pat, "", row['Ports'])
            if "," in t1:
                t1 = t1.split(",")
            print(re.sub(pat, "", row['Ports']))
        else:
            t1 = re.sub(pat, "", str(row['Ports']))
            print("ELSE", t1)
            if "," in t1:
                t1 = t1.split(",")
        if isinstance(t1, (list)):
            for item in t1:
                xlallPorts.append(item)
        else:
            xlallPorts.append(t1)
        # xlallPorts+=t1
    # Remove duplicates:
    xlallPorts= list(dict.fromkeys(xlallPorts))
    print(xlallPorts)
    pass
def main():
    xl = "C:\\cas\\pankaj-nsx-thr\\ALL-FILTER-RULES.xlsx"
    d = myXLS.fast_openpyxl(xl)
    d = d[1]['sheet_All-Filter-rules']
    # print(d)
    nx = myNSX(nsxmgr="192.168.1.26")
    svcDB = nx.getallServices()
    spDB = nx.getSecurityPolicies()
    grpDB = nx.getGroups()
    for row in d:
        if "," in row['SSGrp']:
            glist = row['SSGrp'].split(",")
            for grp in glist:
                print(grp, "creating ")
                grpdata = nx.createGroup(grp)
                sleep(1)
    print(nx.checkGRP("sg_TST_IBM Resilient - Test"))
    nx.createGroup("sg_TST_IdentityIQ - UAT")

##    allgrps = nx.getGroups()
##    for g in allgrps:
##        nx.deleteGroup(g['id'])

if __name__ == '__main__':
    main()
