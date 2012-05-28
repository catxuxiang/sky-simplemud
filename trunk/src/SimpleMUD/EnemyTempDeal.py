'''
Created on 2012-5-28

@author: Sky
'''
from BasicLib.BasicLibString import *
from BasicLib.Redis import sr

def FromLines(file, id1):
    line = file.readline()
    name = RemoveWord(line, 0)
    sr.set("EnemyTemplate:" + id1 + ":NAME", name.strip())
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":HITPOINTS", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":ACCURACY", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":DODGING", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":STRIKEDAMAGE", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":DAMAGEABSORB", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":EXPERIENCE", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":WEAPON", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":MONEYMIN", ParseWord(line, 1))
    line = file.readline()
    sr.set("EnemyTemplate:" + id1 + ":MONEYMAX", ParseWord(line, 1))
    
    line = file.readline()
    while sr.spop("EnemyTemplate:" + id1 + ":LOOT") != None:
        pass
    while line.strip() != "[ENDLOOT]":
        id2 = ParseWord(line, 1)
        chance = ParseWord(line, 2)
        sr.sadd("EnemyTemplate:" + id1 + ":LOOT", id2 + " " + chance)
        line = file.readline()
'''
file = open("..\enemies\enemies.templates")
line = file.readline()
sr.ltrim("EnemyTemplateList", 2, 1)
print(sr.llen("EnemyTemplateList"))
while line:
    if line.strip() != "":
        id1 = ParseWord(line, 1)
        sr.rpush("EnemyTemplateList", id1)
        FromLines(file, id1)
    line = file.readline() 
file.close()  
print("Success!")
'''

