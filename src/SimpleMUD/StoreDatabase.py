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
        sr = EntityDatabase.Sr
        for i in range(0, sr.llen("StoreList")):
            id1 = sr.lindex("StoreList", i)
            store = Store()
            store.SetId(id1)
            store.Load(sr)
            self.m_map[id1] = store
            USERLOG.Log("Loaded Store: " + store.GetName())
        return True
    
storeDatabase = StoreDatabase()
