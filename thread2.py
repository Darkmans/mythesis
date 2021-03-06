"""
author: Liaofan
GitHub: https://github.com/Darkmans
blog  : http://www.fanfanblog.cn | https://www.cnblogs.com/importthis
"""
import re
import time
import queue
import threading
import urllib.error
import urllib.request

urlqueue = queue.Queue()

headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0')
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)
listurl = []

def use_proxy(proxy_addr, url):
    try:
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print('exception:' + str(e))
        time.sleep(1)

class geturl(threading.Thread):
    def __init__(self, key, pagestart, pageend, proxy, urlqueue):
        threading.Thread.__init__(self)
        self.pagestart = pagestart
        self.pageend = pageend
        self.proxy = proxy
        self.urlqueue = urlqueue
        self.key = key
    def run(self):
        page = self.pagestart
        keycode urllib.request.quote(key)
        pagecode = urllib.request.quote('&page')
        for page in range(self.pagestart, self.pageend + 1):
            url = 'http://weixin.sogou.com/weixin?type=2&query=' + keycode + pagecode + str(page)
            data1 = use_proxy(self.proxy, url)
            listurlpat = '<div class="text-box">.*?(http://.*?)"'
            listurl.append(re.compile(listurlpat, re.S).findall(data1))
            print('获取到' + str(len(listurl)) + '页')
        for i in range(0, len(listurl)):
            time.sleep(7)
            for j in range(0. len(listurl[i])):
                try:
                    url = listurl[i][j]
                    url = url.replace('amp;', '')
                    print('第' + str(i) + 'i' + str(j) + 'j次入队')
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e, 'code'):
                        print(e.code)
                    if hasattr(e, 'reason'):
                        print(e.reason)
                    time.sleep(10)
                except Exception as e:
                    print('exception:' + str(e))
                    time.sleep(1)
                    
class getcontent(threading.Thread):
    def __init__(self, urlqueue, proxy):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        self.proxy =proxy
    def run(self):
        html1 = '''<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>微信文章页面</title>
    </head>
    <body>'''
    fh = open('/home/liaofan/my_thesis/5.html', 'wb')
    fh.write(html1.encode('utf-8'))
    fh.close()
    fh = open('/home/liaofan/my_thesis/5.html', 'ab')
    i = 1
    while True:
        try:
            url = self.urlqueue.get()
            data = use_proxy(self.proxy, url)
            titlepat = '<title>(.*?)</title>'
            contentpat = 'id="js_content">(.*?)id="js_sg_bar"'
            title = re.compile(titlepat).findall(data)
            content = re.compile(contentpat, re.S).findall(data)
            thistitle = '此次没有获取到'
            thiscontent = '此次没有获取到'
            if(title != []):
                thistitle = title[0]
            if(content != []):
                thiscontent = content[0]
            dataall = '<p>标题为：' + thistitle + "</p><p>内容为：" + thiscontent + '</p><br>'
            fh.write(dataall.encode('utf-8'))
            print('第' + str(i) + '个网页处理')
            i += 1
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
                time.sleep(10)
        except Exception as e:
            print('exception:' + str(e))
            time.sleep(1)
    fh.close()
    html2 = '''</body>
</html>'''
    fh = open('/home/liaofan/my_thesis/5.html', 'ab')
    fh.write(html2.encode('utf-8'))
    fh.close()
    
class control(threading.Thread):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
    def run(self):
        while True:
            print('程序正在执行中')
            time.sleep(60)
            if(self.urlqueue.empty()):
                print('程序执行完毕！')
                exit()
                
key = '江西财经大学'
proxy = '61.135.217.7:80'
proxy2 = ''
pagestart = 1
pageend = 4
t1 = geturl(key, pagestart, pageend, proxy, urlqueue)
t1.start()
t2 = getcontent(urlqueue, proxy)
t2.start()
t3 = control(urlqueue)
t3.start()
