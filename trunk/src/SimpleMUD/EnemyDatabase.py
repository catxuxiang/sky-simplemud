'''
Created on 2012-4-15

@author: Sky
'''
from SimpleMUD.EntityDatabase import EntityDatabase, EntityDatabaseVector
from BasicLib import BasicLibString
from SimpleMUD.Enemy import EnemyTemplate, Enemy
from BasicLib import BasicLibLogger

class EnemyTemplateDatabase(EntityDatabaseVector):

    def Load(self):
        file = open("..\enemies\enemies.templates")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = BasicLibString.ParseWord(line, 1)
                enemy = EnemyTemplate()
                enemy.SetId(id1)
                enemy.FromLines(file)
                #print(enemy)
                self.m_vector.append(enemy)
                BasicLibLogger.USERLOG.Log( "Loaded Enemy: " + self.m_vector[int(id1)-1].GetName() )
            line = file.readline()    
            
    
#i = EnemyTemplateDatabase()
#i.Load()
    
class EnemyDatabase(EntityDatabase):
    def Create(self, p_template, p_room):
        id1 = self.FindOpenId();
        e = Enemy()
        e.SetId(id1)
        e.LoadTemplate(p_template)
        e.SetCurrentRoom(p_room)
        p_room.AddEnemy(e)  
        self.m_map[id1 - 1] = e

    def Delete(self, p_enemy):
        p_enemy.GetCurrentRoom().RemoveEnemy(p_enemy)
        del p_enemy
    
    def Load(self):
        file = open("..\enemies\enemies.instances")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = BasicLibString.ParseWord(line, 1)
                enemy = Enemy()
                enemy.SetId(id1)
                
                enemy.FromLines(file)
                enemy.GetCurrentRoom().AddEnemy(enemy)
                self.m_map[int(id1) - 1] = enemy
            line = file.readline() 
        #print(len(self.m_map))
        file.close()
     
    def Save(self):
        file = open("..\enemies\enemies.instances", "w")
        string = ""
        for i in self.m_map:
            string += BasicLibString.Fill16Char("[ID]") + self.m_map[i].GetId() + "\n"
            string += self.m_map[i].ToLines()
            string += "\n"
        file.write(string)
        file.close()

'''             
i = EnemyDatabase()
i.Load()
i.Save()
'''
