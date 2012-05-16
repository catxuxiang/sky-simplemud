'''
Created on 2012-4-25

@author: sky
'''
from SimpleMUD.Attributes import *
from SimpleMUD.Entity import Entity
from SimpleMUD.Item import Item
from BasicLib.BasicLibLogger import ERRORLOG
from SocketLib.Telnet import *

PLAYERITEMS = 16

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_pass = "UNDEFINED"
        self.m_rank = PlayerRank_REGULAR
        
        self.m_connection = None
        self.m_loggedin = False
        self.m_active = False
        self.m_newbie = True
        
        self.m_experience = 0
        self.m_level = 1
        self.m_room = 1
        self.m_money = 0
        
        self.m_nextattacktime = 0
        
        self.m_baseattributes[Attribute_STRENGTH] = 1
        self.m_baseattributes[Attribute_HEALTH] = 1
        self.m_baseattributes[Attribute_AGILITY] = 1
        
        self.m_items = 0
        self.m_weapon = -1
        self.m_armor = -1
        
        self.m_statpoints = 18
        
        self.RecalculateStats()
        self.m_hitpoints = self.GetAttr(Attribute_MAXHITPOINTS)
        
        self.m_inventory = []
             
    def Level(self):
        return self.m_level
    
    def HitPoints(self):
        return self.m_hitpoints
    
    def GetStatPoints(self):
        return self.m_statpoints
    
    def SetStatPoints(self, m_statpoints):
        self.m_statpoints = m_statpoints
        
    def GetExperience(self):
        return self.m_experience
    
    def SetExperience(self, m_experience):
        self.m_experience = m_experience
        
    def GetCurrentRoom(self):
        return self.m_room
    
    def SetCurrentRoom(self, m_room):
        self.m_room = m_room
        
    def GetMoney(self):
        return self.m_money
    
    def SetMoney(self, m_money):
        self.m_money = m_money
        
    def GetNextAttackTime(self):
        return self.m_nextattacktime
    
    def SetNextAttackTime(self, m_nextattacktime):
        self.m_nextattacktime = m_nextattacktime
        
    def GetItem(self, p_index):
        return self.m_inventory[p_index]
    
    def GetItems(self):
        return self.m_items
    
    def GetMaxItems(self):
        return PLAYERITEMS
    
    def GetPassword(self):
        return self.m_pass
    
    def SetPassword(self, m_pass):
        self.m_pass = m_pass
        
    def GetRank(self):
        return self.m_rank
    
    def SetRank(self, m_rank):
        self.m_rank = m_rank
        
    def GetConn(self):
        return self.m_connection
    
    def SetConn(self, m_connection):
        self.m_connection = m_connection
        
    def GetLoggedIn(self):
        return self.m_loggedin
    
    def SetLoggedIn(self, m_loggedin):
        self.m_loggedin = m_loggedin
        
    def GetActive(self):
        return self.m_active
    
    def SetActive(self, m_active):
        self.m_active = m_active
        
    def GetNewbie(self):
        return self.m_newbie
    
    def SetNewbie(self, m_newbie):
        self.m_newbie = m_newbie
        
    def NeedForLevel(self, p_level):
        return int(100 * (1.4**(p_level - 1)) - 1)
    
    def GetAttr(self, p_attr):
        val = self.m_attributes[p_attr] + self.m_baseattributes[p_attr]
        if p_attr == Attribute_STRENGTH or p_attr == Attribute_AGILITY or p_attr == Attribute_HEALTH:
            if val < 1:
                return 1
        return val
    
    def GetBaseAttr(self, p_attr):
        return self.m_baseattributes[p_attr]
    
    def GetWeapon(self):
        if self.m_weapon == -1:
            return None
        else:
            return self.m_inventory[self.m_weapon] #return item id
        
    def GetArmor(self):
        if self.m_armor == -1:
            return None
        else:
            return self.m_inventory[self.m_armor] #return item id
        
    def NeedForNextLevel(self):
        return self.NeedForLevel(self.m_level + 1) - self.m_experience
    
    def Train(self):
        if self.NeedForNextLevel() <= 0:
            self.m_statpoints += 2
            self.m_baseattributes[Attribute_MAXHITPOINTS] += self.m_level
            self.m_level += 1
            self.RecalculateStats()
            return True
        else:
            return False
        
    def RecalculateStats(self):
        self.m_attributes[Attribute_MAXHITPOINTS] = 10 + (int(self.m_level * (self.GetAttr(Attribute_HEALTH) / 1.5)))
        self.m_attributes[Attribute_HPREGEN] = self.GetAttr(Attribute_HEALTH) / 5 + self.m_level
        
        self.m_attributes[Attribute_ACCURACY] = self.GetAttr(Attribute_AGILITY) * 3
        self.m_attributes[Attribute_DODGING] = self.GetAttr(Attribute_AGILITY) * 3
        self.m_attributes[Attribute_DAMAGEABSORB] = self.GetAttr(Attribute_STRENGTH) / 5
        self.m_attributes[Attribute_STRIKEDAMAGE] = self.GetAttr(Attribute_STRENGTH) / 5
        
        if self.m_hitpoints > self.GetAttr(Attribute_MAXHITPOINTS):
            self.m_hitpoints = self.GetAttr(Attribute_MAXHITPOINTS)
            
        if self.GetWeapon() != 0:
            self.AddDynamicBonuses(self.GetWeapon())
        if self.GetArmor() != 0:
            self.AddDynamicBonuses(self.GetArmor())
            
    def AddDynamicBonuses(self, p_item):
        if p_item == 0:
            return
        
        i = Item()
        i.SetId(p_item) #perhaps error
        
        for x in range(0, NUMATTRIBUTES):
            self.m_attributes[x] += i.GetAttr( x )
            
    def SetBaseAttr(self, p_attr, p_val):
        self.m_baseattributes[p_attr] = p_val
        self.RecalculateStats()

    def AddToBaseAttr(self, p_attr, p_val):
        self.m_baseattributes[p_attr] += p_val
        self.RecalculateStats()
        
    def AddHitpoints(self, p_hitpoints):
        self.SetHitpoints(self.m_hitpoints + p_hitpoints)
        
    def SetHitpoints(self, p_hitpoints):
        self.m_hitpoints = p_hitpoints
        
        if self.m_hitpoints < 0:
            self.m_hitpoints = 0
        if self.m_hitpoints > self.GetAttr(Attribute_MAXHITPOINTS):
            self.m_hitpoints = self.GetAttr(Attribute_MAXHITPOINTS)
            
    def PickUpItem(self, p_item):
        if len(self.m_items) < self.GetMaxItems():
            #find the first open index to put the item in.
            self.m_items.append(p_item)
            return True
        else:
            return False
        
    def DropItem(self, p_index):
        if self.m_inventory[p_index] != 0:
            #remove the weapon or armor if needed
            if self.m_weapon == p_index:
                self.RemoveWeapon()
            if self.m_armor == p_index:
                self.RemoveArmor()
                
            del self.m_inventory[p_index]
            return True
        else:
            return False
        
    def AddBonuses(self, p_item):
        if p_item == 0:
            return
        
        itm = Item()
        itm.SetId(p_item) #perhaps error
        
        for x in range(0, NUMATTRIBUTES):
            self.m_baseattributes[x] += itm.GetAttr(x)
        self.RecalculateStats()
        
    def RemoveWeapon(self):
        self.m_weapon = -1
        self.RecalculateStats()
        
    def RemoveArmor(self):
        self.m_armor = -1
        self.RecalculateStats()
        
    def UseWeapon(self, p_index):
        self.RemoveWeapon()
        self.m_weapon = p_index
        self.RecalculateStats()
        
    def UseArmor(self, p_index):
        self.RemoveArmor()
        self.m_armor = p_index
        self.RecalculateStats()
        
    def GetItemIndex(self, p_name):
        for i in range(0, len(self.m_inventory)):
            if i.MatchFull(p_name):
                return i.GetId()
            
        for i in range(0, len(self.m_inventory)):
            if i.Match(p_name):
                return i.GetId()
            
        return -1
            
    def SendString(self, p_string):
        if self.GetClient() == None:
            ERRORLOG.Log("Trying to send string to player " + self.GetName() + " but player is not connected.")
            return
        
        self.GetClient().send(p_string + newline)
        
        if self.GetActive():
            self.PrintStatbar()
            
    def PrintStatbar(self, p_update):
        if p_update:# origin:client.Buffered() > 0
            return
        
        statbar = white + bold + "["
        
        ratio = 100 * self.HitPoints() / self.GetAttr(Attribute_MAXHITPOINTS)

        #color code your hitpoints so that they are red if low,
        #yellow if medium, and green if high.
        if ratio < 33:
            statbar += red
        elif ratio < 67:
            statbar += yellow
        else:
            statbar += green
            
        statbar += self.HitPoints() + white + "/" + self.GetAttr(Attribute_MAXHITPOINTS) + "] "
        self.GetClient().send(clearline + "\r" + statbar + reset)
        
    def ToLines(self):
        string = ""
        string += "[NAME]           " + self.m_name + "\n"
        string += "[PASS]           " + self.m_pass + "\n"
        string += "[RANK]           " + GetRankString(self.m_rank) + "\n"
        string += "[STATPOINTS]     " + self.m_statpoints + "\n"
        string += "[EXPERIENCE]     " + self.m_experience + "\n"
        string += "[LEVEL]          " + self.m_level + "\n"
        string += "[ROOM]           " + self.m_room + "\n"
        string += "[MONEY]          " + self.m_money + "\n"
        string += "[HITPOINTS]      " + self.m_hitpoints + "\n"
        string += "[NEXTATTACKTIME] " + self.m_nextattacktime + "\n"
        
        string += self.m_baseattributes.ToLines()
        
        string += "[INVENTORY]      "
        
        for i in range(0, len(self.m_inventory)):
            string += self.m_inventory[i].GetId() + " "
        string += "\n"
        
        string += "[WEAPON]         " + self.m_weapon + "\n"
        string += "[ARMOR]          " + self.m_armor + "\n"
        
        return string 
    
    def FromLines(self, file):
        line = file.readline()
        name = BasicLibString.RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        self.m_pass = BasicLibString.ParseWord(line, 1)        
        line = file.readline()
        self.m_rank = GetRank(BasicLibString.ParseWord(line, 1))
        line = file.readline()
        self.m_statpoints = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_experience = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_level = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_room = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_money = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_hitpoints = BasicLibString.ParseWord(line, 1) 
        line = file.readline()
        self.m_nextattacktime = BasicLibString.ParseWord(line, 1) 
        
        self.m_baseattributes.FromLines(file)
        
        line = file.readline()
        items = BasicLibString.RemoveWord(line, 0).strip().split(" ")
        self.m_items = []
        for i in items:
            if i != 0:
                item = Item()
                item.SetId(i)
                self.m_items.append(item)
                
        line = file.readline()
        self.m_weapon = BasicLibString.ParseWord(line, 1)    
        line = file.readline()
        self.m_armor = BasicLibString.ParseWord(line, 1)  
                
        self.RecalculateStats()

   
    
