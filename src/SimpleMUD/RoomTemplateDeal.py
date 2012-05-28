'''
Created on 2012-5-28

@author: Sky
'''
from BasicLib.BasicLibString import ParseWord, RemoveWord
from SimpleMUD.Attributes import *
from BasicLib.Redis import sr

def LoadTemplate(file, id1):
    line = file.readline()
    name = RemoveWord(line, 0)
    sr.set("RoomTemplate:" + id1 + ":NAME", name.strip())
    line = file.readline()
    description = RemoveWord(line, 0)
    sr.set("RoomTemplate:" + id1 + ":DESCRIPTION", description.strip())
    line = file.readline()
    sr.set("RoomTemplate:" + id1 + ":TYPE", ParseWord(line, 1))
    line = file.readline()
    sr.set("RoomTemplate:" + id1 + ":DATA", ParseWord(line, 1))
    
    for d in range(0, NUMDIRECTIONS):
        line = file.readline()
        sr.set("RoomTemplate:" + id1 + ":" + GetDirectionString(d), ParseWord(line, 1))
    
    line = file.readline()
    sr.set("RoomTemplate:" + id1 + ":ENEMY", ParseWord(line, 1))
    line = file.readline()
    sr.set("RoomTemplate:" + id1 + ":MAXENEMIES", ParseWord(line, 1))
'''        
file = open("../maps/default.map")
line = file.readline()
while line:
    if line.strip() != "":
        id1 = ParseWord(line, 1)
        sr.rpush("RoomTemplateList", id1)
        LoadTemplate(file, id1)
    line = file.readline() 
file.close()
print("Success")
'''
