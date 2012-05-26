'''
Created on 2012-4-21

@author: Sky
'''
from SimpleMUD.EntityDatabase import EntityDatabase
from BasicLib.BasicLibString import ParseWord
from SimpleMUD.Store import Store
from BasicLib.BasicLibLogger import USERLOG

class StoreDatabase(EntityDatabase):
    def Load(self):
        file = open("../stores/stores.str")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                store = Store()
                store.SetId(id1)
                store.FromLines(file)
                self.m_map[id1] = store
                USERLOG.Log("Loaded Store: " + store.GetName())
            line = file.readline() 
        file.close()  
        return True
    
storeDatabase = StoreDatabase()
