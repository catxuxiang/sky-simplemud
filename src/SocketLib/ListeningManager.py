'''
Created on 2012-5-5

@author: Sky
'''
from SocketLib.SocketSet import MAX
from SocketLib.SocketLibSocket import ListeningSocket
from SocketLib.SocketSet import SocketSet

class ListeningManager:
    def __init__(self):
        self.m_sockets = []
        self.m_set = SocketSet()
        self.m_manager = None
        
    def __del__(self):
        for i in self.m_sockets:
            i.Close()
            
    def AddPort(self, p_port):
        if len(self.m_sockets) == MAX:
            raise Exception
        
        lsock = ListeningSocket()
        lsock.Listen(p_port)
        lsock.SetBlocking(False)
        self.m_sockets.append(lsock)
        self.m_set.AddSocket(lsock)
        
    def SetConnectionManager(self, p_manager):
        self.m_manager = p_manager
        
    def Listen(self):
        if self.m_set.Poll() > 0:
            for i in self.m_sockets:
                if self.m_set.HasActivity(i):
                    datasock = i.Accept()
                    if datasock != None:
                        self.m_manager.NewConnection(datasock)

    
