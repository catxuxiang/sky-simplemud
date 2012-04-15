'''
Created on 2012-4-15

@author: Sky
'''

from Entity import Entity

class EnemyTemplate(Entity):
    def __init__(self):
        self.m_hitpoints = 0
        self.m_accuracy = 0
        self.m_dodging = 0
        self.m_strikedamage = 0
        self.m_damageabsorb = 0
        self.m_experience = 0
        self.m_weapon = 0
        self.m_moneymin = 0
        self.m_moneymax = 0
       
