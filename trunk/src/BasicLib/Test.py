'''
Created on 2012-4-14

@author: Sky
'''
class A:
    A.a = 33
class B(A):
    def Test(self):
        print(self.a)
b = B()
b.Test()  
