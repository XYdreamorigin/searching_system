#将所有文档内容进行分词，将每一篇文档分词结果保存在all_papers_vector.txt中
#将所有文档的倒排索引表保存在key_words.json中
import json
import jieba
import string
import re
sum_papers=120

#索引表
cut_all_papers_words={}
#所有文档的索引项作为向量，
all_papers_vector=[]

#将二维列表保存为文件
def save_list(list1,filename):
    file=open(filename+".txt",'w',encoding="utf-8")
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            file.write(str(list1[i][j]))
            file.write('\t')
        file.write('\n')
    file.close()

#将一篇文章分词，并将改词出现的位置记录下来
def Inverted_index(paper_number):
    #读文件
    # 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    file = open("all_papers/paper{}.json".format(paper_number),mode='r',encoding='utf-8')
    #载入文件获取数据
    data = json.load(file)
    #使用 jieba库进行分词
    cut_a_paper_words = " ".join(jieba.cut(data["info"]))
    print(type(cut_a_paper_words))
    #去除所有标点符号
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n。！\\\\’“”―，、0-9：《》（）；]+'
    cut_a_paper_words = re.sub(r, '', cut_a_paper_words)
    #字符串转化为列表，以空格分割
    cut_a_paper_words=cut_a_paper_words.split()
    #列表去重
    cut_a_paper_words=list(set(cut_a_paper_words))
    #print(cut_a_paper_words)

    #保存文档的索引为该文档的描述向量,这里是集合，转为列表类型
    all_papers_vector.append(cut_a_paper_words)
    
    
    #这篇文档中的每一个词，找到他在文档中的位置
    for word in cut_a_paper_words:
        dict={}
        list2=[]
        for station in re.finditer(word, data["info"]):
            #在文章中出现的位置
            list2.append(station.start())
            #在文章出现的位置记录下来
            dict['paper{}'.format(paper_number)]=list2
        # 如果这个关键词并未在索引值中记录
        if word not in cut_all_papers_words.keys():
            cut_all_papers_words[word]=dict
        #如果已经有这个键
        else:
            cut_all_papers_words[word].update(dict)
        #cut_all_papers_words.append(dict)

for i in range(1,sum_papers+1):
    Inverted_index(i)

save_list(all_papers_vector,"all_papers_vector")

# print(cut_all_papers_words)
json_string = json.dumps(cut_all_papers_words, ensure_ascii=False)
f = open('key_words.json', "w", encoding="utf-8")
f.write(json_string)
#print(json_string)