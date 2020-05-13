

import re


def highlight_text(highlight_string, list_res):

    for idx in range(len(list_res)):
        item = list_res[idx]
        item = "\033[0;31m" + highlight_string + "\033[0m" + item.replace(highlight_string, "")
        list_res[idx] = item
    for item in list_res:
        print(item)


str="基本要求：自己动手设计实现一个信息检索系统，中、英文皆可，数据源可以自选，数据通过开源的网络爬虫获取，规模不低于100篇文档，" \
    "进行本地存储。中文可以分词（可用开源代码），也可以不分词，直接使用字作为基本单元。英文可以直接通过空格分隔。构建基本的倒排索" \
    "引文件。实现基本的向量空间检索模型的匹配算法。用户查询输入可以是自然语言字串，查询结果输出按相关度从大到小排序，列出相关度、" \
    "题目、主要匹配内容、URL、日期等信息。最好能对检索结果的准确率进行人工评价。界面不做强制要求，可以是命令行，也可以是可操作的" \
    "界面。提交作业报告和源代码"

list=["基本要求","动手","匹配"]


highlight_text(str,list)
print("\033[0;32;48m Bright Green")

for i in list:
    if i in str:
        print("\033[0;32;48m Bright Green")
    else:
        print("\033[0;30;48m ssssssssss")

import string

ss = 'Enter a short sequence:'

ls = 'Enter a long sequence:'

if (string.find(ls, ss) != -1):
    print ("find it")
else:
    print ("fail")
