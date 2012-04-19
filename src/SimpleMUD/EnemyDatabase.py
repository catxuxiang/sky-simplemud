'''
Created on 2012-4-15

@author: Sky
'''
from EntityDatabase import EntityDatabase, EntityDatabaseVector
from BasicLib import BasicLibString
from Enemy import EnemyTemplate

class EnemyTemplateDatabase(EntityDatabaseVector):

    def Load(self):
        file = open("..\enemies\enemies.templates")
        line = file.readline()
        while line:
            if line.strip() != "":
                enemy = EnemyTemplate()
                enemy.SetId(BasicLibString.ParseWord(line, 1))
                enemy.FromLines(file)
                print(enemy)
                self.container.append(enemy)
            line = file.readline()    
            #USERLOG.Log( "Loaded Enemy: " + m_vector[id].Name() )
    
i = EnemyTemplateDatabase()
i.Load()


    
class EnemyDatabase(EntityDatabase):
    #def __init__(self):
        
    def Load(self):
        return None