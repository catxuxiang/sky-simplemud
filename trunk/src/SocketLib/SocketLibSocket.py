'''
Created on 2012-4-25

@author: sky
'''

class Socket:
    def __init__(self, p_socket):
        self.m_sock = p_socket
        self.m_isblocking = True
    
    def GetSock(self):
        return self.m_sock
    
    def GetLocalPort(self):
        return ntohs( m_localinfo.sin_port );
        
    
    