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
    
    def PlayerFileName(self, p_name):
        return "../players/" + p_name + ".plr"
    
    def LoadPlayer(self, p_name):
        p_name = self.PlayerFileName(p_name)
        file = open(p_name)
        line = file.readline()
        id = ParseWord(line, 1)
        player = Player()
        player.SetId(id)
        player.FromLines(file)
        file.close()
        self.m_map[id] = player
        
        USERLOG.Log("Loaded Player: " + self.m_map[id].GetName())
        
    def Load(self):
        file = open("../players/players.txt")
        line = file.readline()
        while line:
            self.LoadPlayer(line.strip())
            line = file.readline()
        file.close()
        return True
    
    def SavePlayer(self, p_player):
        name = self.PlayerFileName(p_player.GetName())
        file = open(name, "w")
        string = "[ID]             " + p_player.GetId() + "\n"
        string += p_player.ToLines()
        file.write(string)
        file.close()

    def Save(self):
        file = open("../players/players.txt", "w")
        string = ""
        for i in self.m_map:
            string += i.GetName() + "\n"
            self.SavePlayer(i)
        file.write(string)
        file.close()
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
