# -*- coding: UTF-8 -*-  
# 全部函数列表：http://dll.uuwise.com/index.php?n=ApiDoc.AllFunc
# 技术QQ:87280085

from ctypes import *
import sys
import os
import hashlib
import binascii
import random

#reload(sys)                        #必须，不弄的话汉字有问题
#sys.setdefaultencoding('utf8')    #必须，不弄的话汉字有问题

class uuwise:

    def __init__(self):
        self.s_id  = 109639                                # 软件ID
        self.s_key = "f0a94711e4fd4b3ca3b33b100e4ee4f5"  # 软件Key 获取方式：http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY
        self.softVerifyKey="404BFBCD-C83A-4289-A2B0-4B6644AE407F";    #在开发者后台软件列表内获取，请勿泄露此KEY。图例：http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY
        
        
    #得到文件的MD5值函数
    def getFileMd5(self,strFile):  
        file = None;  
        bRet = False;  
        strMd5 = "";  
        try:  
            file = open(strFile, "rb");  
            md5 = hashlib.md5();  
            strRead = "";  
              
            while True:  
                strRead = file.read(8096);  
                if not strRead:  
                    break;  
                md5.update(strRead);  
            #read file finish  
            bRet = True;  
            strMd5 = md5.hexdigest();  
        except:  
            bRet = False;  
        finally:  
            if file:  
                file.close()  
      
        return [bRet, strMd5]; 
    
    #获取文件CRC32码
    def getFileCRC(self,filename):
        f = None;  
        bRet = False;
        crc = 0;
        blocksize = 1024 * 64
        try:
                    f = open(filename, "rb")
                    str = f.read(blocksize)
                    while len(str) != 0:
                            crc = binascii.crc32(str,crc) & 0xffffffff
                            str = f.read(blocksize)
                    f.close()
                    bRet = True; 
        except:
            print("compute file crc failed!"+filename)
            return 0
        return [bRet, '%x' % crc];
    
    #对服务器返回的识别结果进行校验
    def checkResult(self,dllResult, s_id, softVerifyKey, codeid):
        bRet = False;
        #服务器返回的是错误代码
        print(dllResult);
        print(len(dllResult));
        if(len(dllResult) < 0):
            return [bRet, dllResult];
        #截取出校验值和识别结果
        items=dllResult.split('_')
        verify=items[0]
        code=items[1]
    
        localMd5=hashlib.md5(('%d%s%d%s'%(s_id, softVerifyKey, codeid, (code.upper()))).encode("utf-8")).hexdigest().upper()
        if(verify == localMd5):
            bRet = True;
            return [bRet, code];
        return [bRet, "校验结果失败"]

    def uu_login(self):
        UUDLL=os.path.join(os.path.dirname(__file__), 'UUWiseHelper_x64.dll')                   #当前目录下的优优API接口文件
        # 加载动态链接库, 需要放在System 的path里，或者当前目录下
        UU = windll.LoadLibrary(UUDLL)
        
        getScore = UU.uu_getScoreW
        login = UU.uu_loginW
        checkAPi=UU.uu_CheckApiSignW    #api文件校验函数，调用后返回：MD5（软件ID+大写DLL校验KEY+大写随机值参数+优优API文件的MD5值+大写的优优API文件的CRC32值）
        
        #优优云DLL 文件MD5值校验
        #用处：近期有不法份子采用替换优优云官方dll文件的方式，极大的破坏了开发者的利益
        #用户使用替换过的DLL打码，导致开发者分成变成别人的，利益受损，
        #所以建议所有开发者在软件里面增加校验官方MD5值的函数
        #成功集成API文件校验的作者可免费联系客服获取100元充值卡
        
        
        dllMd5=self.getFileMd5(UUDLL);    #api文件的MD5值
        dllCRC32=self.getFileCRC(UUDLL);    #API文件的CRC32值
        randChar=hashlib.md5(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()').encode('utf-8')).hexdigest();    #随机字符串，用于让返回来的结果随机
        
        
        checkStatus=hashlib.md5(('%d%s%s%s%s'%(self.s_id,(self.softVerifyKey.upper()),(randChar.upper()),(dllMd5[1].upper()),(dllCRC32[1].upper()))).encode('utf-8')).hexdigest();        #服务器返回来的值与此值对应一至则表示成功
        
        #debugPoint = raw_input("Pleas input you user name and press enter:")
        serverStatus=c_wchar_p("");    #服务器返回来的结果,serverStatus和checkStatus值一样的话，就OK
        checkAPi(c_int(self.s_id), c_wchar_p(self.s_key.upper()),c_wchar_p(randChar.upper()),c_wchar_p(dllMd5[1].upper()),c_wchar_p(dllCRC32[1].upper()),serverStatus);  #调用检查函数,仅需要调用一次即可，不需要每次上传图片都调用一次
        #检查API文件是否被修改
        
        
        if not (checkStatus == serverStatus.value):
            print("sorry, api file is modified")    #如果API文件被修改，则终止程序
            sys.exit(0)    #终止程序
        
        user_i = "saqwcn"
        passwd_i = "DTDTDT"
        
        user = c_wchar_p(user_i)  # 授权用户名
        passwd = c_wchar_p(passwd_i)  # 授权密码
        
        
        #setSoftInfo(c_int(s_id), c_wchar_p(s_key))        #设置软件ID和KEY，仅需要调用一次即可，使用了checkAPi函数的话，就不用使用此函数了
        ret = login(user, passwd)                        #用户登录，仅需要调用一次即可，不需要每次上传图片都调用一次，特殊情况除外，比如当成脚本执行的话
        
        if ret > 0:
            print('login ok, user_id:%d' % ret)                 #登录成功返回用户ID
        else:
            print('login error,errorCode:%d' %ret )
            sys.exit(0)
        
        ret = getScore(user, passwd)                            #获取用户当前剩余积分
        print('The Score of User : %s  is :%d' % (user.value, ret))
        return UU
        
    def uu_getResult(self):   
        UUDLL=os.path.join(os.path.dirname(__file__), 'UUWiseHelper_x64.dll')                   #当前目录下的优优API接口文件
        # 加载动态链接库, 需要放在System 的path里，或者当前目录下
        UU = windll.LoadLibrary(UUDLL)
        # 初始化函数调用
        recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
        
        pic_file_path = os.path.join(os.path.dirname(__file__), 'pic', 'code.gif')   #测试图片文件
        #此处指的当前脚本同目录中test_pics文件夹下面的test.jpg
        #可以修改成你想要的文件路径     
        result=c_wchar_p("                                              ")    #分配内存空间，避免内存泄露
        code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(2002),result)
        if code_id <= 0:
            print('get result error ,ErrorCode: %d' % code_id)
        else:
            checkedRes=self.checkResult(result.value, self.s_id, self.softVerifyKey, code_id);
            return checkedRes[1]
#             print("the resultID is :%d result is %s" % (code_id,checkedRes[1]))  #识别结果为宽字符类型 c_wchar_p,运用的时候注意转换一下
