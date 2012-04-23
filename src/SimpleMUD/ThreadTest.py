'''
Created on 2012-4-23

@author: sky
'''
import threading, time
import sys

l = threading.Lock()

def PrintSleepThread():
    for i in range(0, 200):
        print(threading.currentThread().getName())
        #time.sleep(0.001)

def PrintThread():
    for i in range(0, 200):
        with l:
            for j in range(0, 50):
                sys.stdout.write(threading.currentThread().getName())
            sys.stdout.write("\n")
                
#a = threading.Thread(target = PrintThread, name = "a")
#b = threading.Thread(target = PrintThread, name = "b")
a = threading.Thread(target = PrintSleepThread, name = "a")
b = threading.Thread(target = PrintSleepThread, name = "b")
b.start()
a.start()
