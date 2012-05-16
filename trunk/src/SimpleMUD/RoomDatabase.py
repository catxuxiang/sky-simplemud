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
        file = open("../maps/default.map")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                room = Room()
                room.SetId(id1)
                room.LoadTemplate(file)
                self.m_vector.append(room)
            line = file.readline() 
        file.close()  

    def LoadData(self):
        file = open("../maps/default.data")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                self.m_vector[int(id1) - 1].LoadData(file)
            line = file.readline() 
        file.close()
        
    def SaveData(self):
        file = open("../maps/default.data", "w")
        string = ""
        for i in self.m_vector:
            string += "[ROOMID] " + i.GetId() + "\n"
            string += i.SaveData() + "\n"
        file.write(string)
        file.close()

roomDatabase = RoomDatabase()
        


