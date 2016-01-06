import urllib.request
import time
from selenium import webdriver
import queue
from collections import deque
from multiprocessing import process


class Proxy:
    def __init__(self, addr, time):
        self.address = addr
        self.time = time
    def __lt__(self, other):
        return self.time < other.time

class ProxyFactory:

    def __init__(self):
        
        self.pool = []
        self.proxyPairs = deque()
    
    def Run(self):
        proxyList = self.FetchProxies()

        #print(proxyList) 
        
        self.ValidateProxies(proxyList)
        
        self.pool.sort()
        
        for i in self.pool:
            temp = {
                    'http' : i.address
            }
            self.proxyPairs.append(temp)
#             self.proxyPairs += [(i.address, i.time)]


    def FetchProxies(self):
        
        print("fetching proxy list...")
        u = "http://www.freeproxylists.net/zh/?c=cn&f=1&s=u"
        service_args = [
         '--proxy=127.0.0.1:1080',
         '--proxy-type=http',
         ]
        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get(u)
        rows = driver.find_elements_by_css_selector("table > tbody > tr")
        proxies = []
        for i in rows:
            if i.text.find("HTTP") != -1:
                cells = i.text.split()
                proxies += ["http://{0}:{1}".format(cells[0], cells[1])]
        proxies = proxies[1:]
        print("{0} fetched".format(len(proxies)))
        return proxies
    
    def CheckProxy(self, address, tests, result):
        for t in tests:
            proxy=urllib.request.ProxyHandler({'http': address})
            opener=urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]
            try:
                start = time.clock()
                #data = opener.open(url = t, timeout = 5).read().decode()
                data = opener.open(t, timeout = 5).read().decode()
                end = time.clock()
#                 print("[Proxy {0}]: OK for {1} in time: {2} s".format(address, t, end - start))
                result.put((address, end - start))
            except Exception as e:
                print(e)
                print("[Proxy {0}]: not available".format(address))
    
    def ValidateProxies(self, proxyList):
            
        maxProc = 5
        
        tests = ["http://www.baidu.com"]
    
        result = queue.Queue()
       
        start = time.clock()
        
        for i in proxyList:
#             p = multiprocessing.process.BaseProcess(target=self.CheckProxy, args=(i, tests, result))
#             p.start()  
#             if len(process.active_children()) > maxProc:
#                 print('active_children: ', process.active_children())
#                 p.join()
            self.CheckProxy(i, tests, result);
            
#         while len(process.active_children()) > 0:
#             time.sleep(3)
        end = time.clock()
        print("total time for validation:", end - start, "s")
        
        self.pool = []
        
        for i in range(result.qsize()):
            a = result.get()
            self.pool += [Proxy(a[0], a[1])]

        
        print("{0} validated".format(len(self.pool)))

pf = ProxyFactory()
pf.Run()
print(pf.proxyPairs)        
# pf = ProxyFactory()
# pf.Run()
# for i in range(len(pf.proxyPairs)):
#     print(pf.proxyPairs.popleft())
