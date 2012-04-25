'''
Created on 2012-4-25

@author: sky
'''
from SocketLib.Telnet import *
from BasicLib.BasicLibLogger import USERLOG, ERRORLOG

LogonState_NEWCONNECTION = 0
LogonState_NEWUSER = 1
LogonState_ENTERNEWPASS = 2
LogonState_ENTERPASS = 3

class Logon(Telnet):
    def __init__(self, p_conn):
        Telnet.__init__(self, p_conn)
        self.m_state = LogonState_NEWCONNECTION
        self.m_errors = 0
    
    def Hungup(self, ip):
        USERLOG.Log(ip + " - hung up in login state.")
 
    def Flooded(self, ip):
        USERLOG.Log(ip + " - flooded in login state.")
        
    def NoRoom(self, p_client):
        msg = "Sorry, there is no more room on this server.\r\n"
        try:
            p_client.send(msg.encode("ascii"))
        except:
            ERRORLOG.Log("Logon's NoRoom Exception")
            
    def Handle(self, p_data):
        if self.m_errors == 5:
            self.m_client.send(red + bold + "Too many incorrect responses, closing connection..." + newline)
            self.m_client.close()
            return
        
        if self.m_state == LogonState_NEWCONNECTION:
            if p_data.lower() == "new":
                self.m_state = LogonState_NEWUSER
                self.m_client.send(yellow + "Please enter your desired name: " + reset)
            else
     
