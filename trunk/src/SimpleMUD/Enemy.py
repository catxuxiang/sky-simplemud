'''
Created on 2012-4-15

@author: Sky
'''

from SimpleMUD.Entity import Entity
from BasicLib.BasicLibString import *

class EnemyTemplate(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_hitpoints = 0
        self.m_accuracy = 0
        self.m_dodging = 0
        self.m_strikedamage = 0
        self.m_damageabsorb = 0
        self.m_experience = 0
        self.m_weapon = None
        self.m_moneymin = 0
        self.m_moneymax = 0
        
    def FromLines(self, file):
        line = file.readline()
        name = RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        self.m_hitpoints = int(ParseWord(line, 1))
        line = file.readline()
        self.m_accuracy = int(ParseWord(line, 1))
        line = file.readline()
        self.m_dodging = int(ParseWord(line, 1))
        line = file.readline()
        self.m_strikedamage = int(ParseWord(line, 1))
        line = file.readline()
        self.m_damageabsorb = int(ParseWord(line, 1))
        line = file.readline()
        self.m_experience = int(ParseWord(line, 1))
        line = file.readline()
        self.m_weapon = ParseWord(line, 1)
        line = file.readline()
        self.m_moneymin = int(ParseWord(line, 1))
        line = file.readline()
        self.m_moneymax = int(ParseWord(line, 1))
        
        self.m_loot = {}
        line = file.readline()
        while line.strip() != "[ENDLOOT]":
            id1 = ParseWord(line, 1)
            chance = ParseWord(line, 2)
            self.m_loot[id1] = int(chance)
            line = file.readline()
        return file
    
    def ToLines(self):
        string  = "[ID]           " + self.m_id + "\n"
        string += "[NAME]         " + self.m_name + "\n"
        string += "[HITPOINTS]    " + str(self.m_hitpoints) + "\n"
        string += "[ACCURACY]     " + str(self.m_accuracy) + "\n"
        string += "[DODGING]      " + str(self.m_dodging) + "\n"
        string += "[STRIKEDAMAGE] " + str(self.m_strikedamage) + "\n"
        string += "[DAMAGEABSORB] " + str(self.m_damageabsorb) + "\n"
        string += "[EXPERIENCE]   " + str(self.m_experience) + "\n"
        string += "[WEAPON]       " + self.m_weapon.GetId() + "\n"
        string += "[MONEYMIN]     " + str(self.m_moneymin) + "\n"
        string += "[MONEYMAX]     " + str(self.m_moneymax) + "\n"        
        for i in self.m_loot:
            string += "[LOOT]     " + i + "  " + str(self.m_loot[i]) + "\n" 
        return string
    
    def __repr__(self):
        return self.ToLines()
        
class Enemy(Entity):   
    def __init__(self):
        self.m_template = None
        self.m_hitpoints = 0
        self.m_room = None
        self.m_nextattacktime = 0

    def LoadTemplate(self, p_template):
        self.m_template = p_template
        self.m_hitpoints = p_template.m_hitpoints
        
    def GetHitPoints(self):
        return self.m_hitpoints
    
    def SetHitPoints(self, m_hitpoints):
        self.m_hitpoints = m_hitpoints
        
    def GetCurrentRoom(self):
        return self.m_room
    
    def SetCurrentRoom(self, m_room):
        self.m_room = m_room    
    
    def GetNextAttackTime(self):
        return self.m_nextattacktime  
    
    def SetNextAttackTime(self, m_nextattacktime):
        self.m_nextattacktime = m_nextattacktime              
        
    def GetName(self):
        return self.m_template.GetName()
    
    def GetAccuracy(self):
        return self.m_template.m_accuracy
    
    def GetDodging(self):
        return self.m_template.m_dodging
    
    def GetStrikeDamage(self):
        return self.m_template.m_strikedamage
    
    def GetDamageAbsorb(self):
        return self.m_template.m_damageabsorb
    
    def GetExperience(self):
        return self.m_template.m_experience
    
    def GetWeapon(self):
        return self.m_template.m_weapon
    
    def GetMoneyMin(self):
        return self.m_template.m_moneymin
    
    def GetMoneyMax(self):
        return self.m_template.m_moneymax
    
    def GetLootList(self):
        return self.m_template.m_loot
    
    def FromLines(self, file):
        line = file.readline()
        self.m_template = ParseWord(line, 1)
        #print(self.m_template.GetId())
        line = file.readline()
        self.m_hitpoints = int(ParseWord(line, 1))
        line = file.readline()
        self.m_room = ParseWord(line, 1)
        line = file.readline()
        #print(line)
        self.m_nextattacktime = int(ParseWord(line, 1))
        return file
    
    def ToLines(self):
        string  = "[TEMPLATEID]     " + self.m_template.GetId() + "\n"
        string += "[HITPOINTS]      " + str(self.m_hitpoints) + "\n"
        string += "[ROOM]           " + self.m_room.GetId() + "\n"
        string += "[NEXTATTACKTIME] " + str(self.m_nextattacktime) + "\n"
        return string
    
    def __repr__(self):
        return self.ToLines()

'''    
file = open("enemies.templates")
i = EnemyTemplate()
file.readline()
i.FromLines(file)
file.close()
j = Enemy()
j.LoadTemplate(i)
print(j)
'''  
        
   
    
