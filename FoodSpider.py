#-*_coding:utf8-*-
import requests
import re
import sys


class spider(object):
    def __init__(self):
        print(u'开始爬取内容。。。')

#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('page=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('page=\d+','page=%s'%i,url,re.S)
            page_group.append(link)
        return page_group
#geteveryclass用来抓取每个食物块的信息
    def geteveryfood(self,source):
        everyfood = re.findall('(<li class="item clearfix">.*?  </li>)',source,re.S)
        return everyfood


#getinfo用来从每个食物块中提取出我们需要的信息
    def getinfo(self,eachfood):
        # foodname = re.search('alt=(.*?)/></a>',eachfood,re.S).group(1).replace('\'','')
        # foodMessage = re.search('<p>(.*?)</p>',eachfood,re.S).group(1)
        imgURL = re.search('<img src=(.*?) alt=',eachfood,re.S).group(1).replace('\'','').replace('small','mid')
        return imgURL

#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,foodinfo):
        f = open('foodURL.txt','a',encoding='utf-8')
        for each in foodinfo:
            f.writelines('<item>'+each+'</item>\n')
        f.close()

if __name__ == '__main__':
    foodinfo = []
    url = 'http://www.boohee.com/food/view_menu?page=1'
    foodspider = spider()
    all_links = foodspider.changepage(url,10)
    for link in all_links:
        print(u'正在处理页面：' + link)
        html = foodspider.getsource(link)
        everyfood = foodspider.geteveryfood(html)
        for each in everyfood:
            info = foodspider.getinfo(each)
            foodinfo.append(info)
    foodspider.saveinfo(foodinfo)


