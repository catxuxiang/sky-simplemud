'''
Created on 2012-5-2

@author: Sky
'''
from SocketLib.SocketLibSocket import DataSocket
from BasicLib.BasicLibTime import *
from SocketLib.Telnet import Telnet

BUFFERSIZE = 1024
TIMECHUNK = 16

class Connection(DataSocket):
    def __init__(self, p_socket = None):
        if p_socket != None:
            DataSocket.__init__(self, p_socket.GetSock())
        self.Initialize()
        
    def Initialize(self):
        self.m_datarate = 0
        self.m_lastdatarate = 0
        self.m_lastReceiveTime = 0
        self.m_lastSendTime = 0
        self.m_checksendtime = False
        self.m_creationtime = GetTimeMS()
        self.m_closed = False
        self.m_handlerstack = []
        self.m_protocol = Telnet()
        self.m_sendbuffer = ""
        
    def GetLastSendTime(self):
        if self.m_checksendtime:
            return GetTimeS() - self.m_lastSendTime
        return 0
    
    def BufferData(self, p_buffer):
        self.m_sendbuffer += p_buffer
        
    def SendBuffer(self):
        sent = 0
        if len(self.m_sendbuffer) > 0:
            sent = DataSocket.Send(self, self.m_sendbuffer)
            self.m_sendbuffer = ""

        if sent > 0:
            self.m_lastSendTime = GetTimeS()
            self.m_checksendtime = False
        else:
            if not self.m_checksendtime:
                self.m_checksendtime = True
                self.m_lastSendTime = GetTimeS()
                
    def Receive(self):
        byte = DataSocket.Receive(self, BUFFERSIZE)
        if len(byte) != 0 and byte[0] == 255:
            return
        
        t = GetTimeS()
        
        if int(self.m_lastReceiveTime / TIMECHUNK) != int(t / TIMECHUNK):
            self.m_lastdatarate = self.m_datarate / TIMECHUNK
            self.m_datarate = 0
            self.m_lastReceiveTime = t
            
        self.m_datarate += len(byte)
        
        #tell the protocol policy object about the received data.
        self.m_protocol.Translate(self, byte, len(byte))
        
    def GetLastReceiveTime(self):
        return self.m_lastReceiveTime
    
    def Close(self):
        self.m_closed = True
        
    def CloseSocket(self):
        DataSocket.Close(self)
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
    
    def SwitchHandler(self, p_handler):
        if self.Handler():
            handler = self.Handler()
            handler.Leave()     # leave the current state if it exists
            del handler       # delete state
            del self.m_handlerstack[len(self.m_handlerstack) - 1]   # pop the pointer off

        self.m_handlerstack.append(p_handler)
        p_handler.Enter()     # enter the new state

    def AddHandler(self, p_handler):
        if self.Handler():
            self.Handler().Leave() # leave the current state if it exists
        self.m_handlerstack.append(p_handler)
        p_handler.Enter()     # enter the new state
    
    def RemoveHandler(self):
        handler = self.Handler()
        handler.Leave()     # leave current state
        del handler       # delete state
        del self.m_handlerstack[len(self.m_handlerstack) - 1]   # pop the pointer off
        if self.Handler():         # if old state exists,
            self.Handler().Enter() # tell it connection has re-entered
            
    def Handler(self):
        if len(self.m_handlerstack) == 0:
            return None
        return self.m_handlerstack[len(self.m_handlerstack) - 1]
    
    def ClearHandlers(self):
        # leave the current handler
        if self.Handler():  
            self.Handler().Leave()

        # delete all the handlers on the stack
        while self.Handler():
            handler = self.Handler()
            del handler
            del self.m_handlerstack[len(self.m_handlerstack) - 1]   # pop the pointer off



        
    
    
    
