'''
Created on 2012-4-15

@author: Sky
'''

from Entity import Entity

WEAPON = 0
ARMOR = 1
HEALING = 2

class Item(Entity):
    def __init__(self):
        self.m_type = WEAPON
        self.m_min = 0
        self.m_max = 0
        self.m_speed = 0
    

        

        
        
        