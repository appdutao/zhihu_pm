'''
Created on 2016-1-6

@author: dutao
'''
import user,uuwise
import zh
from collections import deque

#1.获取可用代理，返回deque
# pf = proxyFactory.ProxyFactory()
# pf.Run()
# proxyPairs = pf.proxyPairs
proxyList = [{'http': 'http://101.200.202.168:80'}, {'http': 'http://222.88.182.52:8000'}, {'http': 'http://101.26.38.162:83'}, {'http': 'http://222.89.107.137:8000'}, {'http': 'http://222.89.178.65:8000'}, {'http': 'http://123.54.0.18:8000'}, {'http': 'http://123.54.6.39:8000'}, {'http': 'http://58.252.2.5:8000'}, {'http': 'http://123.54.6.38:8000'}, {'http': 'http://110.52.232.45:8000'}, {'http': 'http://101.26.38.162:82'}, {'http': 'http://101.26.38.162:80'}, {'http': 'http://101.81.50.255:8118'}, {'http': 'http://119.188.115.27:80'}, {'http': 'http://117.169.66.230:80'}, {'http': 'http://112.25.185.171:8000'}, {'http': 'http://58.83.174.114:80'}, {'http': 'http://119.188.115.27:8088'}, {'http': 'http://223.68.133.236:8000'}, {'http': 'http://123.163.25.21:8000'}, {'http': 'http://183.247.158.197:80'}, {'http': 'http://123.163.52.24:8000'}, {'http': 'http://27.115.75.114:8080'}, {'http': 'http://58.20.232.245:8000'}, {'http': 'http://111.2.196.130:80'}, {'http': 'http://171.35.242.180:80'}, {'http': 'http://113.195.207.249:8000'}, {'http': 'http://222.89.238.61:80'}, {'http': 'http://58.252.8.25:8000'}, {'http': 'http://58.20.128.123:80'}, {'http': 'http://58.22.191.242:80'}, {'http': 'http://112.25.234.188:8000'}, {'http': 'http://221.213.51.82:8090'}, {'http': 'http://117.177.250.153:85'}, {'http': 'http://220.249.151.60:80'}, {'http': 'http://218.104.236.234:80'}, {'http': 'http://117.177.250.149:83'}, {'http': 'http://171.35.242.180:8000'}, {'http': 'http://117.177.250.154:84'}, {'http': 'http://110.52.232.75:8000'}, {'http': 'http://58.22.191.243:80'}, {'http': 'http://58.16.145.184:8000'}, {'http': 'http://117.177.250.151:86'}, {'http': 'http://111.1.89.254:80'}, {'http': 'http://117.177.250.149:84'}, {'http': 'http://120.194.85.49:8000'}]
proxyPairs = deque()
for i in proxyList:
    proxyPairs.append(i)
#2.获取user和pwd
user = user.user()
user.getUsername()
account = user.account
pwd = user.pwd
#uuwise登录
u = uuwise.uuwise()    #创建验证码识别类
u.uu_login()    #uuwise账号登录，返回UU
#获取被发送私信用户，返回list
# account_default = 'kuang52199@163.com'
# pwd_default = 'mix5300'
# proxy_default = {'http' : '222.88.182.52:8000'}
# default_zhihu = zh.ZhiHu(email=account_default, pwd=pwd_default, proxy=proxy_default,uuwise=u)
# follower_urls = default_zhihu.get_allfollers("https://www.zhihu.com/people/zhou-you-rong/followers")
follower_urls = ['https://www.zhihu.com/people/liu-chao-71-34', 'https://www.zhihu.com/people/a-tong-mu-50-66', 'https://www.zhihu.com/people/dong-shi-mei-32', 'https://www.zhihu.com/people/SHUAIBUHAUAI', 'https://www.zhihu.com/people/juan-xing-40', 'https://www.zhihu.com/people/wang-wang-4-97', 'https://www.zhihu.com/people/song-ling-shi-liao-31', 'https://www.zhihu.com/people/yi-zhong-zhi-57-89-65']
#五人一组，登录知乎，获取验证码
message_count = 0
proxy = None
zhihu_account = None
zhihu_pwd = None
temp_zhihu = None
for i in follower_urls:
    if message_count % 7 == 0:
        proxy = proxyPairs.popleft()
        zhihu_account = account.popleft()
        zhihu_pwd = pwd.popleft()
        print('以下发送的消息来自'+zhihu_account)
        temp_zhihu = zh.ZhiHu(email=zhihu_account, pwd=zhihu_pwd, proxy=proxy,uuwise=u)
    temp_zhihu.post_message(i)
    message_count += 1
    