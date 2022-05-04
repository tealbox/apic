#-------------------------------------------------------------------------------
# Name:        Apic-Env-Setup
#-------------------------------------------------------------------------------
## 
## issue with SSL_V3, 

import os, zipfile
import urllib.request
path = 'c:\\myTools'

def getPython(url=None):
    if url is None:
        url = "https://www.python.org/ftp/python/3.10.2/python-3.10.2-embed-amd64.zip"
    pfile = "python-3.10.2-embed-amd64.zip"
    os.chdir(path)
    urllib.request.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()

def getScripter(url=None):
##    os.system(''' c:\\mytools\\python.exe -c "import os ; os.system('mkdir TiTi'); " ''')
    if url is None:
        url = "https://sourceforge.net/projects/pyscripter/files/PyScripter-v4.1/PyScripter-4.1.1-x64.zip/download"
    pfile = "PyScripter-4.1.1-x64.zip"
    os.chdir(path)
    cmd = '''
    c:\\mytools\\python.exe -c "import os ; from urllib import request; os.chdir("c:\\mytools"); urllib.request.urlretrieve({},{} ); "
    '''.format(url,pfile)
    os.system(cmd)
##    urllib.request.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()
    

##https://efotinis.neocities.org/downloads/DeskPins-1.32-setup.exe

def getTopMost(url=None):
    if url is None:
        url = "http://www.nirsoft.net/utils/winlister-x64.zip"
    pfile = "winlister.zip"
    os.chdir(path)
    urllib.request.urlretrieve(url,pfile)
    zip_file = zipfile.ZipFile(pfile)
    zip_file.extractall()

def main():
##    os.mkdir(path)
    os.chdir(path)
##    getPython()
##    getScripter()
    getTopMost()
    pass

if __name__ == '__main__':
    main()
