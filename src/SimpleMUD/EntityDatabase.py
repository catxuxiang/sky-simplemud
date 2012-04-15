'''
Created on 2012-4-14

@author: Sky
'''
from Entity import Entity

class EntityDatabase:
    container = {}
    index = 0
        
    @staticmethod    
    def SetValue(p_id, value):
        EntityDatabase.container[p_id] = value
        
    @staticmethod    
    def GetValue(p_id):
        for i in EntityDatabase.container.keys():
            if i == p_id:
                return EntityDatabase.container[i]
        return None
    
    @staticmethod
    def FindFull(p_name):
        for i in EntityDatabase.container.values():
            if i.CompName() == p_name.strip().lower():
                return i
        return None
    
    @staticmethod
    def Find(p_name):
        for i in EntityDatabase.container.values():
            if i.CompName().find(p_name.strip().lower(), 0) == 0:
                return i
        return None
    
    @staticmethod
    def HasId(p_id):
        if EntityDatabase.GetValue(p_id) == None:
            return False
        else:
            return True
    
    @staticmethod        
    def HasFull(p_name):
        if EntityDatabase.FindFull(p_name) == None:
            return False
        else:
            return True
    
    @staticmethod      
    def Has(p_name):
        if EntityDatabase.Has(p_name) == None:
            return False
        else:
            return True
        
    @staticmethod     
    def Size():
        return len(EntityDatabase.container)
    
    @staticmethod 
    def FindOpenId():
        return len(EntityDatabase.container)
    
    @staticmethod
    def __iter__():
        EntityDatabase.index = 0
        return EntityDatabase.container
    
    @staticmethod
    def next():
        if EntityDatabase.index < len(EntityDatabase.container):
            obj = list(EntityDatabase.container.values())[EntityDatabase.index]
            EntityDatabase.index += 1
            return obj
        else:
            raise StopIteration 


    
#class EntityDatabaseVector:
    

j = Entity()
EntityDatabase.SetValue("111", j)
k = Entity()
EntityDatabase.SetValue("222", k)
for i in EntityDatabase:
    print(i)
print(EntityDatabase.Size())

k = ["111", "222"]
print(k[0])
k.append("333")
print(k)
del k[0]
print(k)
print(k[0])



