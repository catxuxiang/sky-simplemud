'''
Created on 2012-4-21

@author: Sky
'''
from EntityDatabase import EntityDatabase
from BasicLib import BasicLibString
from Store import Store
from BasicLib import BasicLibLogger

m_map = {}

class StoreDatabase(EntityDatabase):
    def Load(self):
        file = open("..\stores\stores.str")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = BasicLibString.ParseWord(line, 1)
                store = Store()
                store.SetId(id1)
                store.FromLines(file)
                m_map[int(id1) - 1] = store
                BasicLibLogger.USERLOG.Log( "Loaded Store: " + m_map[int(id1) - 1].GetName())
            line = file.readline() 
        print(len(m_map))
        file.close()  
        return True      

'''    
i = StoreDatabase()
i.Load()
'''
