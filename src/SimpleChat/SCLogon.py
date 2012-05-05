'''
Created on 2012-5-3

@author: Sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from SimpleChat.SCUserDB import userDatabase
from SocketLib.Telnet import *
from SimpleChat.SCChat import SCChat

class SCLogon(ConnectionHandler):
    def __init__(self, p_conn):
        ConnectionHandler.__init__(self, p_conn)
        
    def Handle(self, p_data):
        conn = self.m_connection
        
        if not userDatabase.IsValidName(p_data):
            conn.Protocol().SendString(conn, red + bold + "Sorry, that is an invalid username.\r\n" + "Please enter another username: " + reset + bold)
            return
        
        if userDatabase.HasUser(p_data):
            conn.Protocol().SendString(conn, red + bold + "Sorry, that name is already in use.\r\n" + "Please enter another username: " + reset)
            return
        
        userDatabase.AddUser(conn, p_data)
        conn.Protocol().SendString(conn, "Thank you for joining us, " + p_data + newline)
        
        conn.RemoveHandler()
        conn.AddHandler(SCChat(conn))
        
    def Enter(self):
        self.m_connection.Protocol().SendString(self.m_connection, green + bold + "Welcome To SimpleChat!\r\n" + "Please enter your username: " + reset + bold)
        
    @staticmethod
    def NoRoom(p_connection):
        msg = "Sorry, there is no more room on this server.\r\n"
        p_connection.Send(msg)

        