#https://www.lunwendata.com/20.html
import scrapy
from Scripts.Searching_System.Searching_System.items import SearchingSystemItem
import re
import requests
class mySpider(scrapy.spiders.Spider):
    name="paper"
    allowed_domains="https://www.lunwendata.com"
    page=0
    start_url = "https://www.lunwendata.com/20_{}.html".format(page)
    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)
    def parse(self, response):  # 解析爬取的内容
        item=SearchingSystemItem()
        #//*[@id="articlelist"]/ul/li[1]
        #//*[@id="articlelist"]/ul/li[1]/a
        for each in response.xpath('//*[@id="articlelist"]/ul/li'):
            #获取文章标题
            item['title']=each.xpath('a/text()').extract()[0]
            #获取文章地址链接
            item['url']= each.xpath('a/@href').extract()[0]
            #调用函数all_info获取文档时间和具体内容
            item['time'],item['info']=self.all_info(item['url'])
            yield item
        if self.page < 5:
            self.page += 1
            new_url ="https://www.lunwendata.com/20_{}.html".format(self.page)
            yield response.follow(url=new_url, callback=self.parse, dont_filter=True)

    #获取到新的url后爬取这篇文章的详细内容
    def all_info(self,url):
        # 保存一整本书的列表，下面有多篇文章
        # 获取该网页的html文
        data = requests.get(url).text
        #对文档进行解码
        data=data.encode("latin1").decode("gbk")
        #使用正则匹配命令查找文档创建时间
        time=re.findall(r"时间：(.+?)</div>", data)
        #使用正则匹配对数据进行清洗，获得p标签下的数据
        info1=re.findall(r"<p>(.+?)</p>", data)
        #继续对数据进行清洗 ，去除p标签下的标签
        info2=""
        for i in info1:
            info2=info2+i;
        info3 = re.sub('<.*?>', '', info2)
        return time,info3
