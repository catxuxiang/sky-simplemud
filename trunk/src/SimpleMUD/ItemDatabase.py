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
        file = open("../items/items.itm")
        line = file.readline()
        while line:
            if line.strip() != "":
                id1 = ParseWord(line, 1)
                item = Item()
                item.SetId(id1)
                item.FromLines(file)
                self.m_map.append(item)
                USERLOG.Log("Loaded Item: " + self.m_map[len(self.m_map) - 1].GetName())
            line = file.readline() 
        file.close()  
        return True

itemDatabase =ItemDatabase()
