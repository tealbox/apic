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
