#/usr/bin/python
import requests,re,time,os.path
import json
from bs4 import BeautifulSoup
from _pyio import open
from collections import deque
#模拟知乎登陆，主要是获取验证码登陆
_zhihu_url='http://www.zhihu.com'
_login_url=_zhihu_url+'/login/email'
_captcha_url=_zhihu_url+'/captcha.gif?r='
proxy = {
           'http' : '222.88.182.52:8000'
           }
header_data={'Accept':'*/*',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'108',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    ,'Host':'www.zhihu.com'
    ,'Origin':'http://www.zhihu.com'
    ,'Referer':'http://www.zhihu.com/'
    ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
    ,'X-Requested-With':'XMLHttpRequest'
    }
messageURL = 'http://www.zhihu.com/inbox/post'

import random
message_data = {}
class ZhiHu():

    _session=None
    #email=None,
    #password=None,
    #xsrf=None
    favor_data=100
    #question_url='http://www.zhihu.com/question/32120582'
    #path_for=None
    def __init__(self,email,pwd,proxy,uuwise):
        self.email = email
        self.pwd = pwd
        self.proxy = proxy
        self.uuwise = uuwise
        self.just_login()
    def get_captcha(self):
        return _captcha_url+str(int(time.time()*1000))
    def save_captcha(self,url,email):
        global _session
        r=_session.get(url,proxies=proxy)
        with open("./pic/code.gif",'wb') as f:
            f.write(r.content)

    def input_data(self):
#         global email
#         global password
        global captcha
        global question_url
#         self.email=input('plesae input your email:')
#         self.password=input('please input your password:')
        self.save_captcha(self.get_captcha(),self.email)
        
        self.captcha=self.uuwise.uu_getResult()
        print('get code complete')

      
    def login(self):
        global _session
        global header_data
        global xsrf
        r=_session.get('http://www.zhihu.com',proxies=proxy)
        self.xsrf=re.findall('xsrf(.*)',r.text)[0][8:42]
        self.input_data()
        
        
        login_data = {' _xsrf':self.xsrf,'email':self.email,'password':self.pwd,'rememberme':'true'
        ,'captcha':self.captcha}
        r=_session.post(_login_url,data=login_data,headers=header_data,proxies=proxy)
        j=r.json()
        print(j)
        c=int(j['r'])
        if c==0:
            print('sign in successful')
            #print(_session.cookies.get_dict())
            self.save_cookies(self.email)
            os.remove("./pic/code.gif")
        
        else:
            print('登陆出现问题。。。。尝试重新登录')
            self.login()
        

    def save_cookies(self,email):
        global _session,path_for
        with open('./'+email+"_cookiefile",'w')as f:
            json.dump(_session.cookies.get_dict(),f)
            #_session.cookies.save()

    def read_cookies(self):
        global _session,path_for
        #_session.cookies.load()
        #_session.headers.update(header_data)
        with open('cookiefile')as f:
            cookie=json.load(f)
            _session.cookies.update(cookie)
 
    def get_text(self,url,answers=15):
        global _session
        global favor_data
        r=_session.get(url,proxies=proxy)
        pat=re.compile('"count">(.*?)</span>')
        _list=re.findall(pat,r.text)
        for k in _list:
            if 'K' in k:
                length = len(k) - 1
                k = int(k[0:length]) * 1000
        favor_list=[int(k) for k in _list]
        favor_list.sort(reverse=True)
        if len(favor_list)>=answers:
            favor_data=favor_list[answers-1]
        else:
            favor_data=0
        self.save_text(r)

    def get_img(self,url):
        global  _session
        r=_session.get(url,proxies=proxy)
        pat_img=re.compile('<noscript><img src="([\s\S]*?)"')
        url_list=re.findall(pat_img,r.text)
        i=0
        try :   
            for img_url in url_list:
                with open(str(i)+'.jpg','bw')as f:
                    print('下载第'+str(i)+'张')
                    f.write(_session.get(img_url,proxies=proxy).content)
                i+=1
        except :
            print('可能出了一点问题。。。')
    
    def save_text(self,r):
        global path_for
        pattern_title=re.compile('<h2 class="zm-item-title zm-editable-content">\n\n([\s\S]*?)\n\n<\/h2>')
        pattern_desc=re.compile('<div class="zm-editable-content">([\s\S]*?)<\/div>')
        pattern_content=re.compile('<div class="zm-editable-content clearfix">([\s\S]*?)<\/div>')
        pattern=re.compile('div [\S\s]*?"count">(.*?)</span>[\s\S]*?clearfix">(.*)[\s\S]*?<\/div>')
        
        title=re.findall(pattern_title,r.text)
        desc=re.findall(pattern_desc,r.text)
        content=re.findall(pattern_content,r.text)
        #print(title,desc)
        #a=re.sub(re.compile('<br>'),'\n',r.text)
        answer_favor_list=re.findall(pattern,r.text)
        pat_sub=re.compile('<br>')
        with open('./'+title[0]+'.txt','w') as f:
            try:
                
                f.write('问题：'+title[0]+'\n\n')
                f.write('描述：'+desc[0]+'\n\n')
                i=0
                for answer in answer_favor_list:
                    if(int(answer[0])>favor_data):
                        f.write('\n-------------------''答案'+str(i)+'(赞同：'+answer[0]+')''---------------------\n')
                        f.write('\n答案'+str(i)+'(赞同：'+answer[0]+')-->'+re.sub(pat_sub,'\n',answer[1]))
                        f.write('\n'+content[i])
                        f.write('\n++++++++++++++++++++++++this answer is over++++++++++++++++++++++++++++++')
                        f.write('\n\n')
                    i+=1
            except Exception:
                print('可能在文件读写的时候出了一点问题。。。')
                
    def get_allfollers(self,user_url):
        global  _session
        follower_page = _session.get(user_url,proxies=proxy)
        soup = BeautifulSoup(follower_page.content, 'lxml')
