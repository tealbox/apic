#-------------------------------------------------------------------------------
# Name:        Apic-Env-Setup
#-------------------------------------------------------------------------------
## Note: only for Python2
## issue with SSL_V3, _ssl.c:510: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure>
# This can;t be resolve in python2 of urllib, but it require higher version of urllib may be 3
# so I downloaded python3 and used for retriving Pyscripter
# no error handling, only for personal use/not commercial 

import os, zipfile
import urllib
path = 'c:\\myTools'

def getPython(url=None):
    if url is None:
        url = "https://www.python.org/ftp/python/3.10.2/python-3.10.2-embed-amd64.zip"
    pfile = "python-3.10.2-embed-amd64.zip"
    os.chdir(path)
    urllib.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()

def getScripter(url=None):
## os.system(''' c:\\mytools\\python.exe -c "import os ; os.system('mkdir ToDo'); " ''')
## 
    if url is None:
        url = "https://sourceforge.net/projects/pyscripter/files/PyScripter-v4.1/PyScripter-4.1.1-x64.zip/download"
    pfile = "pyscripter.zip"
    os.chdir(path)
   
    os.system(''' c:\\mytools\\python.exe -c "import os ; from urllib import request ;  request.urlretrieve( 'https://sourceforge.net/projects/pyscripter/files/PyScripter-v4.1/PyScripter-4.1.1-x64.zip/download','pyscripter.zip'); " ''')
##    urllib.request.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()
    

##https://efotinis.neocities.org/downloads/DeskPins-1.32-setup.exe

def getTopMost(url=None):
    if url is None:
        url = "http://www.nirsoft.net/utils/winlister-x64.zip"
    pfile = "winlister.zip"
    os.chdir(path)
    urllib.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()

def main():
    os.mkdir(path)
    os.chdir(path)
    getPython()
    getScripter()
    getTopMost()
    pass

if __name__ == '__main__':
    main()
