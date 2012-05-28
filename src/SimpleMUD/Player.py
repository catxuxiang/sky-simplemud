'''
Created on 2012-4-25

@author: sky
'''
from SimpleMUD.Attributes import *
from SimpleMUD.Entity import Entity
from BasicLib.BasicLibLogger import ERRORLOG
from SocketLib.Telnet import *
from BasicLib.BasicLibString import ParseWord, RemoveWord, ParseName

PLAYERITEMS = 16

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_pass = "UNDEFINED"
        self.m_rank = PlayerRank_REGULAR
        
        self.m_connection = None
        self.m_loggedin = False
        self.m_active = False
        self.m_newbie = False
        
        self.m_experience = 0
        self.m_level = 1
        self.m_room = "1"
        self.m_money = 0
        
        self.m_nextattacktime = 0
        
        self.m_attributes = []
        for _ in range(0, NUMATTRIBUTES):
            self.m_attributes.append(0)          
        self.m_baseattributes = []
        for _ in range(0, NUMATTRIBUTES):
            self.m_baseattributes.append(0)        
        self.m_baseattributes[Attribute_STRENGTH] = 1
        self.m_baseattributes[Attribute_HEALTH] = 1
        self.m_baseattributes[Attribute_AGILITY] = 1
        
        self.m_inventory = []        
        self.m_weapon = -1
        self.m_armor = -1
        
        self.m_statpoints = 18
        
        self.m_hitpoints = 0
        self.RecalculateStats()
        self.m_hitpoints = int(self.GetAttr(Attribute_MAXHITPOINTS))
        
        
             
    def GetLevel(self):
        return self.m_level
    
    def GetHitPoints(self):
        return int(self.m_hitpoints)
    
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
        if p_index >= len(self.m_inventory):
            return None
        else: 
            return self.m_inventory[p_index]
    
    def GetItems(self):
        return self.m_inventory
    
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
            return self.m_inventory[self.m_weapon]
        
    def GetArmor(self):
        if self.m_armor == -1:
            return None
        else:
            return self.m_inventory[self.m_armor]
        
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
        self.m_attributes[Attribute_HPREGEN] = int(self.GetAttr(Attribute_HEALTH) / 5 + self.m_level)
        
        self.m_attributes[Attribute_ACCURACY] = self.GetAttr(Attribute_AGILITY) * 3
        self.m_attributes[Attribute_DODGING] = self.GetAttr(Attribute_AGILITY) * 3
        self.m_attributes[Attribute_DAMAGEABSORB] = int(self.GetAttr(Attribute_STRENGTH) / 5)
        self.m_attributes[Attribute_STRIKEDAMAGE] = int(self.GetAttr(Attribute_STRENGTH) / 5)
        
        if self.m_hitpoints > self.GetAttr(Attribute_MAXHITPOINTS):
            self.m_hitpoints = self.GetAttr(Attribute_MAXHITPOINTS)
            
        if self.GetWeapon() != None:
            self.AddDynamicBonuses(self.GetWeapon())
        if self.GetArmor() != None:
            self.AddDynamicBonuses(self.GetArmor())
            
    def AddDynamicBonuses(self, p_item):
        if p_item == None:
            return
        
        for x in range(0, NUMATTRIBUTES):
            self.m_attributes[x] += p_item.GetAttr(x)
            
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
        if len(self.m_inventory) < self.GetMaxItems():
            #find the first open index to put the item in.
            self.m_inventory.append(p_item)
            return True
        else:
            return False
        
    def DropItem(self, p_index):
        if self.m_inventory[p_index] != None:
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
        if p_item == None:
            return
        
        for x in range(0, NUMATTRIBUTES):
            self.m_baseattributes[x] += p_item.GetAttr(x)
        self.RecalculateStats()
        
    def RemoveWeapon(self):
        self.m_weapon = -1
        self.RecalculateStats()
        
    def RemoveArmor(self):
        self.m_armor = -1
        self.RecalculateStats()
        
    def UseWeapon(self, p_index):
        self.RemoveWeapon()
        self.m_weapon = int(p_index)
        self.RecalculateStats()
        
    def UseArmor(self, p_index):
        self.RemoveArmor()
        self.m_armor = int(p_index)
        self.RecalculateStats()
        
    def GetItemIndex(self, p_name):
        for i in range(0, len(self.m_inventory)):
            if self.m_inventory[i].MatchFull(p_name):
                return i
            
        for i in range(0, len(self.m_inventory)):
            if self.m_inventory[i].Match(p_name):
                return i
            
        return -1
            
    def SendString(self, p_string):
        if self.GetConn() == None:
            ERRORLOG.Log("Trying to send string to player " + self.GetName() + " but player is not connected.")
            return
        
        self.GetConn().Protocol().SendString(self.GetConn(), p_string + newline)
        
        if self.GetActive():
            self.PrintStatbar()
            
    def PrintStatbar(self, p_update = False):
        # if this is a statusbar update and the user is currently typing something,
        # then do nothing.        
        if p_update and self.GetConn().Protocol().Buffered() > 0:
            return
        
        statbar = white + bold + "["
        
        ratio = 100 * self.GetHitPoints() / self.GetAttr(Attribute_MAXHITPOINTS)

        #color code your hitpoints so that they are red if low,
        #yellow if medium, and green if high.
        if ratio < 33:
            statbar += red
        elif ratio < 67:
            statbar += yellow
        else:
            statbar += green
            
        statbar += str(self.GetHitPoints()) + white + "/" + str(self.GetAttr(Attribute_MAXHITPOINTS)) + "] "
        self.GetConn().Protocol().SendString(self.GetConn(), clearline + "\r" + statbar + reset)
        
    def Save(self, sr):
        id1 = self.GetId()
        sr.set("Player:" + id1 + ":Name", self.m_name)
        sr.set("Player:" + id1 + ":PASS", self.m_pass)
        sr.set("Player:" + id1 + ":RANK", GetRankString(self.m_rank))
        sr.set("Player:" + id1 + ":STATPOINTS", str(self.m_statpoints))
        sr.set("Player:" + id1 + ":EXPERIENCE", str(self.m_experience))
        sr.set("Player:" + id1 + ":LEVEL", str(self.m_level))
        sr.set("Player:" + id1 + ":ROOM", self.m_room.GetId())
        sr.set("Player:" + id1 + ":MONEY", str(self.m_money))
        sr.set("Player:" + id1 + ":HITPOINTS", str(self.m_hitpoints))
        sr.set("Player:" + id1 + ":NEXTATTACKTIME", str(self.m_nextattacktime))
        
        for i in range(0, NUMATTRIBUTES):
            sr.set("Player:" + id1 + ":" + GetAttributeString(i), str(self.m_baseattributes[i]))
        
        string = ""
        for i in self.m_inventory:
            string += i.GetId() + " "
        sr.set("Player:" + id1 + ":INVENTORY", string.strip())
        
        sr.set("Player:" + id1 + ":WEAPON", str(self.m_weapon))
        sr.set("Player:" + id1 + ":ARMOR", str(self.m_armor))
    
    def Load(self, sr):
        id1 = self.GetId()
        self.m_name = sr.get("Player:" + id1 + ":Name")
        self.m_pass = sr.get("Player:" + id1 + ":PASS")      
        self.m_rank = GetRank(sr.get("Player:" + id1 + ":RANK"))
        self.m_statpoints = int(sr.get("Player:" + id1 + ":STATPOINTS")) 
        self.m_experience = int(sr.get("Player:" + id1 + ":EXPERIENCE")) 
        self.m_level = int(sr.get("Player:" + id1 + ":LEVEL")) 
        self.m_room = sr.get("Player:" + id1 + ":ROOM")
        self.m_money = int(sr.get("Player:" + id1 + ":MONEY")) 
        self.m_hitpoints = int(sr.get("Player:" + id1 + ":HITPOINTS")) 
        self.m_nextattacktime = int(sr.get("Player:" + id1 + ":NEXTATTACKTIME")) 
        
        for i in range(0, NUMATTRIBUTES):
            self.m_baseattributes[i] = int(sr.get("Player:" + id1 + ":" + GetAttributeString(i)))       
        
        items = sr.get("Player:" + id1 + ":INVENTORY").split(" ")
        self.m_inventory = []
        for i in items:
            if i != "" and i != "0":
                self.m_inventory.append(i)
                
        self.m_weapon = int(sr.get("Player:" + id1 + ":WEAPON"))    
        self.m_armor = int(sr.get("Player:" + id1 + ":ARMOR"))  
        
        #because item msg have not been loaded, So comment        
        #self.RecalculateStats()

   
    
