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
from BasicLib.Redis import sr
import os.path

DBSAVETIME = Seconds(30)
ROUNDTIME = Seconds(1)
REGENTIME = Minutes(2)
HEALTIME = Minutes(1)

class GameLoop:
    def __init__(self):
        #self.Init()
        self.LoadDatabases()
        self.AddRelation()
        
    def __del__(self):
        self.SaveDatabases()
        
    def Load(self):
        if sr.get("GAMETIME") != None:
            time = int(sr.get("GAMETIME"))
            Game.GetTimer().Reset(time)            
            self.m_savedatabases = int(sr.get("SAVEDATABASES"))
            self.m_nextround = int(sr.get("NEXTROUND"))
            self.m_nextregen = int(sr.get("NEXTREGEN"))
            self.m_nextheal = int(sr.get("NEXTHEAL"))
        else:
            Game.GetTimer().Reset()
            self.m_savedatabases = DBSAVETIME
            self.m_nextround = ROUNDTIME
            self.m_nextregen = REGENTIME
            self.m_nextheal = HEALTIME
        Game.SetRunning(True)
        
    def Save(self):
        sr.set("GAMETIME", str(Game.GetTimer().GetMS()))
        sr.set("SAVEDATABASES", str(self.m_savedatabases))
        sr.set("NEXTROUND", str(self.m_nextround))
        sr.set("NEXTREGEN", str(self.m_nextregen))
        sr.set("NEXTHEAL", str(self.m_nextheal))
        
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
    
    def AddRelation(self):
        for player in playerDatabase.m_map.values():
            player.m_room = roomDatabase.GetValue(player.m_room)
            
            for i in range(0, len(player.m_inventory)):
                player.m_inventory[i] = itemDatabase.GetValue(player.m_inventory[i])
                
            player.RecalculateStats()
            
            
        for room in roomDatabase.m_vector:
            for d in range(0, NUMDIRECTIONS):
                room.m_rooms[d] = roomDatabase.GetValue(room.m_rooms[d])
                
            for i in range(0, len(room.m_items)):
                room.m_items[i] = itemDatabase.GetValue(room.m_items[i])
                
            room.m_spawnwhich = enemyTemplateDatabase.GetValue(room.m_spawnwhich)
            
        for store in storeDatabase.m_map.values():
            for i in range(0, len(store.m_items)):
                store.m_items[i] = itemDatabase.GetValue(store.m_items[i])            
            
        for template in enemyTemplateDatabase.m_vector:
            template.m_weapon = itemDatabase.GetValue(template.m_weapon)
            
        for enemy in enemyDatabase.m_map.values():
            enemy.m_template = enemyTemplateDatabase.GetValue(enemy.m_template)
            enemy.m_room = roomDatabase.GetValue(enemy.m_room)
            enemy.GetCurrentRoom().AddEnemy(enemy)
            
     
        
    def SaveDatabases(self):
        self.Save()
        playerDatabase.Save()
        roomDatabase.SaveData()
        enemyDatabase.Save()
        
    def PerformRound(self):
        now = Game.GetTimer().GetMS()
        for i in enemyDatabase.m_map.values():
            if now >= i.GetNextAttackTime() and len(i.GetCurrentRoom().GetPlayers()) > 0:
                Game.EnemyAttack(i)
                
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
                                   
    
