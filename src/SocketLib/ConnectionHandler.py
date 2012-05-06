'''
Created on 2012-5-2

@author: Sky
'''
'''
Created on 2012-4-24

@author: sky
'''

class ConnectionHandler:
    def __init__(self, p_conn):
        self.m_connection = p_conn
        
    def Handle(self, p_data):
        return 0
        
    def Enter(self):
        return 0
    
    def Leave(self):
        return 0
    
    def Hungup(self):
        return 0

    def Flooded(self):
        return 0
