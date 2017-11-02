import hashlib
import os
import ctypes
from collections import defaultdict

kdll = ctypes.windll.LoadLibrary("kernel32.dll")

def filehasher(filepath):
    BLKSIZE = 65536
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buffer = f.read(BLKSIZE)
        while buffer:
            hasher.update(buffer)
            buffer = f.read(BLKSIZE)
    return hasher.digest()

if __name__ == "__main__":
    currentpath = os.getcwd()
    fdct = {}
    for root, dirs, files in os.walk(currentpath):
        for f in files:
            path = os.path.join(root,f)
            #print(path)
            hval = filehasher(path)
            if fdct.get(hval) == None:
                fdct[hval] = path
            else:
                print(path," is Duplicated")
                os.remove(path)
                kdll.CreateHardLinkW(path, fdct[hval], 0)
    #print(fdct)