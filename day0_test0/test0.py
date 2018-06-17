#导入urllib中的urlopen函数
from urllib.request import urlopen
#导入BeautifulSoup对象
from bs4 import BeautifulSoup
#解决ssl报错
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
#打开url 获取网页内容
html = urlopen('https://www.csdn.net')
#将网页内容传给BeautifulSoup对象
bs_obj = BeautifulSoup(html.read(), 'html.parser')
#找出id=nav的侧边栏中的所有a标签
text_list = bs_obj.find(id="nav").find_all("a")

for text in text_list:
    #打印标签中的文本
    print(text.get_text())

html.close()


'''在python3中当用urllib.request.urlopen或者urllib.request.urlretrieve打开一个 https 的时候会验证一次 SSL 证书, 
当目标使用的是自签名的证书时就会爆出一个
URLError: urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:749)的错误消息;
解决方法：

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
'''