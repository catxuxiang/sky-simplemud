'''
Created on 2012-5-14

@author: sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from BasicLib.BasicLibString import *
from SocketLib.Telnet import *
from BasicLib.BasicLibTime import TimeStamp, DateStamp, Timer
from SimpleMUD.Attributes import *
from SimpleMUD.PlayerDatabase import playerDatabase
from SimpleMUD.ItemDatabase import itemDatabase
from SimpleMUD.RoomDatabase import roomDatabase
from SimpleMUD.StoreDatabase import storeDatabase
from SimpleMUD.EnemyDatabase import enemyDatabase, enemyTemplateDatabase
from BasicLib.BasicLibLogger import USERLOG
from BasicLib.BasicLibRandom import RandomInt
from SimpleMUD.Train import Train

PLAYERITEMS = 16
class Game(ConnectionHandler):
    s_timer = Timer()
    s_running = False
    def __init__(self, p_conn, p_player):
        ConnectionHandler.__init__(self, p_conn)
        self.m_player = p_player
    
    @staticmethod   
    def GetTimer():
        return Game.s_timer
    
    @staticmethod
    def GetRunning():
        return Game.s_running
    
    @staticmethod
    def SetRunning(s_running):
        Game.s_running = s_running
        
    def Handle(self, p_data):
        p = self.m_player
        
        if p_data == "/":
            p_data = self.m_lastcommand
        else:
            self.m_lastcommand = p_data
            
        firstword = ParseWord(p_data, 0).lower()
        
        # ------------------------------------------------------------------------
        #  REGULAR access commands
        # ------------------------------------------------------------------------
        if firstword == "chat" or firstword == ":":
            text = RemoveWord(p_data, 0)
            self.SendGame(magenta + bold + p.GetName() + " chats: " + white + text)
            return
        
        if firstword == "experience" or firstword == "exp":
            p.SendString(self.PrintExperience())
            return
        
        if firstword == "help" or firstword == "commands":
            p.SendString(self.PrintHelp(p.GetRank()))
            return
        
        if firstword == "inventory" or firstword == "inv":
            p.SendString(self.PrintInventory())
            return
        
        if firstword == "quit":
            self.m_connection.Close()
            self.LogoutMessage(p.GetName() + " has left the realm.")
            return
        
        if firstword == "remove":
            self.RemoveItem(ParseWord(p_data, 1))
            return
        
        if firstword == "stats" or firstword == "st":
            p.SendString(self.PrintStats())
            return
        
        if firstword == "time":
            p.SendString( bold + cyan + "The current system time is: " + TimeStamp() + " on " + DateStamp() + "\r\nThe system has been up for: " + Game.s_timer.GetString() + "." )
            return
        
        if firstword == "use":
            self.UseItem(RemoveWord(p_data, 0))
            return
        
        if firstword == "whisper":
            name = ParseWord(p_data, 1)
            message = RemoveWord(RemoveWord(p_data, 0), 0)
            self.Whisper(message, name)
            return
        
        if firstword == "who":
            if(p_data.strip() == "who"):
                p.SendString(self.GetWhoList())
            else:
                p.SendString(self.GetWhoList("all"))
            return
        
        if firstword == "look" or firstword == "l":
            p.SendString(self.PrintRoom(p.GetCurrentRoom()))
            return
        
        if firstword == "north" or firstword == "n":
            self.Move(Direction_NORTH)
            return
        
        if firstword == "east" or firstword == "e":
            self.Move(Direction_EAST)
            return
        
        if firstword == "south" or firstword == "s":
            self.Move(Direction_SOUTH)
            return
        
        if firstword == "west" or firstword == "w":
            self.Move(Direction_WEST)
            return
        
        if firstword == "get" or firstword == "take":
            self.GetItem(RemoveWord(p_data, 0))
            return
        
        if firstword == "drop":
            self.DropItem(RemoveWord(p_data, 0))
            return
        
        if firstword == "train":
            if p.GetCurrentRoom().GetType() != RoomType_TRAININGROOM:
                p.SendString(red + bold + "You cannot train here!")
                return
            
            if p.Train():
                p.SendString(green + bold + "You are now level " + str(p.GetLevel()))
            else:
                p.SendString(red + bold + "You don't have enough experience to train!")
                
            return
        
        if firstword == "editstats":
            if p.GetCurrentRoom().GetType() != RoomType_TRAININGROOM:
                p.SendString(red + bold + "You cannot edit your stats here!")
                return
            
            self.GotoTrain()
            return
        
        if firstword == "list":
            if p.GetCurrentRoom().GetType() != RoomType_STORE:
                p.SendString(red + bold + "You're not in a store!")
                return
            
            p.SendString(self.StoreList(p.GetCurrentRoom().GetData()))
            return
        
        if firstword == "buy":
            if p.GetCurrentRoom().GetType() != RoomType_STORE:
                p.SendString(red + bold + "You're not in a store!")
                return
            
            self.Buy(RemoveWord(p_data, 0))
            return
        
        if firstword == "sell":
            if p.GetCurrentRoom().GetType() != RoomType_STORE:
                p.SendString(red + bold + "You're not in a store!")
                return
            
            self.Sell(RemoveWord(p_data, 0))
            return
        
        if firstword == "attack" or firstword == "a":
            self.PlayerAttack(RemoveWord(p_data, 0))
            return
        
        # ------------------------------------------------------------------------
        #  GOD access commands
        # ------------------------------------------------------------------------        
        if firstword == "kick" and p.GetRank() >= PlayerRank_GOD:
            k = playerDatabase.FindLoggedIn(ParseWord(p_data, 1))
            if k == None:
                p.SendString(red + bold + "Player could not be found.")
                return
            
            if k.GetRank() > p.GetRank():
                p.SendString(red + bold + "You can't kick that player!")
                return
            
            k.GetConn().Close()
            self.LogoutMessage(k.GetName() + " has been kicked by " + p.GetName() + "!!!")
            return
        
        # ------------------------------------------------------------------------
        #  ADMIN access commands
        # ------------------------------------------------------------------------
        if firstword == "announce" and p.GetRank() >= PlayerRank_ADMIN:
            self.Announce(RemoveWord(p_data, 0))
            return
        
        if firstword == "changerank" and p.GetRank() >= PlayerRank_ADMIN:
            name = ParseWord(p_data, 1)
            f = playerDatabase.Find(name)
            if f == None:
                p.SendString(red + bold + "Error: Could not find user " + name)
                return
            
            rank = self.GetRank(ParseWord(p_data, 2))
            f.SetRank(rank)
            self.SendGame( green + bold + f.GetName() + "'s rank has been changed to: " + GetRankString(rank))
            return
        
        if firstword == "reload" and p.GetRank() >= PlayerRank_ADMIN:
            db = ParseWord(p_data, 1).lower()
            
            if db == "items":
                itemDatabase.Load()
                p.SendString(bold + cyan + "Item Database Reloaded!")
            elif db == "player":
                user = ParseWord(p_data, 2)
                player = playerDatabase.FindFull(user)
                if player == None:
                    p.SendString(bold + red + "Invalid Player Name")
                else:
                    a = player.GetActive()
                    if a:
                        player.GetConn().Handler().Leave()
                    playerDatabase.LoadPlayer(player.GetName())
                    if a:
                        player.GetConn().Handler().Enter()
                        
                    p.SendString(bold + cyan + "Player " + player.GetName() + " Reloaded!")
            elif db == "rooms":
                roomDatabase.LoadTemplates()
                p.SendString(bold + cyan + "Room Template Database Reloaded!")
            elif db == "stores":
                storeDatabase.Load()
                p.SendString(bold + cyan + "Store Database Reloaded!")
            elif db == "enemies":
                enemyTemplateDatabase.Load()
                p.SendString(bold + cyan + "Enemy Database Reloaded!")
            else:
                p.SendString(bold + red + "Invalid Database Name")
            return
        
        if firstword == "shutdown" and p.GetRank() >= PlayerRank_ADMIN:
            self.Announce("SYSTEM IS SHUTTING DOWN")
            self.SetRunning(False)
            return
        
        # ------------------------------------------------------------------------
        #  Command not recognized, send to room
        # ------------------------------------------------------------------------
        Game.SendRoom(bold + p.GetName() + " says: " + dim + p_data, p.GetCurrentRoom())
        
    def Enter(self):
        USERLOG.Log(self.m_connection.GetRemoteAddress() + " - User " + self.m_player.GetName() + " entering Game state.")
        
        self.m_lastcommand = ""
        
        p = self.m_player
        p.GetCurrentRoom().AddPlayer(p)
        p.SetActive(True)
        p.SetLoggedIn(True)
        
        self.SendGame(bold + green + p.GetName() + " has entered the realm.")
        
        if p.GetNewbie():
            self.GotoTrain()
        else:
            p.SendString(self.PrintRoom(p.GetCurrentRoom()))
            
    def Leave(self):
        USERLOG.Log(self.m_connection.GetRemoteAddress() + " - User " + self.m_player.GetName() + " leaving Game state.")
        
        # remove the player from his room
        self.m_player.GetCurrentRoom().RemovePlayer(self.m_player)
        self.m_player.SetActive(False)
        
        # log out the player from the database if the connection has been closed
        if self.m_connection.Closed():
            playerDatabase.Logout(self.m_player)
            
    def Hungup(self):
        USERLOG.Log(self.m_connection.GetRemoteAddress() + " - User " + self.m_player.GetName() + " hung up.")
        p = self.m_player
        self.LogoutMessage(p.GetName() + " has suddenly disappeared from the realm.")
        
    def Flooded(self):
        USERLOG.Log(self.m_connection.GetRemoteAddress() + " - User " + self.m_player.GetName() + " flooded.")
        p = self.m_player
        self.LogoutMessage(p.GetName() + " has been kicked for flooding!")
        
    def SendGlobal(self, p_str):
        for i in playerDatabase.m_map.values():
            if i.GetLoggedIn():
                i.SendString(p_str)

    def SendGame(self, p_str):
        for i in playerDatabase.m_map.values():
            if i.GetActive():
                i.SendString(p_str)     
                
    def LogoutMessage(self, p_reason):
        self.SendGame(red + bold + p_reason)
        
    def Announce(self, p_announcement):
        self.SendGlobal(cyan + bold + "System Announcement: " + p_announcement)
        
    def Whisper(self, p_str, p_name):
        # find the player
        player = playerDatabase.FindActive(p_name)
        
        # if no match was found
        if player == None:
            self.m_player.SendString(red + bold + "Error, cannot find user.")
        else:
            player.SendString(yellow + self.m_player.GetName() + " whispers to you: " + reset + p_str)
            self.m_player.SendString(yellow + "You whisper to " + player.GetName() + ": " + reset + p_str)
            
    def GetWhoStr(self, p):
        string  = " " + p.GetName() + "| "
        string += str(p.GetLevel()) + "| "
        
        if p.GetActive():
            string += green + "Online  " + white
        elif p.GetLoggedIn():
            string += yellow + "Inactive" + white
        else:
            string += red + "Offline " + white

        string += " | "
        if p.GetRank() == PlayerRank_REGULAR:
            string += white
        elif p.GetRank() == PlayerRank_GOD:
            string += yellow
        elif p.GetRank() == PlayerRank_ADMIN:
            string += green
        string += GetRankString(p.GetRank())

        string += white + "\r\n"
        return string
            
    def GetWhoList(self, p_who = ""):
        string = (white + bold + 
        "--------------------------------------------------------------------------------\r\n" + 
        " Name             | Level     | Activity | Rank\r\n" + 
        "--------------------------------------------------------------------------------\r\n")
        
        whostr = ""
        if p_who == "all":
            for i in playerDatabase.m_map.values():
                whostr += self.GetWhoStr(i)
        else:
            for i in playerDatabase.m_map.values():
                if i.GetLoggedIn():
                    whostr += self.GetWhoStr(i)    
        
        string += whostr
        string += "--------------------------------------------------------------------------------"
        return string
    
    def PrintHelp(self, p_rank):
        help1 = white + bold + \
        "--------------------------------- Command List ---------------------------------\r\n" + \
        " /                          - Repeats your last command exactly.\r\n" + \
        " chat <mesg>                - Sends message to everyone in the game\r\n" + \
        " experience                 - Shows your experience statistics\r\n" + \
        " help                       - Shows this menu\r\n" + \
        " inventory                  - Shows a list of your items\r\n" + \
        " quit                       - Allows you to leave the realm.\r\n" + \
        " remove <'weapon'/'armor'>  - removes your weapon or armor\r\n" + \
        " stats                      - Shows all of your statistics\r\n" + \
        " time                       - shows the current system time.\r\n" + \
        " use <item>                 - use an item in your inventory\r\n" + \
        " whisper <who> <msg>        - Sends message to one person\r\n" + \
        " who                        - Shows a list of everyone online\r\n" + \
        " who all                    - Shows a list of everyone\r\n" + \
        " look                       - Shows you the contents of a room\r\n" + \
        " north/east/south/west      - Moves in a direction\r\n" + \
        " get/drop <item>            - Picks up or drops an item on the ground\r\n" + \
        " train                      - Train to the next level (TR)\r\n" + \
        " editstats                  - Edit your statistics (TR)\r\n" + \
        " list                       - Lists items in a store (ST)\r\n" + \
        " buy/sell <item>            - Buy or Sell an item in a store (ST)\r\n" + \
        " attack <enemy>             - Attack an enemy\r\n"
        
        god = yellow + bold + \
        "--------------------------------- God Commands ---------------------------------\r\n" + \
        " kick <who>                 - kicks a user from the realm\r\n"
        
        admin = green + bold + \
        "-------------------------------- Admin Commands --------------------------------\r\n" + \
        " announce <msg>             - Makes a global system announcement\r\n" + \
        " changerank <who> <rank>    - Changes the rank of a player\r\n" + \
        " reload <db>                - Reloads the requested database\r\n" + \
        " shutdown                   - Shuts the server down\r\n"
        
        end = white + bold + \
        "--------------------------------------------------------------------------------"
        
        if p_rank == PlayerRank_REGULAR:
            return help1 + end
        elif p_rank == PlayerRank_GOD:
            return help1 + god + end
        elif p_rank == PlayerRank_ADMIN:
            return help1 + god + admin + end
        else:
            return "ERROR"
    
    def PrintStats(self):
        p = self.m_player
        return white + bold + \
        "---------------------------------- Your Stats ----------------------------------\r\n" + \
        " Name:          " + p.GetName() + "\r\n" + \
        " Rank:          " + GetRankString(p.GetRank()) + "\r\n" + \
        " HP/Max:        " + str(p.GetHitPoints()) + "/" + str(p.GetAttr(Attribute_MAXHITPOINTS)) + \
        "  (" + str(p.GetHitPoints()/p.GetAttr(Attribute_MAXHITPOINTS)) + "%)\r\n" + \
        str(self.PrintExperience()) + "\r\n" + \
        " Strength:      " + str(p.GetAttr(Attribute_STRENGTH)) + \
        " Accuracy:      " + str(p.GetAttr(Attribute_ACCURACY)) + "\r\n" + \
        " Health:        " + str(p.GetAttr(Attribute_HEALTH)) + \
        " Dodging:       " + str(p.GetAttr(Attribute_DODGING)) + "\r\n" + \
        " Agility:       " + str(p.GetAttr( Attribute_AGILITY)) + \
        " Strike Damage: " + str(p.GetAttr(Attribute_STRIKEDAMAGE)) + "\r\n" + \
        " StatPoints:    " + str(p.GetStatPoints()) + \
        " Damage Absorb: " + str(p.GetAttr(Attribute_DAMAGEABSORB)) + "\r\n" + \
        "--------------------------------------------------------------------------------"
        
    def PrintExperience(self):
        p = self.m_player
        return white + bold + \
        " Level:         " + str(p.GetLevel()) + "\r\n" + \
        " Experience:    " + str(p.GetExperience()) + "/" + \
        str(p.NeedForLevel(p.GetLevel() + 1)) + " (" + \
        str(p.GetExperience()/p.NeedForLevel(p.GetLevel() + 1)) + \
        "%)"
        
    def PrintInventory(self):
        p = self.m_player
        
        itemlist = white + bold + \
        "-------------------------------- Your Inventory --------------------------------\r\n" + \
        " Items:  "
        
        for i in range(0, PLAYERITEMS):
            if p.GetItem(i) != None:
                itemlist += p.GetItem(i).GetName() + ", "
        itemlist = itemlist[0:len(itemlist) - 2]
        itemlist += "\r\n"
        
        itemlist += " Weapon: "
        if p.GetWeapon() == None:
            itemlist += "NONE!"
        else:
            itemlist += p.GetWeapon().GetName()
            
        itemlist += "\r\n Armor:  "
        if p.GetArmor() == None:
            itemlist += "NONE!"
        else:
            itemlist += p.GetArmor().GetName()
            
        itemlist += "\r\n Money:  $" + str(p.GetMoney())
        
        itemlist += "\r\n--------------------------------------------------------------------------------"
        
        return itemlist
    
    def UseItem(self, p_name):
        p = self.m_player
        i = p.GetItemIndex(p_name)
        
        if i == -1:
            p.SendString(red + bold + "Could not find that item!")
            return False
        
        itm = p.GetItem(i)
        if itm.GetType() == ItemType_WEAPON:
            p.UseWeapon(i)
            Game.SendRoom(green + bold + p.GetName() + " arms a " + itm.GetName(), p.GetCurrentRoom())
            return True
        elif itm.GetType() == ItemType_ARMOR:
            p.UseArmor(i)
            Game.SendRoom(green + bold + p.GetName() + " puts on a " + itm.GetName(), p.GetCurrentRoom())
            return True
        elif itm.GetType() == ItemType_HEALING:
            p.AddBonuses(itm)
            p.AddHitpoints(RandomInt(itm.GetMin(), itm.GetMax()))
            p.DropItem(i)
            Game.SendRoom(green + bold + p.GetName() + " uses a " + itm.GetName(), p.GetCurrentRoom())
            return True
        return False

    def RemoveItem(self, p_name):
        p = self.m_player
        p_name = p_name.lower()
        
        if p_name == "weapon" and p.GetWeapon() != None:
            Game.SendRoom(green + bold + p.GetName() + " puts away a " + p.GetWeapon().GetName(), p.GetCurrentRoom())
            p.RemoveWeapon()
            return True
        
        if p_name == "armor" and p.GetArmor() != None:
            Game.SendRoom(green + bold + p.GetName() + " takes off a " + p.GetArmor().GetName(), p.GetCurrentRoom())
            p.RemoveArmor()
            return True
        
        p.SendString(red + bold + "Could not Remove item!")
        return False
    
    def PrintRoom(self, p_room):
        desc = "\r\n" + bold + white + p_room.GetName() + "\r\n"
        desc += bold + magenta + p_room.GetDescription() + "\r\n"
        desc += bold + green + "exits: "
        for d in range(0, NUMDIRECTIONS):
            if p_room.GetAdjacent(d) != None:
                desc += DIRECTIONSTRINGS[d] + "  "
        desc += "\r\n"
        
        # ---------------------------------
        # ITEMS
        # ---------------------------------
        temp = bold + yellow + "You see: "
        count = 0
        if p_room.GetMoney() > 0:
            count += 1
            temp += "$" + p_room.GetMoney() + ", "
            
        for i in p_room.GetItems():
            count += 1
            temp += i.GetName() + ", "
            
        if count > 0:
            temp = temp[0:len(temp) - 2]
            desc += temp + "\r\n"
            
        # ---------------------------------
        # PEOPLE
        # ---------------------------------
        temp = bold + cyan + "People: "
        count = 0
        for i in p_room.GetPlayers():
            temp += i.GetName() + ", "
            count += 1
            
        if count > 0:
            temp = temp[0:len(temp) - 2]
            desc += temp + "\r\n"
            
        # ---------------------------------
        # ENEMIES
        # ---------------------------------
        temp = bold + red + "Enemies: "
        count = 0
        for i in p_room.GetEnemies():
            temp += i.GetName() + ", "
            count += 1
            
        if count > 0:
            temp = temp[0:len(temp) - 2]
            desc += temp + "\r\n"            

        return desc
    
    @staticmethod
    def SendRoom(p_text, p_room):
        #print("222" + str(p_room) + "111")
        for i in p_room.GetPlayers():
            i.SendString(p_text)
            
    def Move(self, p_direction):
        p = self.m_player
        next1 = p.GetCurrentRoom().GetAdjacent(p_direction)
        previous = p.GetCurrentRoom()
        
        if next1 == None:
            Game.SendRoom(red + p.GetName() + " bumps into the wall to the " + \
                  DIRECTIONSTRINGS[p_direction] + "!!!", \
                  p.GetCurrentRoom())
            return
        
        previous.RemovePlayer(p)
        
        Game.SendRoom(green + p.GetName() + " leaves to the " + \
              DIRECTIONSTRINGS[p_direction] + ".", \
              previous)
        Game.SendRoom(green + p.GetName() + " enters from the " + \
              DIRECTIONSTRINGS[OppositeDirection(p_direction)] + ".", \
              next1)
        p.SendString(green + "You walk " + DIRECTIONSTRINGS[p_direction] + ".")
        p.SetCurrentRoom(next1)
        next1.AddPlayer(p)
        
        p.SendString(self.PrintRoom(next1))
        
    def GetItem(self, p_name):
        p = self.m_player
        
        if p_name[0] == '$':
            # clear off the '$', and convert the result into a number.
            p_name = p_name[1:len(p_name)]
            m = int(p_name)
            
            # make sure there's enough money in the room
            if m > p.GetCurrentRoom().GetMoney():
                p.SendString(red + bold + "There isn't that much here!")
            else:
                p.SetMoney(p.GetMoney() + m)
                p.GetCurrentRoom().SetMoney(p.GetCurrentRoom().GetMoney() - m)
                Game.SendRoom( cyan + bold + p.GetName() + " picks up $" + m + ".", p.GetCurrentRoom())
            return
        
        i = p.GetCurrentRoom().FindItem(p_name)
        if i == None:
            p.SendString(red + bold + "You don't see that here!")
            return
        
        if not p.PickUpItem(i):
            p.SendString(red + bold + "You can't carry that much!")
            return
        
        p.GetCurrentRoom().RemoveItem(i)
        Game.SendRoom(cyan + bold + p.GetName() + " picks up " + i.GetName() + ".", p.GetCurrentRoom())
        
    def DropItem(self, p_name):
        p = self.m_player
        
        if p_name[0] == '$':
            # clear off the '$', and convert the result into a number.
            p_name = p_name[1:len(p_name)]
            m = int(p_name)
            
            # make sure there's enough money in the inventory
            if m > p.GetMoney():
                p.SendString(red + bold + "You don't have that much!")
            else:
                p.SetMoney(p.GetMoney() - m)
                p.GetCurrentRoom().SetMoney(p.GetCurrentRoom().GetMoney() + m)
                Game.SendRoom(cyan + bold + p.GetName() + " drops $" + m + ".", p.GetCurrentRoom())
            return
        
        i = p.GetItemIndex(p_name)
        if i == -1:
            p.SendString(red + bold + "You don't have that!")
            return
        Game.SendRoom(cyan + bold + p.GetName() + " drops " + \
                p.GetItem(i).GetName() + ".", p.GetCurrentRoom())
        p.GetCurrentRoom().AddItem(p.GetItem(i))
        p.DropItem(i)
        
    def GotoTrain(self):
        p = self.m_player
        p.SetActive(False)
        p.GetConn().AddHandler(Train(self.m_connection, p))
        self.LogoutMessage(p.GetName() + " leaves to edit stats")
        
    def StoreList(self, p_id):
        s = storeDatabase.GetValue(p_id)
        output = white + bold + \
              "--------------------------------------------------------------------------------\r\n"
        output += " Welcome to " + s.GetName() + "!\r\n"
        output += "--------------------------------------------------------------------------------\r\n"
        output += " Item                           | Price\r\n"
        output += "--------------------------------------------------------------------------------\r\n"
        
        for i in s.m_items:
            output += " " + i.GetName() + "| "
            output += i.GetPrice() + "\r\n"
        output += bold + \
              "--------------------------------------------------------------------------------\r\n"
        
        return output
    
    def Buy(self, p_name):
        p = self.m_player
        s = storeDatabase.GetValue(p.GetCurrentRoom().GetData())
        
        i = s.Find(p_name)
        if i == None:
            p.SendString(red + bold + "Sorry, we don't have that item!")
            return
        
        if p.GetMoney() < i.GetPrice():
            p.SendString(red + bold + "Sorry, but you can't afford that!")
            return
        
        if not p.PickUpItem(i):
            p.SendString(red + bold + "Sorry, but you can't carry that much!")
            return
        
        p.SetMoney(p.GetMoney() - i.GetPrice())
        Game.SendRoom(cyan + bold + p.GetName() + " buys a " + i.GetName(), p.GetCurrentRoom())
        
    def Sell(self, p_name):
        p = self.m_player
        s = storeDatabase.GetValue(p.GetCurrentRoom().GetData())
        
        index = p.GetItemIndex(p_name)
        if index == -1:
            p.SendString(red + bold + "Sorry, you don't have that!")
            return
        
        i = p.GetItem(index)
        if not s.Has(i):
            p.SendString(red + bold + "Sorry, we don't want that item!")
            return
        
        p.DropItem(index)
        p.SetMoney(p.GetMoney() + i.GetPrice())
        Game.SendRoom(cyan + bold + p.GetName() + " sells a " + i.GetName(), p.GetCurrentRoom())
    
    @staticmethod    
    def EnemyAttack(p_enemy):
        e = p_enemy
        r = e.GetCurrentRoom()
        
        p = r.GetPlayers()[RandomInt(0, len(r.GetPlayers()) - 1)]
        
        now = Game.GetTimer().GetMS()
        damage = 0
        if e.GetWeapon() == None:
            damage = RandomInt(1, 3)
            e.SetNextAttackTime(now + 1000)
        else:
            damage = RandomInt(e.GetWeapon().GetMin(), e.GetWeapon().GetMax())
            e.SetNextAttackTime(now + e.GetWeapon().GetSpeed()*1000)
        
        if RandomInt(0, 99) >= e.GetAccuracy() - p.GetAttr(Attribute_DODGING):
            Game.SendRoom(white + e.GetName() + " swings at " + p.GetName() + \
                        " but misses!", e.GetCurrentRoom())
            return
        
        damage += e.GetStrikeDamage()
        damage -= p.GetAttr(Attribute_DAMAGEABSORB)
        if damage < 1:
            damage = 1
        p.AddHitpoints(-damage)
        Game.SendRoom(red + e.GetName() + " hits " + p.GetName() + " for " + damage + " damage!", e.GetCurrentRoom())
        
        if p.GetHitPoints() <= 0:
            Game.PlayerKilled(p)
    
    @staticmethod
    def PlayerKilled(self, p_player):
        p = p_player
        Game.SendRoom(red + bold + p.GetName() + " has died!", p.GetCurrentRoom())
        
        # drop the money
        m = int(p.GetMoney() / 10)
        if m > 0:
            p.GetCurrentRoom().SetMoney(p.GetCurrentRoom().GetMoney() + m)
            p.SetMoney(p.GetMoney() - m)
            Game.SendRoom(cyan + "$" + m + " drops to the ground.", p.GetCurrentRoom())
            
        # drop an item
        if len(p.GetItems()) > 0:
            index = RandomInt(0, PLAYERITEMS - 1)
            while p.GetItem(index) == None:
                index = RandomInt(0, PLAYERITEMS - 1)
            i = p.GetItem(index)
            p.GetCurrentRoom().AddItem(i)
            p.DropItem(index)
            
            Game.SendRoom(cyan + i.GetName() + " drops to the ground.", p.GetCurrentRoom())
            
        # subtract 10% experience
        exp = int(p.GetExperience() / 10)
        p.SetExperience(p.GetExperience() - exp)
        
        # remove the player from the room and transport him to room 1.
        p.GetCurrentRoom().RemovePlayer(p_player)
        p.SetCurrentRoom(roomDatabase.GetValue("1"))
        p.GetCurrentRoom().AddPlayer(p_player)
        
        # set the hitpoints to 70%
        p.SetHitpoints(int(p.GetAttr(Attribute_MAXHITPOINTS) * 0.7))
        p.SendString(white + bold + "You have died, but have been ressurected in " + p.GetCurrentRoom().GetName())
        p.SendString(red + bold + "You have lost " + exp + " experience!")
        Game.SendRoom(white + bold + p.GetName() + " appears out of nowhere!!" , p.GetCurrentRoom())
        
    def PlayerAttack(self, p_name):
        p = self.m_player
        now = Game.GetTimer().GetMS()
        
        if now < p.GetNextAttackTime():
            p.SendString(red + bold + "You can't attack yet!")
            return
        
        ptr = p.GetCurrentRoom().FindEnemy(p_name)
        if ptr == None:
            p.SendString(red + bold + "You don't see that here!")
            return
        
        e = ptr
        damage = 0
        if p.GetWeapon() == None:
            damage = RandomInt(1, 3)
            p.SetNextAttackTime(now + 1000)
        else:
            damage = RandomInt(p.GetWeapon().GetMin(), p.GetWeapon().GetMax())
            p.SetNextAttackTime(now + p.GetWeapon().GetSpeed() * 1000)
        
        if RandomInt(0, 99) >= p.GetAttr(Attribute_ACCURACY) - e.Dodging():
            Game.SendRoom(white + p.GetName() + " swings at " + e.GetName() + \
                  " but misses!", p.GetCurrentRoom())
            return
        
        damage += p.GetAttr(Attribute_STRIKEDAMAGE)
        damage -= e.DamageAbsorb()
        
        if damage < 1:
            damage = 1
        
        e.SetHitPoints(e.GetHitPoints() - damage)
        Game.SendRoom(red + p.GetName() + " hits " + e.GetName() + " for " + damage + " damage!", p.GetCurrentRoom())
        
        if e.GetHitPoints() <= 0:
            self.EnemyKilled(e, self.m_player)
            
    def EnemyKilled(self, p_enemy, p_player):
        e = p_enemy
        Game.SendRoom(cyan + bold + e.GetName() + " has died!", e.GetCurrentRoom())
        
        # drop the money
        m = RandomInt(e.GetMoneyMin(), e.GetMoneyMax())
        if m > 0:
            e.GetCurrentRoom().SetMoney(e.GetCurrentRoom().GetMoney() + m)
            Game.SendRoom(cyan + "$" + m + " drops to the ground.", e.GetCurrentRoom())
            
        # drop all the items
        list1 = e.GetLootList()
        for i in list1.keys():
            if RandomInt(0, 99) < list1[i]:
                item = itemDatabase.GetValue(i)
                e.GetCurrentRoom().AddItem(item)
                Game.SendRoom(cyan + item.GetName() + " drops to the ground.", e.GetCurrentRoom())
                
        # add experience to the player who killed it
        p = p_player
        p.SetExperience(p.GetExperience() + e.GetExperience())
        p.SendString(cyan + bold + "You gain " + str(e.GetExperience()) + " experience.")
        
        # remove the enemy from the game
        enemyDatabase.Delete(p_enemy)


