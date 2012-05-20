'''
Created on 2012-5-20

@author: sky
'''
from SimpleMUD.GameLoop import GameLoop
from SocketLib.ListeningManager import ListeningManager
from SocketLib.ConnectionManager import ConnectionManager
from SimpleMUD.Game import Game
from time import sleep

gameloop = GameLoop()

lm = ListeningManager()
cm = ConnectionManager(128, 60, 65536)

lm.SetConnectionManager(cm)
lm.AddPort(5098)


while Game.GetRunning():
    lm.Listen()
    cm.Manage()
    gameloop.Loop()
    sleep(1)
