'''
Created on 2012-4-14

@author: Sky
'''
class EntityDatabase:
    def __init__(self):
        self.m_map = {}
        
    def SetValue(self, p_id, value):
        self.m_map[p_id] = value
        
    def GetValue(self, p_id):
        for i in self.m_map.keys():
            if i == p_id:
                return self.m_map[i]
        return None
    
    def FindFull(self, p_name):
        for i in self.m_map.values():
            if i.CompName() == p_name.strip().lower():
                return i
        return None
    
    def Find(self, p_name):
        for i in self.m_map.values():
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
        if self.Find(p_name) == None:
            return False
        else:
            return True
        
    def Size(self):
        return len(self.m_map)
    
    def FindOpenId(self):
        return len(self.m_map) + 1
    
    def __iter__(self):
        for i in self.m_map:
            yield self.m_map[i]
            
class EntityDatabaseVector:
    def __init__(self):
        self.m_vector = []
        
    def __iter__(self):
        for i in self.m_vector:
            yield i
            
    def Size(self):
        return len(self.m_vector)
    
    def SetValue(self, value):
        self.m_vector.append(value)
   
    def GetValue(self, p_id):
        for i in self.m_vector:
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
    print(item.GetName())
print(i.Size())
'''



