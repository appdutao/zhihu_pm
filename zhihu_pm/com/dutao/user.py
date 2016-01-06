'''
Created on 2016-1-6
用于获取文本文件中的帐户名和密码
@author: dutao
'''
from collections import deque

class user:
    
    def __init__(self):
        self.account = deque()
        self.pwd = deque()
    
    def getUsername(self):
        with open("user.txt",'r') as f:
            for line in f:
                self.account.append(line.split('----')[0])
                self.pwd.append(line.split('----')[1].strip())
u = user()
u.getUsername()
print(u.account.popleft())