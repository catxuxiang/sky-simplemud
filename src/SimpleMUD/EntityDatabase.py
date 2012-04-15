'''
Created on 2012-4-14

@author: Sky
'''
from Entity import Entity

class EntityDatabase:
    
    def __init__(self):
        self.container = {}
        
    def SetValue(self, p_id, value):
        self.container[p_id] = value
        
    def GetValue(self, p_id):
        for i in self.container.keys():
            if i == p_id:
                return self.container[i]
        return None
    
    def FindFull(self, p_name):
        for i in self.container.values():
            if i.CompName() == p_name.strip().lower():
                return i
        return None
    
    def Find(self, p_name):
        for i in self.container.values():
            if i.CompName().find(p_name.strip().lower(), 0) == 0:
                return i
        return None
    
    def HasId(self, p_id):
        if self.GetValue(p_id) == None:
            return False
        else:
            return True
    
    def HasFull(self, p_name):
        if self.FindFull(p_name) == None:
            return False
        else:
            return True
    
    def Has(self, p_name):
        if self.Has(p_name) == None:
            return False
        else:
            return True
        
    def Size(self):
        return len(self.container)
    
    def FindOpenId(self):
        return len(self.container)
    
    def __iter__(self):
        for i in self.container:
            yield self.container[i]
            
class EntityDatabaseVector:
    def __init__(self):
        self.container = []
        
    def __iter__(self):
        for i in self.container:
            yield i
            
    def Size(self):
        return len(self.container)
    
    def SetValue(self, value):
        self.container[i].append(value)
   
    def GetValue(self, p_id):
        for i in self.container:
            if i.Id() == p_id:
                return i
        return None
            
        
        
        
'''    
i = EntityDatabase()
j = Entity()
i.SetValue("111", j)
k = Entity()
i.SetValue("222", k)
for item in i:
    print(item.Name())
print(i.Size())

k = ["111", "222"]
print(k[0])
k.append("333")
print(k)
del k[0]
print(k)
print(k[0])
'''



