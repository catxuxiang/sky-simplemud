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
        sr = EntityDatabaseVector.Sr
        for i in range(0, sr.llen("EnemyTemplateList")):
            id1 = sr.lindex("EnemyTemplateList", i)
            enemy = EnemyTemplate()
            enemy.SetId(id1)
            enemy.Load(sr)
            self.m_vector.append(enemy)
            USERLOG.Log("Loaded EnemyTemplate: " + enemy.GetName())
   
            
    
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
        sr = EntityDatabaseVector.Sr
        for i in range(0, sr.llen("EnemyList")):
            id1 = sr.lindex("EnemyList", i)
            enemy = Enemy()
            enemy.SetId(id1)
            enemy.Load(sr)
            self.m_map[id1] = enemy
     
    def Save(self):
        sr = EntityDatabaseVector.Sr
        sr.ltrim("EnemyList", 2, 1)
        for i in self.m_map:
            sr.rpush("EnemyList", i)
            self.m_map[i].Save(sr)
            
enemyTemplateDatabase = EnemyTemplateDatabase()
enemyDatabase = EnemyDatabase()

'''             
i = EnemyDatabase()
i.Load()
i.Save()
'''
