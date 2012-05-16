'''
Created on 2012-4-25

@author: sky
'''
from SocketLib.Telnet import *
from BasicLib.BasicLibLogger import USERLOG, ERRORLOG
from SimpleMUD.PlayerDatabase import playerDatabase
from SimpleMUD.Player import Player
from SimpleMUD.Attributes import *

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
            self.m_connection.send(red + bold + "Too many incorrect responses, closing connection..." + newline)
            self.m_connection.close()
            return
        
        if self.m_state == LogonState_NEWCONNECTION:
            if p_data.lower() == "new":
                self.m_state = LogonState_NEWUSER
                self.m_connection.send(yellow + "Please enter your desired name: " + reset)
            else:
                playerdb = playerDatabase.FindFull(p_data)
                if(playerdb == None):
                    self.m_errors += 1
                    self.m_connection.send(red + bold + "Sorry, the user \"" + white + p_data + red + "\" does not exist.\r\n" + "Please enter your name, or \"new\" if you are new: " + reset)
                else:
                    self.m_state = LogonState_ENTERPASS
                    self.m_name = p_data
                    self.m_pass = playerdb.GetPassword()
                    self.m_connection.send(green + bold + "Welcome, " + white + p_data + red + newline + green + "Please enter your password: " + reset)
            return
     
        if self.m_state == LogonState_ENTERNEWPASS:
            if len(p_data.strip()) == 0:
                self.m_errors += 1
                self.m_connection.send(red + bold + "INVALID PASSWORD!" + green + "Please enter your desired password: " + reset)
                return
            
            self.m_connection.send(green + "Thank you! You are now entering the realm..." + newline)
            p = Player()
            p.SetName(self.m_name)
            p.SetPassword(p_data)
            
            if playerDatabase.Size() == 0:
                p.SetRank(PlayerRank_ADMIN)
                p.SetId(1)
            else:
                p.SetId(playerDatabase.LastID() + 1)
                
            playerDatabase.AddPlayer(p)
            self.GotoGame(True)
            return
        
        if self.m_state == LogonState_ENTERPASS:
            if self.m_pass == p_data:
                self.m_connection.send(green + "Thank you! You are now entering the realm..." + newline)
                self.GotoGame()
            else:
                self.m_errors += 1
                self.m_connection.send(red + bold + "INVALID PASSWORD!" + newline + yellow + "Please enter your password: " + reset)
            return
        
    def Enter(self):
        USERLOG.Log(self.m_name + " - entered login state.")
        self.m_connection.send(red + bold + "Welcome To SimpleMUD v1.0\r\n" + "Please enter your name, or \"new\" if you are new: " + reset)

    def GotoGame(self, p_newbie):
        p = playerDatabase.FindFull(self.m_name)
        
        if p.GetLoggedIn():
            p.GetClient().close()
        
        p.SetNewbie(p_newbie)
        p.SetConn(self.m_connection)
        p.GetConn().SwitchHandler(Game(p.Conn(), p.GetId()))
}