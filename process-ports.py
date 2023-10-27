#-------------------------------------------------------------------------------
# Name:        module2, Created: 2023-10-27
#-------------------------------------------------------------------------------
import myXLS
import re
def main():
    xl = "C:\\cas\\pankaj-nsx-thr\\tst_rules.xlsx"
    d = myXLS.fast_openpyxl(xl)
    d = d[1]['sheet_Rules-Test']
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

if __name__ == '__main__':
    main()