#         followers = soup.findAll('a', {'class': 'zm-item-link-avatar'})
        followers_num = int(soup.find("div", {'class': 'zm-profile-side-following zg-clear'}).find_all("a")[1].strong.string)
        follerows_list = []  # store all followers' url
        cnt = 0
        for i in range(int((followers_num - 1) / 20 + 1)):
            cnt += 1
            if cnt > 10:
                break
            if i is 0:
                user_list = soup.find_all("h2", {'class': 'zm-list-content-title'})
                for tmp in user_list:
                    follerows_list.append(tmp.a['href'])
            else:
                post_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'
                _xsrf = soup.find('input', {'name': '_xsrf'})['value']
                offset = i * 20
                hash_id = re.findall('hash_id&quot;: &quot;(.*)&quot;},', follower_page.text)[0]
                params = json.dumps({'offset': offset, 'order_by': 'created', 'hash_id': hash_id})
                follower_data = {
                    '_xsrf': _xsrf,
                    'method': 'next',
                    'params': params
                }
                r_post = _session.post(post_url, data=follower_data, headers=header_data,proxies=proxy)
                followee_list = r_post.json()['msg']
#                 for j in range(min(followers_num - i * 20, 20)):
                for j in range(len(followee_list)):
                    followee_soup = BeautifulSoup(followee_list[j],'lxml')
                    user_link = followee_soup.find('h2', class_='zm-list-content-title').a['href']
                    follerows_list.append(user_link)
#         for i in follerows_list:
#             print(i)
        return follerows_list
    
    def getRandomStr(self):
        str_1 = random.choice(['Hi', 'Hello', '你好', '您好', 'Hi,你好', '你好啊', 'come on', 'HI', 'HELLO', '帅哥'])
        str_2 = random.choice(['我是', '在下', '俺', '洒家', '吾', '本人', '晚辈', '小弟', '老夫','贫道'])
        str_3 = '是'
        str_4 = random.choice(['关于', '那个', '那一个'])
        str_5 = '答案的答主，谢谢你的关注奥'
        return str_1 + str_2 + str_3 + str_4 + str_5
    
    def post_message(self,url):
        global _session
        content = self.getRandomStr()
        message_data['content'] = content
        profile_page = _session.get(url,proxies=proxy)
        soup = BeautifulSoup(profile_page.text, "lxml")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        member_id = soup.find('button', {'data-follow': 'm:button'}).get('data-id')
        message_data['_xsrf'] = xsrf
        message_data['member_id'] = member_id
        response = _session.post(messageURL, headers=header_data, data=message_data,proxies=proxy)
        time.sleep(5)
        print(response)
                
    def do_first(self):
        global _session
        _session=requests.session()
        if os.path.exists(self.email+'_cookiefile'):
            print(self.email+'---------------have cookies--------------------')
            self.read_cookies()
#             self.get_text(self.q_url)
#             self.get_img(self.q_url)
        else:
            self.login()
        
#         self.post_message(follower_urls)
    def just_login(self):
        global _session
        _session=requests.session()
        self.login() 
#         if os.path.exists(self.email+'_cookiefile'):
#             print(self.email+'---------------have cookies--------------------')
#             self.read_cookies()
# #             self.get_text(self.q_url)
# #             self.get_img(self.q_url)
#         else:
#             self.login()        
