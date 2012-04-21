'''
Created on 2012-4-21

@author: Sky
'''
from Entity import Entity
from Item import Item
from BasicLib import BasicLibString

class Store(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_items = []
        
    def Find(self, p_item):
        for i in self.m_items:
            if i.MatchFull(p_item):
                return i
            
        for i in self.m_items:
            if i.Match(p_item):
                return i
            
        return None        

    def Has(self, p_item):
        for i in self.m_items:
            if i.GetId() == p_item.GetId():
                return True
        return False
    
    def FromLines(self, file):
        line = file.readline()
        self.SetName(BasicLibString.RemoveWord(line, 0).strip())          
        line = file.readline()
        itemids = BasicLibString.RemoveWord(line, 0).strip()
        for i in itemids.split(' '):
            if i != "0":
                item = Item()
                item.SetId(i)
                #print(i)
                self.m_items.append(item)
                
'''                
file = open("Store.instances")
file.readline()
i = Store()
i.FromLines(file)
'''