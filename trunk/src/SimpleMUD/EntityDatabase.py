'''
Created on 2012-4-14

@author: Sky
'''
from Entity import Entity

class EntityDatabase:
    def __init__(self):
        self.container = {}
        
    def SetValue(self, id, value):
        self.container[id] = value
        
    def GetValue(self, id):
        for i in self.container.keys():
            if i == id:
                return self.container[i]
        return None
    
    def FindFull(self, name):
        for i in self.container.values():
            if i.CompName() == name.strip().lower():
                return i
        return None
    
    def Find(self, name):
        for i in self.container.values():
            if i.CompName().find(name.strip().lower(), 0) == 0:
                return i
        return None
    

i = EntityDatabase()
j = Entity()
i.SetValue("111", j)
print(i.GetValue("1121"))