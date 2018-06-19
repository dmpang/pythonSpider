from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv

#设置UA标识
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 "
)
driver = webdriver.PhantomJS(executable_path='phantomjs', desired_capabilities=dcap)

#构造百度音乐歌单首页
pageNum = 1
url = '%s%d%s' % ('http://music.baidu.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset=', 20*pageNum, '&third_type=')

#创建歌单csv文件
csv_file = open("songlist.csv", "w", newline='', encoding='utf_8_sig')
write = csv.writer(csv_file)
write.writerow(['标题', '播放数', '封面链接', '歌单链接'])

while 1:
    #找到歌单内容存放位置
    driver.get(url)
    data = driver.find_element_by_class_name("songlist-list").find_element_by_tag_name("ul").\
        find_elements_by_tag_name("li")
    #最后一页跳出循环
    if len(data) == 0:
        break

    #解析当前页歌单列表
    for i in range(len(data)):
        num = data[i].find_element_by_class_name("num").text
        #获取播放数大于500万的歌单
        if '万' in num and int(num.split("万")[0]) > 200:
            wrap = data[i].find_element_by_class_name("img-wrap").\
                find_element_by_tag_name("img")
            songListTitle = data[i].find_element_by_class_name("text-title").\
                find_element_by_tag_name("a")
            #输出歌单名等信息
            print(songListTitle.get_attribute('title'),
                  num, wrap.get_attribute('src'),
                  songListTitle.get_attribute('href'))
            #写入csv文件
            write.writerow([songListTitle.get_attribute('title'),
                            num, wrap.get_attribute('src'),
                            songListTitle.get_attribute('href')])
        #构造下一页url
        pageNum += 1
        url = '%s%d%s' % ('http://music.baidu.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset=', 20*pageNum, '&third_type=')

csv_file.close()
