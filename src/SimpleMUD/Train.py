'''
Created on 2012-5-18

@author: sky
'''
from BasicLib.BasicLibString import *
from SocketLib.ConnectionHandler import ConnectionHandler
from SimpleMUD.PlayerDatabase import playerDatabase
from SocketLib.Telnet import *
from SimpleMUD.Attributes import *

class Train(ConnectionHandler):
    def __init__(self, p_conn, p_player):
        ConnectionHandler.__init__(self, p_conn)
        self.m_player = p_player
        
    def Hungup(self):
        playerDatabase.Logout(self.m_player)
        
    def Flooded(self):
        playerDatabase.Logout(self.m_player)
        
    def Handle(self, p_data):
        p_data = ParseWord(p_data, 0).lower()
        
        p = self.m_player
        
        if p_data == "quit":
            # save the player to disk
            playerDatabase.SavePlayer(p)
            
            # go back to the previous handler
            p.GetConn().RemoveHandler()
            return
        
        n = p_data[0]
        if n >= "1" and n <= "3" and p.GetStatPoints() > 0:
            p.SetStatPoints(p.GetStatPoints() - 1)
            p.AddToBaseAttr(int(n) - 1, 1)
            
        self.PrintStats(True)
        
    def Enter(self):
        p = self.m_player
        
        p.SetActive(False)
        
        if p.GetNewbie():
            p.SendString(magenta + bold + \
            "Welcome to SimpleMUD, " + p.GetName() + "!\r\n" + \
            "You must train your character with your desired stats,\r\n" + \
            "before you enter the realm.\r\n\r\n")
            p.SetNewbie(False)
            
        self.PrintStats(False)
        
    def PrintStats(self, p_clear):
        p = self.m_player
        
        if p_clear:
            p.SendString(clearscreen)
            
        p.SendString(white + bold + \
        "--------------------------------- Your Stats ----------------------------------\r\n" + \
        "Player:           " + p.GetName() + "\r\n" + \
        "Level:            " + str(p.GetLevel()) + "\r\n" + \
        "Stat Points Left: " + str(p.GetStatPoints()) + "\r\n" + \
        "1) Strength:      " + str(p.GetAttr(Attribute_STRENGTH)) + "\r\n" + \
        "2) Health:        " + str(p.GetAttr(Attribute_HEALTH)) + "\r\n" + \
        "3) Agility:       " + str(p.GetAttr(Attribute_AGILITY)) + "\r\n" + \
        bold + \
        "-------------------------------------------------------------------------------\r\n" + \
        "Enter 1, 2, or 3 to add a stat point, or \"quit\" to enter the realm: ")
