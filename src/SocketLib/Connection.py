'''
Created on 2012-5-2

@author: Sky
'''
from SocketLib.SocketLibSocket import DataSocket
from BasicLib.BasicLibString import GetTimeMS

BUFFERSIZE = 1024
TIMECHUNK = 16

class Connection(DataSocket):
    def __init__(self):
        self.Initialize()
        
    def __init__(self, p_socket):
        DataSocket.__init__(p_socket)
        self.Initialize()
        
    def Initialize(self):
        self.m_datarate = 0
        self.m_lastdatarate = 0
        self.m_lastReceiveTime = 0
        self.m_lastSendTime = 0
        self.m_checksendtime = False
        self.m_creationtime = GetTimeMS()
        self.m_closed = False
        
    def GetLastReceiveTime(self):
        return self.m_lastReceiveTime
    
    def Close(self):
        self.m_closed = True
        
    def CloseSocket(self):
        self.m_sock.close()
        self.ClearHandlers()
        
    def GetDataRate(self):
        return self.m_lastdatarate
    
    def GetCurrentDataRate(self):
        return self.m_datarate / TIMECHUNK
    
    def GetBufferedBytes(self):
        return len(self.m_sendbuffer)
    
    def GetCreationTime(self):
        return self.m_creationtime
    
    def Protocol(self):
        return self.m_protocol
    
    def Closed(self):
        return self.m_closed
    
    
