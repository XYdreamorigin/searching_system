from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import jieba
import json
import re
import _thread
from time import *

class Application(Frame) :
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack( )
        self.create_widgets( )

        global vector, vocabulary
        vector = self.Read_list("all_papers_vector")
        vocabulary = []
        # 二维变一维
        for i in range(len(vector)):
            for j in range(len(vector[i])):
                vocabulary.append(vector[i][j])

        # 去重
        vocabulary = list(set(vocabulary))

    def create_widgets(self) :
        global  photo
        photo = PhotoImage(file="imgs/bupt.gif")
        self.label_photo=Label(self,image=photo)
        self.label_photo.pack(anchor=NW)
        self.label_photo.grid(rowspan=2,column=0)
        self.label_system=Label(self,text="信息检索系统",font=("华文行楷",100))#字体和字号
        self.label_system.grid(row=0,column=1,columnspan=3)
        self.label_byr = Label(self, text="陈萧尧\t  陈健\t邱诗媛", font=("华文行楷", 20))  # 字体和字号
        self.label_byr.grid(row=1, column=1,columnspan=3)

        self.search_by_title = Label(self, text="论文查找", font=("宋体", 15))  # 字体和字号
        self.search_by_title.grid(row=2, column=0,ipady=30)
        self.choose = StringVar();
        self.choose.set("B")
        self.r1 = Radiobutton(self, text="向量空间模型的查询算法", value="A", variable=self.choose,font=("宋体", 15))
        self.r2 = Radiobutton(self, text="基于倒排索引的查询算法", value="B", variable=self.choose,font=("宋体", 15))
        self.r1.grid(row=2, column=1)
        self.r2.grid(row=2, column=2)

        query_str_title = StringVar()
        self.query_str_title = Entry(self, textvariable=query_str_title,bd=3)
        self.query_str_title.grid(row=3, column=0,columnspan=3,sticky=EW)

        self.search_delete = Button(self, text="删除", font=("宋体", 15), bg="gray", command=self.search_delete)  # 字体和字号
        self.search_delete.grid(row=3, column=3,sticky=E)

        self.search_button = Button(self, text="搜索", font=("宋体", 15),bg="gray",command=self.search_paper)  # 字体和字号
        self.search_button.grid(row=3, column=3,sticky=W)

    def Read_list(self,filename):
        file1 = open(filename + ".txt", "r", encoding="utf-8")
        list_row = file1.readlines()
        list_source = []
        for i in range(len(list_row)):
            column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
            list_source.append(column_list)  # 在末尾追加到list_source
        # for i in range(len(list_source)):  # 行数
        #     for j in range(len(list_source[i])):  # 列数
        #         list_source[i][j] = list_source[i][j]
        file1.close()
        return list_source


    def search_delete(self):
        self.query_str_title.delete(0,END)
    def relevancy(self,number, str_query):
        query_vector = []
        paper_vector = []
        # 建立文档向量
        for i in vocabulary:
            if i in vector[number]:
                paper_vector.append(1)
            else:
                paper_vector.append(0)
        # 查询向量赋值
        for i in vocabulary:
            if i in str_query:
                query_vector.append(1)
            else:
                query_vector.append(0)
        # 夹角余弦相关度的分子
        member = 0
        sum_query = 0
        sum_paper = 0
        for i in range(len(vocabulary)):
            member = member + int(query_vector[i]) * int(paper_vector[i])
            sum_query = sum_query + int(query_vector[i])
            sum_paper = sum_paper + int(paper_vector[i])
        # 分母
        denominator = (sum_paper ** 0.5) * (sum_query ** 0.5)
        return member / denominator

    def relevancy_B(self,number, str_query):
        query_vector = []
        paper_vector = []
        # 建立文档向量
        for i in vocabulary:
            if i in vector[number-1]:
                paper_vector.append(1)
            else:
                paper_vector.append(0)
        # 查询向量赋值
        for i in vocabulary:
            if i in str_query:
                query_vector.append(1)
            else:
                query_vector.append(0)
        # 夹角余弦相关度的分子
        sum_query = 0
        sum_paper = 0
        for i in range(len(vocabulary)):
            sum_query = sum_query + int(query_vector[i])
            sum_paper = sum_paper + int(paper_vector[i])
        # 分母
        denominator = (sum_paper ** 0.5) * (sum_query ** 0.5)
        return denominator

    def CallOn(self,event):
        newwindow = Tk()
        newwindow.geometry("1200x800")
        sb = tk.Scrollbar(newwindow)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        text=Text(newwindow,height=1100,width=750,bd=2,bg="white",font=("宋体", 15))
        if str(self.choose.get()) == "A":
            f4 = open("all_papers/paper{}.json".format(self.result[self.paper_info1.curselection()[0]][0]), mode='r',
                        encoding='utf-8')
        else:
            f4 = open("all_papers/{}.json".format(self.result[self.paper_info1.curselection()[0]][0]), mode='r',
                      encoding='utf-8')
        #print(self.paper_info1.curselection()[0])
        #print(self.result[self.paper_info1.curselection()[0]][0])
        tempinfo = json.load(f4)
        text.insert(INSERT, tempinfo["title"])
        text.insert(INSERT, "\n\n")
        text.insert(INSERT, tempinfo["url"])
        text.insert(INSERT, "\n\n")
        text.insert(INSERT, tempinfo["time"])
        text.insert(INSERT, "\n\n")
        text.insert(INSERT,tempinfo["info"])
        #print(tempinfo)
        text.pack()


        newwindow.mainloop()
    def search_paper(self):
        #print(self.query_str_title.get())
        if self.query_str_title.get() != "":
            # 将用户输入的自然语言进行分词
            global str_query
            str_query = " ".join(jieba.cut(self.query_str_title.get()))
            # print(str_query)
            # 去除所有标点符号
            r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n。！\\\\’“”―，、0-9：《》（）；]+'
            str_query = re.sub(r, '', str_query)
            # 字符串转化为列表，以空格分割
            str_query = str_query.split()
            # 列表去重
            str_query = set(str_query)
            #print(self.choose.get())
            # self.paper_info1 = ScrolledText(self, bg="white", wrap=WORD)
            # self.paper_info1.grid(row=4, column=0, columnspan=4, sticky=EW, ipady=30)

            self.paper_info1 = Listbox(self)

            self.paper_info1.bind('<Double-Button-1>', self.CallOn)
            self.paper_info1.grid(row=4, column=0, columnspan=4, sticky=EW, ipady=30)
            # self.paper_info1.insert(END,"111")
            if str(self.choose.get()) == "A":
                try:
                    _thread.start_new_thread(self.vector_search, ("Thread-1", 2,))
                except:
                    print("Error: 无法启动线程")
                #self.vector_search()

            else:
                try:
                    _thread.start_new_thread(self.index_search, ("Thread-2", 4,))
                except:
                    print("Error: 无法启动线程")
                #self.index_search()

    def insert(self, str):
        self.paper_info1.insert(INSERT, str + '\n')
        self.paper_info1.see(END)

    def vector_search(self, threadName, delay):
        # 相关度列表
        relevancy_list = {}
        for i in range(120):
            relevancy_list["{}".format(i + 1)] = self.relevancy(i, str_query)
        # 排序输出
        self.result = sorted(relevancy_list.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

        for i in range(120):
            if (self.result[i][1] == 0):
                break
            f1 = open("all_papers/paper{}.json".format(self.result[i][0]), mode='r', encoding='utf-8')
            # 载入文件获取数据
            data = json.load(f1)
            self.paper_info1.insert(END,"标题：{}\n".format(data['title'])+"   相关度：{}\n".format(self.result[i][1]))


    def index_search(self, threadName, delay):
        f2 = open("key_words.json", mode='r', encoding='utf-8')
        info = json.load(f2)
        # 关键字在这文档中出现的次数
        times = {}
        # 赋初始值=0
        for k in range(1, 121):
            times['paper{}'.format(k)] = 0

        # 所有查询的关键词
        for i in str_query:  # 如果关键字出现在文章中
            if i in info.keys():  # 将出现过得文档关键词出现的个数加1
                for j in info[i].keys():
                    times[j] = times[j] + 1

        for j in range(1, 121):
            if(self.relevancy_B(j, str_query)!=0):
                times['paper{}'.format(j)] = times['paper{}'.format(j)] / self.relevancy_B(j, str_query)
        self.result = sorted(times.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
       # print(self.result)
        #self.paper_info1.insert(END,"以下是匹配结果(10个):\n")
        for i in range(120):
            if (self.result[i][1] == 0):
                break
            f3 = open("all_papers/{}.json".format(self.result[i][0]), mode='r', encoding='utf-8')
            # 载入文件获取数据
            paper_info = json.load(f3)
            self.paper_info1.insert(END,"标题：{}\n".format(paper_info['title'])+"   相关度：{}\n".format(self.result[i][1]))


root=Tk( )
root.geometry("1200x800")
root.title("信息检索系统")
app= Application (master=root)
root.resizable(width=False, height=True)
root.mainloop( )
