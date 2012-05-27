'''
Created on 2012-4-15

@author: Sky
'''
from SimpleMUD.EntityDatabase import EntityDatabase, EntityDatabaseVector
from BasicLib.BasicLibString import ParseWord
from SimpleMUD.Enemy import EnemyTemplate, Enemy
from BasicLib.BasicLibLogger import USERLOG

class EnemyTemplateDatabase(EntityDatabaseVector):

    def Load(self):
        file = open("..\enemies\enemies.templates")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                enemy = EnemyTemplate()
                enemy.SetId(id1)
                enemy.FromLines(file)
                #print(enemy)
                self.m_vector.append(enemy)
                USERLOG.Log("Loaded Enemy: " + enemy.GetName())
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
        self.m_map[id1] = e

    def Delete(self, p_enemy):
        p_enemy.GetCurrentRoom().RemoveEnemy(p_enemy)
        del self.m_map[p_enemy.GetId()]
        del p_enemy
    
    def Load(self):
        file = open("..\enemies\enemies.instances")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                enemy = Enemy()
                enemy.SetId(id1)
                enemy.FromLines(file)
                #enemy.GetCurrentRoom().AddEnemy(enemy)
                self.m_map[id1] = enemy
            line = file.readline() 
        #print(len(self.m_map))
        file.close()
     
    def Save(self):
        file = open("..\enemies\enemies.instances", "w")
        string = ""
        for i in self.m_map:
            string += "[ID] " + i + "\n"
            string += self.m_map[i].ToLines()
            string += "\n"
        file.write(string)
        file.close()
        
enemyTemplateDatabase = EnemyTemplateDatabase()
enemyDatabase = EnemyDatabase()

'''             
i = EnemyDatabase()
i.Load()
i.Save()
'''
