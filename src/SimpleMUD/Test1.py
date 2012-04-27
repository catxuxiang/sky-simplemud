'''
Created on 2012-4-27

@author: sky
'''
from SimpleMUD.Test import A


class B(A):
    i = 2
    @staticmethod
    def Test1():
        print(B.i)
        
B.Test()  
B.Test1()      
