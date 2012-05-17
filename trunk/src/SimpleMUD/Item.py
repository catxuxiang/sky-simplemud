'''
Created on 2012-4-15

@author: Sky
'''

from SimpleMUD.Entity import Entity
from SimpleMUD.Attributes import *
from BasicLib import BasicLibString

class Item(Entity):
    def __init__(self):
        self.m_type = ItemType_WEAPON
        self.m_min = 0
        self.m_max = 0
        self.m_speed = 0
        self.m_attributes = AttributeSet()
        
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
        name = BasicLibString.RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        self.m_type = GetItemType(BasicLibString.ParseWord(line, 1))
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
        string  = BasicLibString.Fill16Char("[NAME]") + self.m_name + "\n"
        string += BasicLibString.Fill16Char("[TYPE]") + GetItemTypeString(self.m_type) + "\n"
        string += BasicLibString.Fill16Char("[MIN]") + self.m_min + "\n"
        string += BasicLibString.Fill16Char("[MAX]") + self.m_max + "\n"
        string += BasicLibString.Fill16Char("[SPEED]") + self.m_speed + "\n"
        string += BasicLibString.Fill16Char("[PRICE]") + self.m_price + "\n"
        return string + str(self.m_attributes)
''' 
a = Item()
file = open("example.itm")
a.FromLines(file)
file.close()
print(a)
'''       
    

    

        

        
        
        