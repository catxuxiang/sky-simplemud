'''
Created on 2012-5-5

@author: Sky
'''
import select

MAX = 64

class SocketSet:
    def __init__(self):
        self.m_set = []
        self.m_activityset = []
        
    def AddSocket(self, p_sock):
        # add the socket desc to the set
        self.m_set.append(p_sock.GetSock())
        
    def RemoveSocket(self, p_sock):
        index = 0
        i = -1
        for sock in self.m_set:
            if sock == p_sock.GetSock():
                i = index
            index += 1
        if i != -1:
            del self.m_set[i]
    
    #p_time unit:second        
    def Poll(self, p_time = 0):
        self.m_activityset = []
        for i in self.m_set:
            self.m_activityset.append(i)
        infds,outfds,errfds = select.select(self.m_activityset, [], [], p_time)
        return len(infds)
