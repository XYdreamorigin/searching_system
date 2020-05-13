import json
import re

import jieba

# 读文件里面的数据转化为二维列表

def Read_list(filename):
    file1 = open(filename+".txt", "r",encoding="utf-8")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
        list_source.append(column_list)                # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j]=list_source[i][j]
    file1.close()
    return list_source

def relevancy(number,str_query):
    query_vector=[]
    paper_vector=[]
    #建立文档向量
    for i in vocabulary:
        if i in vector[number]:
            paper_vector.append(1)
        else:
            paper_vector.append(0)
    #查询向量赋值
    for i in vocabulary:
        if i in str_query:
            query_vector.append(1)
        else:
            query_vector.append(0)
    #夹角余弦相关度的分子
    member=0
    sum_query=0
    sum_paper=0
    for i in range(len(vocabulary)):
        member=member+int(query_vector[i])*int(paper_vector[i])
        sum_query=sum_query+int(query_vector[i])
        sum_paper=sum_paper+int(paper_vector[i])
    #分母
    denominator=(sum_paper**0.5)*(sum_query**0.5)
    return member/denominator


if __name__ == '__main__':
    str_input = input("请输入查询信息：")
    # 将用户输入的自然语言进行分词
    str_query = " ".join(jieba.cut(str_input))
    # print(str_query)
    # 去除所有标点符号
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n。！\\\\’“”―，、0-9：《》（）；]+'
    str_query = re.sub(r, '', str_query)
    # 字符串转化为列表，以空格分割
    str_query = str_query.split()
    # 列表去重
    str_query = set(str_query)
    # print(cut_a_paper_words)s
    # print(sorted(list(str_query)))
    print("1.基于向量空间模型查询算法     2.基于倒排索引的查询算法")
    choose = input("请选择查询方式:")
    print(choose)
    choose=int(choose)
    if choose == 1:
        global vector
        vector = Read_list("all_papers_vector")
        # print(len(vector))
        # print(sorted(vector[0]))
        # 计算相关度,number为文档编号  paper1,number=1

        # 词汇表
        vocabulary = []
        for i in range(len(vector)):
            for j in range(len(vector[i])):
                vocabulary.append(vector[i][j])

        # 去重
        vocabulary = list(set(vocabulary))
        # 相关度列表
        relevancy_list = {}
        for i in range(120):
            relevancy_list["{}".format(i + 1)] = relevancy(i, str_query)
        # 排序输出
        relevancy_list = sorted(relevancy_list.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

        # print(relevancy_list)
        # print(relevancy_list[0])
        # print(type(relevancy_list[0]))
        # print(relevancy_list[0][0])

        print("以下是匹配结果(10个):\n")
        for i in range(10):
            f1 = open("all_papers/paper{}.json".format(i + 1), mode='r', encoding='utf-8')
            # 载入文件获取数据
            data = json.load(f1)
            print("相关度：{}\n".format(relevancy_list[i][1]))
            print("标题：{}\n".format(data['title']))
            print("网址：{}\n".format(data['url']))
            print("时间：{}\n".format(data['time'][0]))
            print("正文：{}\n".format(data["info"]))
    else:
        f2=open("key_words.json", mode='r', encoding='utf-8')
        info=json.load(f2)
        #关键字在这文档中出现的次数
        times={}
        #赋初始值=0
        for k in range(1,121):
            times['paper{}'.format(k)]=0

        #所有查询的关键词
        for i in str_query: #如果出现在文章中
            if i in info.keys():#将出现过得文档关键词出现的个数加1
                for j in info[i].keys():
                    times[j]=times[j]+1
        result=sorted(times.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
        for i in range(10):
            f3 = open("all_papers/{}.json".format(result[i][0]), mode='r', encoding='utf-8')
            # 载入文件获取数据
            paper_info = json.load(f3)
            print("匹配关键词个数：{}\n".format(result[i][1]))
            print("标题：{}\n".format(paper_info['title']))
            print("网址：{}\n".format(paper_info['url']))
            print("时间：{}\n".format(paper_info['time'][0]))
            print("正文：{}\n".format(paper_info["info"]))




