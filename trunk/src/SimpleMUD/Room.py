'''
Created on 2012-4-20

@author: sky
'''
from Entity import Entity
from SimpleMUD import Attributes
from BasicLib import BasicLibString

class Room(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.m_type = Attributes.RoomType_PLAINROOM
        self.m_data = 0
        self.m_description = "UNDEFINED"
        
        self.m_rooms = []
        for d in range(0, Attributes.NUMDIRECTIONS):
            self.m_rooms.append(0)
        
        self.m_spawnwhich = 0
        self.m_maxenemies = 0
        self.m_money = 0
        
        self.m_players = []
        self.m_enemies = []
        
    def AddPlayer(self, p_player):
        self.m_players.append(p_player)
        
    def RemovePlayer(self, p_player):
        for i in self.m_players:
            if i.GetId() == p_player.GetId():
                del i
                
    def FindItem(self, p_item):
        for i in self.m_items:
            if i.MatchFull(p_item):
                return i
            
        for i in self.m_items:
            if i.Match(p_item):
                return i
            
        return None
    
    def AddItem(self, p_item):
        if len(self.m_items) >= 32:
            del self.m_items[len(self.m_items) - 1]
        self.m_items.append(p_item)
        
    def RemoveItem(self, p_item):
        for i in self.m_items:
            if i.GetId() == p_item.GetId():
                del i
    
    def FindEnemy(self, p_enemy):
        for i in self.m_enemies:
            if i.MatchFull(p_enemy):
                return i
            
        for i in self.m_enemies:
            if i.Match(p_enemy):
                return i
            
        return None        
        
    def AddEnemy(self, p_enemy):
        self.m_enemies.append(p_enemy)
        
    def RemoveEnemy(self, p_enemy):
        for i in self.m_enemies:
            if i.GetId() == p_enemy.GetId():
                del i    
                
    def LoadTemplate(self, file):
        line = file.readline()
        name = BasicLibString.RemoveWord(line, 0)
        self.m_name = name.strip()
        line = file.readline()
        description = BasicLibString.RemoveWord(line, 0)
        self.m_description = description.strip()        
        line = file.readline()
        self.m_type = Attributes.GetRoomType(BasicLibString.ParseWord(line, 1))
        line = file.readline()
        self.m_data = BasicLibString.ParseWord(line, 1)
        
        for d in range(0, Attributes.NUMDIRECTIONS):
            line = file.readline()
            self.m_rooms[d] = BasicLibString.ParseWord(line, 1)
            
        
        line = file.readline()
        self.m_spawnwhich = BasicLibString.ParseWord(line, 1)
        line = file.readline()
        self.m_maxenemies = BasicLibString.ParseWord(line, 1)
      
         


        
        
a = [1,2,3,4]
print(a)
del a[2]
print(a)
print(len(a))