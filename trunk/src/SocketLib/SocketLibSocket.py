'''
Created on 2012-4-29

@author: Sky
'''
'''
Created on 2012-4-25

@author: sky
'''
import socket

class Socket():
    def __init__(self, p_socket):
        self.m_sock = p_socket
        self.m_sock.setblocking(True)
        self.localAddress, self.localPort = self.m_sock.getsockname()
        
    def GetSock(self):
        return self.m_sock
    
    def GetLocalPort(self):
        return self.localPort
    
    def GetLocalAddress(self):
        return self.localAddress
    
    def Close(self):
        self.m_sock.close()
        
    def SetBlocking(self, p_blockmode):
        self.m_sock.setblocking(p_blockmode)
        
class DataSocket(Socket):
    def Connect(self, p_addr, p_port):
        if self.m_connected == True:
            raise Exception("The socket is already connected!") 

        if self.m_sock == None:
            self.m_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        self.remoteAddress = p_addr
        self.remotePort = p_port

    def GetRemotePort(self):
        return self.remotePort
    
    def GetRemoteAddress(self):
        return self.remoteAddress 
    
    def IsConnected(self):
        return self.m_connected
    
    def Send(self, string):
        self.m_sock.send(string)
        
    def Receive(self, p_size):
        return self.m_sock.recv(p_size)
    
    def Close(self):
        Socket.Close(self)
        self.m_connected = False
        
class ListeningSocket(Socket):
    def __init__(self):
        self.m_listening = False
        
    def Listen(self, p_port):
        if(self.m_sock == None):
            self.m_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_sock.bind(("localhost", p_port)) 
        self.m_sock.listen(8) 
        self.m_listening = True
        
    def Accept(self):
        client, addr = self.m_sock.accept()
        return DataSocket(client)
    
    def Close(self):
        self.m_sock.close()
        self.m_listening = False

    
    