'''
Created on 2012-4-25

@author: sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from SocketLib.Telnet import *
from BasicLib.BasicLibLogger import USERLOG, ERRORLOG
from SimpleMUD.PlayerDatabase import playerDatabase
from SimpleMUD.RoomDatabase import roomDatabase
from SimpleMUD.Player import Player
from SimpleMUD.Attributes import *
from SimpleMUD.Game import Game

LogonState_NEWCONNECTION = 0
LogonState_NEWUSER = 1
LogonState_ENTERNEWPASS = 2
LogonState_ENTERPASS = 3

class Logon(ConnectionHandler):
    def __init__(self, p_conn):
        ConnectionHandler.__init__(self, p_conn)
        self.m_state = LogonState_NEWCONNECTION
        self.m_errors = 0
    
    def Hungup(self, ip):
        USERLOG.Log(ip + " - hung up in login state.")
 
    def Flooded(self, ip):
        USERLOG.Log(ip + " - flooded in login state.")
        
    def NoRoom(self, p_connection):
        msg = "Sorry, there is no more room on this server.\r\n"
        try:
            p_connection.Send(msg.encode("ascii"))
        except:
            ERRORLOG.Log("Logon's NoRoom Exception")
            
    def Handle(self, p_data):
        if self.m_errors == 5:
            self.m_connection.Protocol().SendString(self.m_connection, red + bold + "Too many incorrect responses, closing connection..." + newline)
            self.m_connection.close()
            return
        
        if self.m_state == LogonState_NEWCONNECTION:
            if p_data.lower() == "new":
                self.m_state = LogonState_NEWUSER
                self.m_connection.Protocol().SendString(self.m_connection, yellow + "Please enter your desired name: " + reset)
            else:
                playerdb = playerDatabase.FindFull(p_data)
                if(playerdb == None):
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, red + bold + "Sorry, the user \"" + white + p_data + red + "\" does not exist.\r\n" + "Please enter your name, or \"new\" if you are new: " + reset)
                else:
                    self.m_state = LogonState_ENTERPASS
                    self.m_name = p_data
                    self.m_pass = playerdb.GetPassword()
                    self.m_connection.Protocol().SendString(self.m_connection, green + bold + "Welcome, " + white + p_data + red + newline + green + "Please enter your password: " + reset)
            return
        
        if self.m_state == LogonState_NEWUSER:
            # check if the name is taken:
            if playerDatabase.HasFull(p_data):
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, \
                red + bold + "Sorry, the name \"" + white + p_data + red + \
                "\" has already been taken." + newline + yellow + \
                "Please enter your desired name: " + reset)
            else:
                if not self.AcceptibleName(p_data):
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, \
                    red + bold + "Sorry, the name \"" + white + p_data + red + \
                    "\" is unacceptible." + newline + yellow + \
                    "Please enter your desired name: " + reset)
                else:
                    self.m_state = LogonState_ENTERNEWPASS
                    self.m_name = p_data
                    self.m_connection.Protocol().SendString(self.m_connection, \
                        green + "Please enter your desired password: " + \
                        reset)
            return
     
        if self.m_state == LogonState_ENTERNEWPASS:
            if len(p_data.strip()) == 0:
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, red + bold + "INVALID PASSWORD!" + green + "Please enter your desired password: " + reset)
                return
            
            self.m_connection.Protocol().SendString(self.m_connection, green + "Thank you! You are now entering the realm..." + newline)
            p = Player()
            p.SetName(self.m_name)
            p.SetPassword(p_data)
            p.m_room = roomDatabase.GetValue(p.m_room)
            
            if playerDatabase.Size() == 0:
                p.SetRank(PlayerRank_ADMIN)
                p.SetId("1")
            else:
                p.SetId(str(int(playerDatabase.GetLastId()) + 1))
                
            playerDatabase.AddPlayer(p)
            self.GotoGame(True)
            return
        
        if self.m_state == LogonState_ENTERPASS:
            if self.m_pass == p_data:
                self.m_connection.Protocol().SendString(self.m_connection, green + "Thank you! You are now entering the realm..." + newline)
                self.GotoGame()
            else:
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, red + bold + "INVALID PASSWORD!" + newline + yellow + "Please enter your password: " + reset)
            return
        
    def Enter(self):
        USERLOG.Log(self.m_connection.GetRemoteAddress() + " - entered login state.")
        self.m_connection.Protocol().SendString(self.m_connection, red + bold + "Welcome To SimpleMUD v1.0\r\n" + "Please enter your name, or \"new\" if you are new: " + reset)

    def GotoGame(self, p_newbie = False):
        p = playerDatabase.FindFull(self.m_name)
        
        if p.GetLoggedIn():
            p.GetConn().Close()
            p.GetConn().Handler().Hungup()
            p.GetConn().ClearHandlers()
        
        p.SetNewbie(p_newbie)
        p.SetConn(self.m_connection)
        p.GetConn().SwitchHandler(Game(p.GetConn(), p))
        
    def AcceptibleName(self, p_name):
        if len(p_name) > 16 or len(p_name) < 3:
            return False
        if p_name == "new":
            return False        
        return True