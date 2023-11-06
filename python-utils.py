def checkPort(port):
    if isinstance(port, (int,)) and  port in range(0,65535):
        return port
    elif isinstance(port, (int,)) and not port in range(0,65535):
        print(port, " must be int and in range 0,65535, 1")
        return False
    elif isinstance(port, str):
        try:
            port = int(port)
        except ValueError as ve:
            print(port, " must be int and in range 0,65535, 2")
            return False
        except Exception as ex:
            print(port, " must be int and in range 0,65535, 3")
            return False
        return ports
#---------------------------------------------------

import re
def checkPort(port):
    if isinstance(port, (int,)) and  port in range(0,65535):
        return port
    elif isinstance(port, (int,)) and not port in range(0,65535):
        print(port, " must be int and in range 0,65535, 1")
        return False
    elif isinstance(port, str):
        try:
            port = int(port)
        except ValueError as ve:
            print(port, " must be int and in range 0,65535, 2")
            return False
        except Exception as ex:
            print(port, " must be int and in range 0,65535, 3")
            return False
        return port
#---------------------------------------------------
def checkRange(prange):
    # assuming the range does not contain any alphabets.
    # check for those. range must be sting else it will send difference of numbers
    # remove all spaces and check
    if not isinstance(prange, (str,)):
        print("port range must be string of digits")
        return False
    # remove all spaces from string
    prange = re.sub("\s+","", prange)
    if not prange.isdigit() and not "-" in prange:
        print("Port range must be string and contain only digits in x-y" ,prange)
        return False
    # split from - and check indivisual numbers using checkPort
    numbers = prange.split("-")
    if len(numbers) > 2:
        # prange contain multiple hyphens and hence not a valid range
        print("Port range must contain only one hyphen (-) ", prange)
        return False
    a = checkPort(numbers[0])
    if not a:
        return False
    b = checkPort(numbers[1])
    if not b and a>b:
        return False
    return f"{a}-{b}"
