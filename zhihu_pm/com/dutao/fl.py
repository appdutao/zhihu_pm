'''
Created on 2016-1-6

@author: Administrator
'''
import zh
import uuwise
u = uuwise.uuwise()    #创建验证码识别类
u.uu_login()    #uuwise账号登录，返回UU
account_default = 'kuang52199@163.com'
pwd_default = 'mix5300'
proxy_default = {'http' : '222.88.182.52:8000'}
default_zhihu = zh.ZhiHu(email=account_default, pwd=pwd_default, proxy=proxy_default,uuwise=u)
follower_urls = default_zhihu.get_allfollers("https://www.zhihu.com/people/zhou-you-rong/followers")
print(follower_urls)