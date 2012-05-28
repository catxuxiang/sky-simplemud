'''
Created on 2012-5-15

@author: sky
'''
from BasicLib.BasicLibString import *
from SimpleMUD.Room import Room
from BasicLib.BasicLibLogger import USERLOG
from SimpleMUD.EnemyDatabase import EntityDatabaseVector

class RoomDatabase(EntityDatabaseVector):
    def LoadTemplates(self):
        sr = EntityDatabaseVector.Sr
        for i in range(0, sr.llen("RoomTemplateList")):
            id1 = sr.lindex("RoomTemplateList", i)
            room = Room()
            room.SetId(id1)
            room.LoadTemplate(sr)
            self.m_vector.append(room)

    def LoadData(self):
        sr = EntityDatabaseVector.Sr
        for i in self.m_vector:
            i.LoadData(sr)
        
    def SaveData(self):
        sr = EntityDatabaseVector.Sr
        for i in self.m_vector:
            i.SaveData(sr)

roomDatabase = RoomDatabase()
        


