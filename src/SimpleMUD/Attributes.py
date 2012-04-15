'''
Created on 2012-4-15

@author: Sky
'''
from BasicLib import BasicLibString

Attribute_STRENGTH = 0
Attribute_HEALTH = 1
Attribute_AGILITY = 2
Attribute_MAXHITPOINTS = 3
Attribute_ACCURACY = 4
Attribute_DODGING = 5
Attribute_STRIKEDAMAGE = 6
Attribute_DAMAGEABSORB = 7
Attribute_HPREGEN = 8
NUMATTRIBUTES = 9

def GetAttributeString(index):
    if index == Attribute_STRENGTH:
        return "STRENGTH"
    elif index == Attribute_HEALTH:
        return "HEALTH"
    elif index == Attribute_AGILITY:
        return "AGILITY"
    elif index == Attribute_MAXHITPOINTS:
        return "MAXHITPOINTS"
    elif index == Attribute_ACCURACY:
        return "ACCURACY"
    elif index == Attribute_DODGING:
        return "DODGING"
    elif index == Attribute_STRIKEDAMAGE:
        return "STRIKEDAMAGE"
    elif index == Attribute_DAMAGEABSORB:
        return "DAMAGEABSORB"
    elif index == Attribute_HPREGEN:
        return "HPREGEN"            

def GetAttribute(p_str):
    if p_str == "STRENGTH":
        return Attribute_STRENGTH
    elif p_str == "HEALTH":
        return Attribute_HEALTH
    elif p_str == "AGILITY":
        return Attribute_AGILITY
    elif p_str == "MAXHITPOINTS":
        return Attribute_MAXHITPOINTS
    elif p_str == "ACCURACY":
        return Attribute_ACCURACY
    elif p_str == "DODGING":
        return Attribute_DODGING
    elif p_str == "STRIKEDAMAGE":
        return Attribute_STRIKEDAMAGE
    elif p_str == "DAMAGEABSORB":
        return Attribute_DAMAGEABSORB
    elif p_str == "HPREGEN":
        return Attribute_HPREGEN  
    
class AttributeSet:
    def __init__(self):
        self.m_attributes = []
        for i in range(0, NUMATTRIBUTES):
            self.m_attributes.append(0)

    def GetValue(self, p_attr):
        return self.m_attributes[p_attr]

    def FromLines(self, lines):
        for i in lines:
            name = BasicLibString.ParseName(BasicLibString.ParseWord(i, 0))
            value = BasicLibString.ParseWord(i, 1)
            self.m_attributes[int(GetAttribute(name))] = int(value)
            
    def __repr__(self):
        string = ""
        for i in range(0, len(self.m_attributes)):
            string += GetAttributeString(i) + ":" + str(self.m_attributes[i]) + "\n"
        return string
            
i = AttributeSet()
file0 = open("Attribute.templates", "r")
lines = file0.readlines()  
i.FromLines(lines)
print(i)
file0.close()

        


WEAPON = 0
ARMOR = 1
HEALING = 2

def GetItemTypeString(index):
    if index == WEAPON:
        return "WEAPON"
    elif index == ARMOR:
        return "ARMOR"
    elif index == HEALING:
        return "HEALING"

def GetItemType(p_str):
    if p_str == "WEAPON":
        return WEAPON
    elif p_str == "ARMOR":
        return ARMOR
    elif p_str == "HEALING":
        return HEALING
