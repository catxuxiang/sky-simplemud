'''
Created on 2012-4-27

@author: sky
'''
from SimpleMUD.EnemyDatabase import EntityDatabase
from SimpleMUD.Player import Player
from BasicLib.BasicLibString import ParseWord
from BasicLib.BasicLibLogger import USERLOG

class PlayerDatabase(EntityDatabase):
    def GetLastId(self):
        return str(len(self.m_map))
    
    def FindActive(self, p_name):
        for i in self.m_map.values():
            if i.MatchFull(p_name) and i.GetActive():
                return i
            
        for i in self.m_map.values():
            if i.Match(p_name) and i.GetActive():
                return i
            
        return None
    
    def FindLoggedIn(self, p_name):
        for i in self.m_map.values():
            if i.MatchFull(p_name) and i.GetLoggedIn():
                return i
            
        for i in self.m_map.values():
            if i.Match(p_name) and i.GetLoggedIn():
                return i
            
        return None
    
    def LoadPlayer(self, p_id):
        sr = EntityDatabase.Sr
        player = Player()
        player.SetId(p_id)
        player.Load(sr)
        self.m_map[p_id] = player
        
        USERLOG.Log("Loaded Player: " + self.m_map[p_id].GetName())
        
    def Load(self):
        sr = EntityDatabase.Sr
        for i in sr.hkeys("PlayerHash"):
            self.LoadPlayer(i)
        return True
    
    def SavePlayer(self, p_player):
        p_player.Save(EntityDatabase.Sr)

    def Save(self):
        sr = EntityDatabase.Sr
        for i in sr.hkeys("PlayerHash"):
            sr.hdel("PlayerHash", i)
        for i in self.m_map.values():
            sr.hset("PlayerHash", i.GetId(), i.GetName())
            self.SavePlayer(i)
        return True

    def AddPlayer(self, p_player):
        for i in self.m_map.values():
            if i.GetId() == p_player.GetId() or i.GetName().lower() == p_player.GetName().lower():
                return False
            
        self.m_map[p_player.GetId()] = p_player
        
        file = open('../players/players.txt', 'a')
        file.write(p_player.GetName() + "\n")
        file.close()
        
        self.SavePlayer(p_player)
        
        return True
    
    def Logout(self, p_player):
        USERLOG.Log("User " + p_player.GetName() + " logged off.")
        
        p_player.SetConn(None)
        p_player.SetLoggedIn(False)
        p_player.SetActive(False)
        
        self.SavePlayer(p_player)
        
playerDatabase = PlayerDatabase()

