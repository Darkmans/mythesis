"""
author: Liaofan
GitHub: https://github.com/Darkmans
blog  : http://www.fanfanblog.cn | https://www.cnblogs.com/importthis
"""
import re
import time
import urllib.error
import urllib.request

# 模拟浏览器
headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0')
opener = urllib.request.build_opener()
opener.addheaders = [headers]

# 将opener安装为全局
urllib.request.install_opener(opener)

# 设置一个列表listurl存储文章网址列表
listurl = []

# 功能为使用代理服务器
def use_proxy(proxy_addr, url):
    # 建立异常处理机制
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
        # 若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('exception:' + str(e))
        # 若为Exception异常，延时1秒执行
        time.sleep(1)

def getlisturl(key, pagestart, pageend, proxy):
    try:
        page = pagestart
        # 编码关键词key
        keycode = urllib.request.quote(key)
        # 编码"&page"
        pagecode = urllib.request.quote('&page')
        # 循环爬取各页文章链接
        for page in range(pagestart, pageend + 1):
            # 分别构建各页的url链接，每次循环构建一次
            url = 'http://weixin.sogou.com/weixin?type=2&query=' + keycode + pagecode + str(page)
            print(url)
            # 用代理服务器爬取，解决IP被封杀问题
            data1 = use_proxy(proxy, url)
            # 获取文章链接的正则表达式
            listurlpat = '<div class="txt-box">.*?(http://.*?)"'
            # 获取每页的所有文章链接并添加到列表listurl中
            listurl.append(re.compile(listurlpat, re.S).findall(data1))
        # 便于调试
        print('共获取到' + str(len(listurl)) + '页')
        return listurl
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        # 若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('exception:' + str(e))
        #  若为Exception异常，延时1秒执行
        time.sleep(1)

# 通过文章链接获取对应内容
def getcontent(listurl, proxy):
    i = 0
    # 设置本地文件中的开始html编码
    html1 = '''<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>微信文章页面</title>
    </head>
    <body>'''
    fh = open('/home/liaofan/my_thesis/4.html', 'wb')
    fh.write(html1.encode('utf-8'))
    fh.close()
    fh = open('/home/liaofan/my_thesis/4.html', 'ab')
    for i in range(0, len(listurl)):
        for j in range(0, len(listurl[i])):
            print('33')
            try:
                url = listurl[i][j]
                url = url.replace('amp;', '')
                data = use_proxy(proxy, url)
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
                print('第' + str(i) + '个网页第' + str(j) + '次处理')
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
    fh = open('/home/liaofan/my_thesis/4.html', 'ab')
    fh.write(html2.encode('utf-8'))

key = '江西财经大学'
proxy = '61.135.217.7:80'
proxy2 = ''
pagestart = 1
pageend = 4
listurl = getlisturl(key, pagestart, pageend, proxy)
print(listurl)
getcontent(listurl, proxy)
