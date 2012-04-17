'''
Created on 2012-4-15

@author: Sky
'''

from Entity import Entity
import Attributes
from BasicLib import BasicLibString

class Item(Entity):
    def __init__(self):
        self.m_type = Attributes.ItemType_WEAPON
        self.m_min = 0
        self.m_max = 0
        self.m_speed = 0
        self.m_attributes = Attributes.AttributeSet()
        
    def Type(self):
        return self.m_type
    
    def GetAttr(self, p_att):
        return self.m_attributes[p_att]
    
    def Min(self):
        return self.m_min
    
    def Max(self):
        return self.m_max
    
    def Speed(self):
        return self.m_speed
    
    def Price(self):
        return self.m_price
    
    def FromLines(self, file):
        line = file.readline()
        name = BasicLibString.ParseName(BasicLibString.ParseWord(line, 0))
        self.m_name = line.replace("[" + name + "]", "").strip()
        line = file.readline()
        self.m_type = Attributes.GetItemType(BasicLibString.ParseWord(line, 1))
        line = file.readline()
        self.m_min = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_max = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_speed = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_price = BasicLibString.ParseWord(line, 1)
        self.m_attributes.FromLines(file)
        
    def __repr__(self):
        string  = "[NAME]\t" + self.m_name + "\n"
        string += "[TYPE]\t" + Attributes.GetItemTypeString(self.m_type) + "\n"
        string += "[MIN]\t" + self.m_min + "\n"
        string += "[MAX]\t" + self.m_max + "\n"
        string += "[SPEED]\t" + self.m_speed + "\n"
        string += "[PRICE]\t" + self.m_price + "\n"
        return string + str(self.m_attributes)
    
a = Item()
file = open("example.itm")
a.FromLines(file)
file.close()
print(a)
           
    

    

        

        
        
        