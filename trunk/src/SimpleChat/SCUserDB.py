'''
Created on 2012-5-3

@author: Sky
'''

class User:
    def __init__(self, c = None, n = ""):
        self.__init__()
        self.connection = c
        self.name = n
        
class UserDatabase:
    def __init__(self):
        self.m_users = []
        
    def Find(self, p_connection):
        for i in self.m_users:
            if i.connection == p_connection:
                return i
        return None
        
    def AddUser(self, p_connection, p_name):
        if not self.HasUser(p_name) and self.IsValidName(p_name):
            self.m_users.append(User(p_connection, p_name))
            return True
        return False
    
    def DeleteUser(self, p_connection):
        i = 0
        index = -1
        for user in self.m_users:
            if user.connection == p_connection:
                index = i
            i += 1
        if index != -1:
            del self.m_users[index]
            
    def HasUser(self, p_name):
        for user in self.m_users:
            if user.name == p_name:
                return True
        return False
        
    def IsValidName(self, p_name):
        inv = " \"'~!@#$%^&*+/\\[]{}<>()=.,?;:"
        for i in range(0, len(inv)):
            j = inv[i:i+1]
            if p_name.find(j) != -1:
                return False
            
        if len(p_name) > 16 or len(p_name) < 3:
            return False
    
        return True 

userDatabase = UserDatabase()


