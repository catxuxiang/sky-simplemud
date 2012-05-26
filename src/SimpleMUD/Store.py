'''
Created on 2012-4-21

@author: Sky
'''
from SimpleMUD.Entity import Entity
from BasicLib.BasicLibString import RemoveWord

class Store(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_items = []
        
    def Find(self, p_name):
        for i in self.m_items:
            if i.MatchFull(p_name):
                return i
            
        for i in self.m_items:
            if i.Match(p_name):
                return i
            
        return None        

    def Has(self, p_item):
        for i in self.m_items:
            if i.GetId() == p_item.GetId():
                return True
        return False
    
    def FromLines(self, file):
        line = file.readline()
        self.SetName(RemoveWord(line, 0).strip())          
        line = file.readline()
        itemids = RemoveWord(line, 0).strip()
        for i in itemids.split(' '):
            if i != "0":
                self.m_items.append(i)
                
'''                
file = open("Store.instances")
file.readline()
i = Store()
i.FromLines(file)
'''