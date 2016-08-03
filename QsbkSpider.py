#-*_coding:utf8-*-
import requests
import re
import time


class spider(object):
    def __init__(self):
        print(u'开始爬取内容。。。')

#getsource用来获取网页源代码
    def getsource(self,url):
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                  ,'Referer':url+'/?s=4900467'}
        html = requests.get(url,headers = header)
        html.encoding = 'utf-8'
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('page/(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('page/\d+','page/%s'%i,url,re.S)
            page_group.append(link)
        return page_group
#geteveryclass用来抓取每个块的段子
    def getMessage(self,source):
        message = re.findall('<div class="content">(.*?)</div>',source,re.S)
        return message

#saveinfo用来保存结果到duanzi.txt文件中
    def saveinfo(self,message):
        linenum = 1;
        f = open('duanzi.txt','a',encoding='utf-8')
        for each in message:
            f.writelines(str(linenum)+ '、' + each + '\n\n')
            linenum = linenum + 1;
        f.close()

if __name__ == '__main__':
    allMessage = []
    url = 'http://www.qiushibaike.com/text/page/1'
    qsbk = spider()
    all_links = qsbk.changepage(url,35)
    count = 1;
    for link in all_links:
        print(u'正在处理页面：' + link)
        html = qsbk.getsource(link)
        message = qsbk.getMessage(html)
        for each in message:
            allMessage.append(each.replace('\n',''))
        count = count + 1;
        if (count == 4):
            time.sleep(3)
            count = 1
qsbk.saveinfo(allMessage)


