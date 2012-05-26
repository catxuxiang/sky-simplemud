'''
Created on 2012-5-20

@author: sky
'''
from BasicLib.BasicLibTime import *
from BasicLib.BasicLibString import ParseWord
from SimpleMUD.Game import Game
from SimpleMUD.ItemDatabase import itemDatabase
from SimpleMUD.PlayerDatabase import playerDatabase
from SimpleMUD.RoomDatabase import roomDatabase
from SimpleMUD.StoreDatabase import storeDatabase
from SimpleMUD.EnemyDatabase import enemyTemplateDatabase, enemyDatabase
from SimpleMUD.Attributes import *
from SocketLib.Telnet import *
import os.path

DBSAVETIME = Minutes(15)
ROUNDTIME = Seconds(1)
REGENTIME = Minutes(2)
HEALTIME = Minutes(1)

class GameLoop:
    def __init__(self):
        self.LoadDatabases()
        
    def __del__(self):
        self.SaveDatabases()
        
    def Load(self):
        src = "../game.data"
        if (os.path.exists(src)):
            file = open(src)
            line = file.readline()
            time = int(ParseWord(line, 1))
            Game.GetTimer().Reset(time)            
            line = file.readline()
            self.m_savedatabases = int(ParseWord(line, 1))
            line = file.readline()
            self.m_nextround = int(ParseWord(line, 1))
            line = file.readline()
            self.m_nextregen = int(ParseWord(line, 1))
            line = file.readline()
            self.m_nextheal = int(ParseWord(line, 1))
        else:
            Game.GetTimer().Reset()
            self.m_savedatabases = DBSAVETIME
            self.m_nextround = ROUNDTIME
            self.m_nextregen = REGENTIME
            self.m_nextheal = HEALTIME
        Game.SetRunning(True)
        
    def Save(self):
        file = open("../game.data", "w")
        string = ""
        string += "[GAMETIME]      " + str(Game.GetTimer().GetMS()) + "\n"
        string += "[SAVEDATABASES] " + str(self.m_savedatabases) + "\n"
        string += "[NEXTROUND]     " + str(self.m_nextround) + "\n"
        string += "[NEXTREGEN]     " + str(self.m_nextregen) + "\n"
        string += "[NEXTHEAL]      " + str(self.m_nextheal) + "\n"
        file.write(string)
        file.close()
        
    def Loop(self):
        if Game.GetTimer().GetMS() >= self.m_nextround:
            self.PerformRound()
            self.m_nextround += ROUNDTIME
        
        if Game.GetTimer().GetMS() >= self.m_nextregen:
            self.PerformRegen()
            self.m_nextregen += REGENTIME
            
        if Game.GetTimer().GetMS() >= self.m_nextheal:
            self.PerformHeal()
            self.m_nextheal += HEALTIME
            
        if Game.GetTimer().GetMS() >= self.m_savedatabases:
            self.SaveDatabases()
            self.m_savedatabases += DBSAVETIME
            
    def LoadDatabases(self):
        self.Load()
        itemDatabase.Load()
        playerDatabase.Load()
        roomDatabase.LoadTemplates()
        roomDatabase.LoadData()
        storeDatabase.Load()
        enemyTemplateDatabase.Load()
        enemyDatabase.Load()
        
    def SaveDatabases(self):
        self.Save()
        playerDatabase.Save()
        roomDatabase.SaveData()
        enemyDatabase.Save()
        
    def PerformRound(self):
        now = Game.GetTimer().GetMS()
        for i in enemyDatabase.m_map.values():
            if now >= i.GetNextAttackTime() and len(i.GetCurrentRoom().GetPlayers()) > 0:
                Game.EnemyAttack(i.GetId())
                
    def PerformRegen(self):
        for i in roomDatabase.m_vector:
            if i.GetSpawnWhich() != None and len(i.GetEnemies()) < i.GetMaxEnemies():
                enemyDatabase.Create(i.GetSpawnWhich(), i)
                Game.SendRoom(red + bold + i.GetSpawnWhich().GetName() + " enters the room!", i)
                
    def PerformHeal(self):
        for i in playerDatabase.m_map.values():
            if i.GetActive():
                i.AddHitpoints(i.GetAttr(Attribute_HPREGEN))
                i.PrintStatbar(True)
                                   
    
