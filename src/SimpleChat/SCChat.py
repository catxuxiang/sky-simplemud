'''
Created on 2012-5-5

@author: Sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from SimpleChat.SCUserDB import userDatabase
from BasicLib.BasicLibString import ParseWord, RemoveWord
from SocketLib.Telnet import *

class SCChat(ConnectionHandler):
    def __init__(self, p_conn):
        ConnectionHandler.__init__(self, p_conn)
        
    def Handle(self, p_data):
        name = userDatabase.Find(self.m_connection).name
        
        # message is a command
        if p_data[0:1] == '/':
            command = ParseWord(p_data, 0)
            data = RemoveWord(p_data, 0)
            
            if command == "/who":
                wholist = magenta + bold + "Who is in the room: "
                
                if len(userDatabase.m_users) == 0:
                    for i in userDatabase.m_users:
                        wholist += i.name
                        wholist += ", "
                    wholist = wholist[0:len(wholist) - 2]
                wholist += newline
                self.m_connection.Protocol().SendString(self.m_connection, wholist)
            elif command == "/quit":
                self.CloseConnection("has quit. Message: " + data)
                self.m_connection.Close()
        else:
            if len(p_data.strip()) > 0:
                self.SendAll(green + bold + "<" + name + "> " + reset + p_data)
    
    def Enter(self):
        self.SendAll(bold + yellow + userDatabase.Find(self.m_connection).name + " has entered the room.")
        
    def Leave(self):
        userDatabase.DeleteUser(self.m_connection)
        
    def Hungup(self):
        self.CloseConnection("has hung up!")
        
    def Flooded(self):
        self.CloseConnection("has been kicked for flooding!")
        
    def CloseConnection(self, p_reason):
        self.SendAll(bold + red + userDatabase.Find(self.m_connection).name + " " + p_reason)
        
    def SendAll(self, p_message):
        for i in userDatabase.m_users:
            i.connection.Protocol().SendString(i.connection, p_message + newline)
        
