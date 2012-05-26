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
        i = 0
        index = -1
        for sock in self.m_set:
            if sock == p_sock.GetSock():
                index = i
            i += 1
        if index != -1:
            del self.m_set[index]
    
    #p_time unit:second        
    def Poll(self, p_time = 0):
        self.m_activityset = []
        for i in self.m_set:
            self.m_activityset.append(i)
        infds,_,_ = select.select(self.m_activityset, [], [], p_time)
        return len(infds)
    
    def HasActivity(self, p_sock):
        for sock in self.m_activityset:
            if sock == p_sock.GetSock():
                return True
        return False
