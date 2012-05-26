'''
Created on 2012-4-15

@author: Sky
'''

from SimpleMUD.Entity import Entity
from SimpleMUD.Attributes import *
from BasicLib.BasicLibString import RemoveWord, ParseWord, ParseName

class Item(Entity):
    def __init__(self):
        self.m_type = ItemType_WEAPON
        self.m_min = 0
        self.m_max = 0
        self.m_speed = 0
        self.m_attributes = []
        for _ in range(0, NUMATTRIBUTES):
            self.m_attributes.append(0)          
        
    def GetType(self):
        return self.m_type
    
    def GetAttr(self, p_att):
        return self.m_attributes[p_att]
    
    def GetMin(self):
        return self.m_min
    
    def GetMax(self):
        return self.m_max
    
    def GetSpeed(self):
        return self.m_speed
    
    def GetPrice(self):
        return self.m_price
    
    def FromLines(self, file):
        line = file.readline()
        name = RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        self.m_type = GetItemType(ParseWord(line, 1))
        line = file.readline()
        self.m_min = int(ParseWord(line, 1))
        line = file.readline()
        self.m_max = int(ParseWord(line, 1))
        line = file.readline()
        self.m_speed = int(ParseWord(line, 1))
        line = file.readline()
        self.m_price = int(ParseWord(line, 1))
        #self.m_attributes.FromLines(file)
        for _ in range(0, NUMATTRIBUTES):
            line = file.readline()
            name = ParseName(ParseWord(line, 0))
            value = ParseWord(line, 1)
            self.m_attributes[GetAttribute(name)] = int(value)
        
    def __repr__(self):
        string  = "[NAME]  " + self.m_name + "\n"
        string += "[TYPE]  " + GetItemTypeString(self.m_type) + "\n"
        string += "[MIN]   " + str(self.m_min) + "\n"
        string += "[MAX]   " + str(self.m_max) + "\n"
        string += "[SPEED] " + str(self.m_speed) + "\n"
        string += "[PRICE] " + str(self.m_price) + "\n"
        #return string + str(self.m_attributes)
        for i in range(0, NUMATTRIBUTES):
            string += "[" + GetAttributeString(i) + "] " + str(self.m_attributes[i]) + "\n"
        return string
''' 
a = Item()
file = open("example.itm")
a.FromLines(file)
file.close()
print(a)
'''       
    

    

        

        
        
        