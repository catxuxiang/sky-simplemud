'''
Created on 2012-5-28

@author: Sky
'''
from BasicLib.BasicLibString import RemoveWord, ParseWord, ParseName
from BasicLib.Redis import sr
from SimpleMUD.Attributes import *

def FromLines(file, id1):
    line = file.readline()
    name = RemoveWord(line, 0)
    sr.set("Item:" + id1 + ":NAME", name.strip())
    line = file.readline()
    sr.set("Item:" + id1 + ":TYPE", ParseWord(line, 1))
    line = file.readline()
    sr.set("Item:" + id1 + ":MIN", ParseWord(line, 1))
    line = file.readline()
    sr.set("Item:" + id1 + ":MAX", ParseWord(line, 1))
    line = file.readline()
    sr.set("Item:" + id1 + ":SPEED", ParseWord(line, 1))
    line = file.readline()
    sr.set("Item:" + id1 + ":PRICE", ParseWord(line, 1))
    #self.m_attributes.FromLines(file)
    for _ in range(0, NUMATTRIBUTES):
        line = file.readline()
        name = ParseName(ParseWord(line, 0))
        value = ParseWord(line, 1)
        sr.set("Item:" + id1 + ":" + name, value)
'''            
file = open("../items/items.itm")
line = file.readline()
while line:
    if line.strip() != "":
        id1 = ParseWord(line, 1)
        sr.rpush("ItemList", id1)
        FromLines(file, id1)
    line = file.readline() 
file.close()  
print("Success!")
'''
