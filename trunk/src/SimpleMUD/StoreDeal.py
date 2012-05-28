'''
Created on 2012-5-28

@author: Sky
'''
from BasicLib.BasicLibString import ParseWord, RemoveWord
from BasicLib.Redis import sr

def FromLines(file, id1):
    line = file.readline()
    sr.set("Store:" + id1 + ":NAME", RemoveWord(line, 0).strip())         
    line = file.readline()
    sr.set("Store:" + id1 + ":Items", RemoveWord(line, 0).strip())     
'''            
file = open("../stores/stores.str")
line = file.readline()
while line:
    if line.strip() != "":
        id1 = ParseWord(line, 1)
        sr.rpush("StoreList", id1)
        FromLines(file, id1)
    line = file.readline() 
file.close()
print("Success")
'''
