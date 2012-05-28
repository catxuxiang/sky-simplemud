'''
Created on 2012-5-28

@author: Sky
'''
from redis.client import StrictRedis
sr = StrictRedis(host='localhost', port=6379, db=0)
