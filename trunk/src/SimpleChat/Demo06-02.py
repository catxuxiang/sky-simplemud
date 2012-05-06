'''
Created on 2012-5-5

@author: Sky
'''
from SocketLib.ListeningManager import ListeningManager
from SocketLib.ConnectionManager import ConnectionManager
from time import sleep

lm = ListeningManager()
cm = ConnectionManager(128, 60, 65536)

lm.SetConnectionManager(cm)
lm.AddPort(5098)

while True:
    lm.Listen()
    cm.Manage()
    sleep(1)