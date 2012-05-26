'''
Created on 2012-4-20

@author: sky
'''
from SimpleMUD.Entity import Entity
from SimpleMUD.Item import Item
from SimpleMUD.Attributes import *
from BasicLib.BasicLibString import RemoveWord, ParseWord
from SimpleMUD.RoomDatabase import roomDatabase
from SimpleMUD.EnemyDatabase import enemyTemplateDatabase
from SimpleMUD.ItemDatabase import itemDatabase

class Room(Entity):
    def GetType(self):
        return self.m_type
    
    def SetType(self, m_type):
        self.m_type = m_type
        
    def GetData(self):
        return self.m_data
    
    def SetData(self, m_data):
        self.m_data = m_data
        
    def GetDescription(self):
        return self.m_description
    
    def SetDescription(self, m_description):
        self.m_description = m_description
        
    def GetAdjacent(self, p_dir):
        return self.m_rooms[p_dir]
    
    def SetAdjacent(self, p_dir, value):
        self.m_rooms[p_dir] = value

    def GetSpawnWhich(self):
        return self.m_spawnwhich
    
    def SetSpawnWhich(self, m_spawnwhich):
        self.m_spawnwhich = m_spawnwhich
        
    def GetMaxEnemies(self):
        return self.m_maxenemies
    
    def SetMaxEnemies(self, m_maxenemies):
        self.m_maxenemies = m_maxenemies
        
    def GetItems(self):
        return self.m_items
    
    def SetItems(self, m_items):
        self.m_items = m_items
        
    def GetMoney(self):
        return self.m_money
    
    def SetMoney(self, m_money):
        self.m_money = m_money

    def GetEnemies(self):
        return self.m_enemies
    
    def SetEnemies(self, m_enemies):
        self.m_enemies = m_enemies
        
    def GetPlayers(self):
        return self.m_players
    
    def SetPlayers(self, m_players):
        self.m_players = m_players 
    
    def __init__(self):
        Entity.__init__(self)
        self.m_type = RoomType_PLAINROOM
        self.m_data = "0"
        self.m_description = "UNDEFINED"
        
        self.m_rooms = []
        for _ in range(0, NUMDIRECTIONS):
            self.m_rooms.append(None)
        
        self.m_spawnwhich = None
        self.m_maxenemies = 0
        self.m_money = 0
        
        self.m_players = []
        self.m_enemies = []
        
        self.m_items = []
        
    def AddPlayer(self, p_player):
        self.m_players.append(p_player)
        
    def RemovePlayer(self, p_player):
        i = 0
        index = -1
        for p in self.m_players:
            if p == p_player:
                index = i
            i += 1
        if index != -1:
            del self.m_players[index]
                
    def FindItem(self, p_name):
        for i in self.m_items:
            if i.MatchFull(p_name):
                return i
            
        for i in self.m_items:
            if i.Match(p_name):
                return i
            
        return None
    
    def AddItem(self, p_item):
        if len(self.m_items) >= 32:
            del self.m_items[len(self.m_items) - 1]
        self.m_items.append(p_item)
        
    def RemoveItem(self, p_item):
        i = 0
        index = -1
        for item in self.m_items:
            if item.GetId() == p_item.GetId():
                index = i
            i += 1
        if index != -1:
            del self.m_items[index]
    
    def FindEnemy(self, p_name):
        for i in self.m_enemies:
            if i.MatchFull(p_name):
                return i
            
        for i in self.m_enemies:
            if i.Match(p_name):
                return i
            
        return None        
        
    def AddEnemy(self, p_enemy):
        self.m_enemies.append(p_enemy)
        
    def RemoveEnemy(self, p_enemy):
        i = 0
        index = -1        
        for e in self.m_enemies:
            if e.GetId() == p_enemy.GetId():
                index = i
            i += 1
        if index != -1:
            del self.m_enemies[index]
                
    def LoadTemplate(self, file):
        line = file.readline()
        name = RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        description = RemoveWord(line, 0)
        self.m_description = description.strip()        
        line = file.readline()
        self.m_type = GetRoomType(ParseWord(line, 1))
        line = file.readline()
        self.m_data = ParseWord(line, 1)
        
        for d in range(0, NUMDIRECTIONS):
            line = file.readline()
            self.m_rooms[d] = roomDatabase.GetValue(ParseWord(line, 1))
            #print(self.m_rooms[d])
        
        line = file.readline()
        self.m_spawnwhich = enemyTemplateDatabase.GetValue(ParseWord(line, 1))
        line = file.readline()
        self.m_maxenemies = int(ParseWord(line, 1))
        #print(self.m_maxenemies)
        
    def LoadData(self, file):
        self.m_items = []
        line = file.readline()
        itemids = RemoveWord(line, 0).strip()
        for i in itemids.split(' '):
            if i != "0":
                self.m_items.append(itemDatabase.GetValue(i))
                
        line = file.readline()
        self.m_money = int(ParseWord(line, 1))
        #print(self.m_money)
        
    def SaveData(self):
        string = "[ITEMS] "
        for i in self.m_items:
            string += i.GetId() + " "
        string += "0\n"
        string += "[MONEY] " + str(self.m_money) + "\n"
        return string


'''
i = Room()
file = open("Room.templates")
i.LoadTemplate(file)
'''

'''           
i = Room()
file = open("Room.instances")
file.readline()
i.LoadData(file)
print(i.SaveData())     
'''      
         


        
'''        
a = [1,2,3,4]
print(a)
del a[2]
print(a)
print(len(a))
'''