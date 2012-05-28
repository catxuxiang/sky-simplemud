'''
Created on 2012-5-15

@author: sky
'''
from SimpleMUD.EntityDatabase import EntityDatabase
from SimpleMUD.Item import Item
from BasicLib.BasicLibString import ParseWord
from BasicLib.BasicLibLogger import USERLOG

class ItemDatabase(EntityDatabase):
    def Load(self):
        sr = EntityDatabase.Sr
        for i in range(0, sr.llen("ItemList")):
            id1 = sr.lindex("ItemList", i)
            item = Item()
            item.SetId(id1)
            item.Load(sr)
            self.m_map[id1] = item
            USERLOG.Log("Loaded Item: " + item.GetName())
        return True

itemDatabase =ItemDatabase()
