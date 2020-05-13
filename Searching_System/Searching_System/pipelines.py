# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
class SearchingSystemPipeline(object):
    #文档编号
    num = 1
    def process_item(self, item, spider):
        #打开一个文档
        self.file = open('all_papers/paper{}.json'.format(self.num), "w", encoding="utf-8")
        #文档编号加1
        self.num += 1
        # 生成字典对象
        dict_item = dict(item)
        # 生成json串
        json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
        # 将json串写入到文件中
        self.file.write(json_str)
        # 关闭文件
        self.file.close()
        return item
