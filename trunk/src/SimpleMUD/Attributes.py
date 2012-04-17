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

    def FromLines(self, file):
        for i in range(0, NUMATTRIBUTES):
            line = file.readline()
            name = BasicLibString.ParseName(BasicLibString.ParseWord(line, 0))
            value = BasicLibString.ParseWord(line, 1)
            self.m_attributes[int(GetAttribute(name))] = int(value)
            
    def ToLines(self, string):
        for i in range(0, NUMATTRIBUTES):
            string += BasicLibString.Fill16Char("[" + GetAttributeString(i) + "]") + str(self.m_attributes[i]) + "\n"
        return string
            
    def __repr__(self):
        return self.ToLines("")

'''        
i = AttributeSet()
file0 = open("Attribute.templates", "r")
i.FromLines(file0)
print(file0.readline() + "1111")
print(file0.readline() + "1111")
#print(i)
file0.close()
print(i)
'''

        
ItemType_WEAPON = 0
ItemType_ARMOR = 1
ItemType_HEALING = 2
NUMITEMTYPES = 3

def GetItemTypeString(index):
    if index == ItemType_WEAPON:
        return "WEAPON"
    elif index == ItemType_ARMOR:
        return "ARMOR"
    elif index == ItemType_HEALING:
        return "HEALING"

def GetItemType(p_str):
    if p_str == "WEAPON":
        return ItemType_WEAPON
    elif p_str == "ARMOR":
        return ItemType_ARMOR
    elif p_str == "HEALING":
        return ItemType_HEALING
    
PlayerRank_REGULAR = 0
PlayerRank_GOD = 1
PlayerRank_ADMIN = 2
NUMPLAYERRANKTYPES = 3

def GetRankString(index):
    if index == PlayerRank_REGULAR:
        return "REGULAR"
    elif index == PlayerRank_GOD:
        return "GOD"
    elif index == PlayerRank_ADMIN:
        return "ADMIN"

def GetRank(p_str):
    if p_str == "REGULAR":
        return PlayerRank_REGULAR
    elif p_str == "GOD":
        return PlayerRank_GOD
    elif p_str == "ADMIN":
        return PlayerRank_ADMIN
    
RoomType_PLAINROOM = 0
RoomType_TRAININGROOM = 1
RoomType_STORE = 2
NUMROOMTYPES = 3

def GetRoomTypeString(index):
    if index == RoomType_PLAINROOM:
        return "PLAINROOM"
    elif index == RoomType_TRAININGROOM:
        return "TRAININGROOM"
    elif index == RoomType_STORE:
        return "STORE"

def GetRoomType(p_str):
    if p_str == "PLAINROOM":
        return RoomType_PLAINROOM
    elif p_str == "TRAININGROOM":
        return RoomType_TRAININGROOM
    elif p_str == "STORE":
        return RoomType_STORE
    
Direction_NORTH = 0
Direction_EAST = 1
Direction_SOUTH = 2
Direction_WEST = 3
NUMDIRECTIONS = 4

def OppositeDirection(p_dir):
    return (p_dir + 2) % 4

def GetDirectionString(index):
    if index == Direction_NORTH:
        return "NORTH"
    elif index == Direction_EAST:
        return "EAST"
    elif index == Direction_SOUTH:
        return "SOUTH"
    elif index == Direction_WEST:
        return "WEST"

def GetDirection(p_str):
    if p_str == "NORTH":
        return Direction_NORTH
    elif p_str == "EAST":
        return Direction_EAST
    elif p_str == "SOUTH":
        return Direction_SOUTH
    elif p_str == "WEST":
        return Direction_WEST



