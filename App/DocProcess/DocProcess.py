from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import csv
from App.TextRank import TextRank


def ReadDocx(str):
    document = Document(str)
    Title=""#标题
    Doucment_num=""#文档编号
    Text = ""#文档正文
    #获取标题
    Document_num_index=0;
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
            if(paragraph.runs[0].bold):#加粗是章节标题
                Sections.append(section)
                section=[]
                section.append(paragraph.text)
            else:
                section.append(paragraph.text)

    final=[];
    final.append(Title)
    final.append(Doucment_num)
    final.append(Text)
    final.append(Sections)
    return final


def SaveCsv(path,documentInfo):
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

        #关键词
        textRank = TextRank.TextRank(str(documentInfo[2]), 2, True, "./TextRank/cn_stopwords.txt", False)
        keyWords=textRank.get_n_keywords(10)#list of tuple
        #变为字符串
        keyWordsList=[item[0] for item in keyWords]
        row.append(" ".join(keyWordsList))
        row.append("")
        row.append("")
        row.append("")
        row.append("")
        csv_write.writerow(row)



if __name__ == "__main__":
    doxc = ReadDocx("Data/安监总管三〔2013〕88号.docx")
    SaveCsv("../../Data/Res.csv", doxc)

