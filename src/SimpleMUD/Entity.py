'''
Created on 2012-4-14

@author: Sky
'''

class Entity:
    def __init__(self):
        self.m_name = "UNDEFINED"
        self.m_id = 0
        
    def Name(self):
        return self.m_name
    
    def CompName(self):
        return self.m_name.lower()
    
    def MatchFull(self, p_str):
        return self.CompName() == p_str.lower()
    
    def Match(self, p_str):
        if len(p_str) == 0:
            return True
        
        name = self.CompName()
        search = p_str.lower()
        index = name.find(search, 0) 
        
        if index == 0:
            return True
        else:
            return False
        
    def Id(self):
        return self.m_id

'''    
i = Entity()
print(i.Match("unDEF")) 
'''     
    
    
