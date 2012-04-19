'''
Created on 2012-4-15

@author: Sky
'''
from EntityDatabase import EntityDatabase, EntityDatabaseVector
from BasicLib import BasicLibString
from Enemy import EnemyTemplate
from BasicLib import BasicLibLogger

m_vector = []
m_map = {}

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
                print(enemy)
                m_vector.append(enemy)
                BasicLibLogger.USERLOG.Log( "Loaded Enemy: " + m_vector[int(id1)-1].Name() )
            line = file.readline()    
            
    
#i = EnemyTemplateDatabase()
#i.Load()
    
class EnemyDatabase(EntityDatabase):
    def Load(self):
        file = open("..\enemies\enemies.templates")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = BasicLibString.ParseWord(line, 1)
                enemy = EnemyTemplate()
                enemy.SetId(id1)
                enemy.FromLines(file)
                print(enemy)
                m_vector.append(enemy)
                BasicLibLogger.USERLOG.Log( "Loaded Enemy: " + m_vector[int(id1)-1].Name() )
            line = file.readline()          
{
    ifstream file( "enemies/enemies.instances" );
    entityid id;
    std::string temp;

    file >> std::ws;    // eat the whitespace
    while( file.good() )
    {
        file >> temp >> id;
        m_map[id].ID() = id;
        file >> m_map[id] >> std::ws;
        m_map[id].CurrentRoom()->AddEnemy( id );
    }
}
}