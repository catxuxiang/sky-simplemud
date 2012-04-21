'''
Created on 2012-4-15

@author: Sky
'''

from Entity import Entity
from BasicLib import BasicLibString
from Room import Room

class EnemyTemplate(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_hitpoints = 0
        self.m_accuracy = 0
        self.m_dodging = 0
        self.m_strikedamage = 0
        self.m_damageabsorb = 0
        self.m_experience = 0
        self.m_weapon = 0
        self.m_moneymin = 0
        self.m_moneymax = 0
        
    def FromLines(self, file):
        line = file.readline()
        name = BasicLibString.RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        self.m_hitpoints = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_accuracy = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_dodging = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_strikedamage = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_damageabsorb = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_experience = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_weapon = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_moneymin = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_moneymax = BasicLibString.ParseWord(line, 1)
        
        self.m_loot = []
        line = file.readline()
        while line.strip() != "[ENDLOOT]":
            id1 = BasicLibString.ParseWord(line, 1)
            chance = BasicLibString.ParseWord(line, 2)
            self.m_loot.append([id1, chance])
            line = file.readline()
        return file
    
    def ToLines(self, string):
        string += BasicLibString.Fill16Char("[ID]") + self.m_id + "\n"
        string += BasicLibString.Fill16Char("[NAME]") + self.m_name + "\n"
        string += BasicLibString.Fill16Char("[HITPOINTS]") + self.m_hitpoints + "\n"
        string += BasicLibString.Fill16Char("[ACCURACY]") + self.m_accuracy + "\n"
        string += BasicLibString.Fill16Char("[DODGING]") + self.m_dodging + "\n"
        string += BasicLibString.Fill16Char("[STRIKEDAMAGE]") + self.m_strikedamage + "\n"
        string += BasicLibString.Fill16Char("[DAMAGEABSORB]") + self.m_damageabsorb + "\n"
        string += BasicLibString.Fill16Char("[EXPERIENCE]") + self.m_experience + "\n"
        string += BasicLibString.Fill16Char("[WEAPON]") + self.m_weapon + "\n"
        string += BasicLibString.Fill16Char("[MONEYMIN]") + self.m_moneymin + "\n"
        string += BasicLibString.Fill16Char("[MONEYMAX]") + self.m_moneymax + "\n"        
        for i in self.m_loot:
            string += BasicLibString.Fill16Char("[LOOT]") + i[0] + "  " + i[1] + "\n" 
        return string
    
    def __repr__(self):
        return self.ToLines("")
        
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
        
    def Name(self):
        return self.m_template.Name()
    
    def Accuracy(self):
        return self.m_template.m_accuracy
    
    def Dodging(self):
        return self.m_template.m_dodging
    
    def StrikeDamage(self):
        return self.m_template.m_strikedamage
    
    def DamageAbsorb(self):
        return self.m_template.m_damageabsorb
    
    def Experience(self):
        return self.m_template.m_experience
    
    def Weapon(self):
        return self.m_template.m_weapon
    
    def MoneyMin(self):
        return self.m_template.m_moneymin
    
    def MoneyMax(self):
        return self.m_template.m_moneymax
    
    def LootList(self):
        return self.m_template.m_loot
    
    def FromLines(self, file):
        line = file.readline()
        self.m_template = EnemyTemplate()
        self.m_template.SetId(BasicLibString.ParseWord(line, 1))
        #print(self.m_template.GetId())
        line = file.readline()
        self.m_hitpoints = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        room = Room()
        room.SetId(BasicLibString.ParseWord(line, 1))
        self.m_room = room
        line = file.readline()
        #print(line)
        self.m_nextattacktime = BasicLibString.ParseWord(line, 1)
        return file
    
    def ToLines(self):
        string = BasicLibString.Fill16Char("[TEMPLATEID]") + str(self.m_template.GetId()) + "\n"
        string += BasicLibString.Fill16Char("[HITPOINTS]") + str(self.m_hitpoints) + "\n"
        string += BasicLibString.Fill16Char("[ROOM]") + str(self.m_room.GetId()) + "\n"
        string += BasicLibString.Fill16Char("[NEXTATTACKTIME]") + " " + str(self.m_nextattacktime) + "\n"
        return string
    
    def __repr__(self):
        return self.ToLines("")

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
        
   
    
