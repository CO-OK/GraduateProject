from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import csv
from App.TextRank import TextRank

class DocxProcess:
    def __init__(self,docxFilePath,numwords=10, windows=2,
                 use_stopwords=False, stopWordsFilePath=None,
                 pr_config={'alpha': 0.85, 'max_iter': 100}):
        """
        :param docxFilePath docx文档路径
        :param numwords: 关键词个数
        :param windows: 提取关键词时邻接矩阵的滑动窗口数
        :param use_stopwords: 是否使用停用词
        :param stopWordsFilePath:停用词列表的路径
        :param pr_config:提取关键词时的配置
        """
        self.DocxFilePath=docxFilePath
        self.NumWords=numwords
        self.windows=windows
        self.UseStopwords=use_stopwords
        self.StopwordsPath=stopWordsFilePath
        self.PrConfig=pr_config

    def GetKeyWords(self,text):
        """
        :param text:要提取关键词的文本2962466400
        :return: 关键词字符串
        """
        textRank=TextRank.TextRank(text,self.windows,self.UseStopwords,self.StopwordsPath,False,self.PrConfig)
        keywords=textRank.get_n_keywords(self.NumWords)
        res=""
        for item in keywords:
            res+=item[0]+" "
        return res


    def ReadDocx(self):
        """
        :param filePath: docx文件路径
        :return: 标题、文档编号、文档正文、文档关键词、正文文件(路径)、各个章节组成的列表
        """
        document = Document(self.DocxFilePath)
        Title=""#标题
        Doucment_num=""#文档编号
        Text = ""#文档正文
        #获取标题
        Document_num_index=0
        #从文章开始能够找到的所有居中的段落都算标题
        for i,paragraph in enumerate(document.paragraphs):
            if(paragraph.alignment==WD_ALIGN_PARAGRAPH.CENTER):
                Title+=paragraph.text+" "
                Document_num_index=i
            else:
                break
        #获取文档编号
        #按照安全总管系列的文章来说标题的最后一部分应该就是文章编号
        Doucment_num=document.paragraphs[Document_num_index].text

        #文档正文
        for paragraph in document.paragraphs:
            Text+=paragraph.text+"\n"

        #获取文档章节
        Sections=[]
        section=[]
        for i,paragraph in enumerate(document.paragraphs):
            if(i<=Document_num_index):
                continue
            else:#进入正文
                if(paragraph.text==""):continue#这段没有文字的话就继续
                if(paragraph.runs[0].bold):#加粗是章节标题
                    Sections.append(section)
                    section=[]
                    section.append(paragraph.text)
                else:
                    section.append(paragraph.text)
        if(len(section)!=0):
            Sections.append(section)
        final=[]
        final.append(Title)
        final.append(Doucment_num)
        final.append(Text)
        keywords=self.GetKeyWords(Text)#关键词
        final.append(keywords)
        final.append(self.DocxFilePath)
        final.append(Sections)
        return final


    def SaveCsv(self,path,documentInfo):
        """
        :param path:最后csv文件的保存路径
        :param documentInfo:已经解析好的文档相关信息
        :return:
        """
        with open(path,'w') as f:
            #后缀必须是csv才可以被创建
            csv_write = csv.writer(f)
            #先写入标题
            csv_head = ["文档编号","文档名称","正文","正文关键词","文档正文文件","文档附件","文档附件关键词","文档附件文件"]
            csv_write.writerow(csv_head)
            #再写入内容
            row=[]
            row.append(documentInfo[1])
            row.append(documentInfo[0])
            row.append(documentInfo[2])
            row.append(documentInfo[3])
            row.append(documentInfo[4])
            #关键词
            # textRank = TextRank.TextRank(str(documentInfo[2]), 2, True, "./TextRank/cn_stopwords.txt", False)
            # keyWords=textRank.get_n_keywords(10)#list of tuple
            #变为字符串
            # keyWordsList=[item[0] for item in keyWords]
            # row.append(" ".join(keyWordsList))
            # row.append("")
            row.append("")
            row.append("")
            row.append("")
            csv_write.writerow(row)





# if __name__ == "__main__":
#     doc=DocxProcess("../../Data/安监总管三〔2010〕186号.docx",use_stopwords=True, stopWordsFilePath="../TextRank/cn_stopwords.txt")
#     docinfo=doc.ReadDocx()
#     print(doc.GetKeyWords(docinfo[2]))
#     doc.SaveCsv("test.csv",docinfo)



