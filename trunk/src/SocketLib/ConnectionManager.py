'''
Created on 2012-5-5

@author: Sky
'''
from SocketLib.SocketSet import MAX, SocketSet
from SocketLib.Connection import Connection
from SimpleMUD.Logon import Logon

class ConnectionManager:
    def __init__(self, p_maxdatarate, p_sendtimeout, p_maxbuffered):
        self.m_connections = []
        self.m_set = SocketSet()
        self.m_maxdatarate = p_maxdatarate
        self.m_sendtimeout = p_sendtimeout
        self.m_maxbuffered = p_maxbuffered
        
    def __del__(self):
        for i in self.m_connections:
            i.CloseSocket()

    def NewConnection(self, p_socket):
        # turn the socket into a connection
        conn = Connection(p_socket)
        
        if self.AvailableConnections() == 0:
            # tell the default protocol handler that there is no more room
            # for the connection within this manager.
            Logon.NoRoom(conn)
            conn.CloseSocket()
        else:
            self.m_connections.append(conn)
            conn.SetBlocking(False)
            self.m_set.AddSocket(conn)
            conn.AddHandler(Logon(conn))
            
    def Close(self, conn):
        self.m_set.RemoveSocket(conn)
        conn.CloseSocket()
        index = 0
        i = -1
        for connection in self.m_connections:
            if connection == conn:
                i = index
            index += 1
        if i != -1:
            del self.m_connections[i]
            
    def Listen(self):
        socks = 0
        if self.TotalConnections() > 0:
            socks = self.m_set.Poll()
            
        # detect if any sockets have action on them
        if socks > 0:
            for c in self.m_connections:
                if self.m_set.HasActivity(c):
                    #try:
                    c.Receive()
                    if c.GetCurrentDataRate() > self.m_maxdatarate:
                        # too much data was sent, tell the protocol handler
                        c.Close()
                        c.Handler().Flooded()
                        
                        # close the connection
                        self.Close(c)
                    #except Exception:
                    #    print("ConnectionManager:Listen() Exception!")
                    #    c.Close()
                    #    #print(c.Handler())
                    #    c.Handler().Hungup()
                    #    self.Close(c)
    def Send(self):
        for c in self.m_connections:
            try:
                c.SendBuffer()
                if c.GetBufferedBytes() > self.m_maxbuffered or c.GetLastSendTime() > self.m_sendtimeout:
                    c.Close()
                    c.Handler().Hungup()
                    self.Close(c)
            except:
                print("ConnectionManager:Send() Exception!")
                c.Close()
                c.Handler().Hungup()
                self.Close(c)
                
    def CloseConnections(self):
        for c in self.m_connections:
            if c.Closed():
                self.Close(c)
        
    def AvailableConnections(self):
        return MAX - len(self.m_connections)
    
    def TotalConnections(self):
        return len(self.m_connections)
    
    def Manage(self):
        self.Listen()
        self.Send()
        self.CloseConnections()
        
    
