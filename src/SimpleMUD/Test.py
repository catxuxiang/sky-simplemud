'''
Created on 2012-4-16

@author: sky
'''

class A:
    def __init__(self):
        self.A = "111"
        
class B(A):
    def __init__(self):
        A.__init__(self)
        self.B = "2222"
        
    def Test(self):
        print(self.A)
        
i = B()
i.Test()     
