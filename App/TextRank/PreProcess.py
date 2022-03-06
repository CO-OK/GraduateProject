import jieba
import re

import  numpy as np
class PreProcess:
    def __init__(self, filePath_str, use_stopwords,stopWordsFilePath=None,UseFilePath=True):
        """
            filePath_str 原文件路径或者是直接需要待处理的字符串，和UseFilePath在一起使用
                         当UseFilePath为False时filePath_str是文件在内存中的文本
                         当UseFilePath为True时filePath_str是待处理的文件路径，需要先读取该文件
            use_stopwords: 是否使用停用词
            stopWordsFilePath：通用词表路径
            UseFilePath：看第一条
        """
        if(use_stopwords):
            #加载停用词
            self.stop_list = [line.strip() for line in open(stopWordsFilePath, 'r', encoding='utf-8').readlines()]
        if(UseFilePath):
            with open(filePath_str, encoding='utf-8') as f:
                document = f.read()
                self.sents = self._split_scentence(document)
                self.words_pro = self._get_words(self.sents, use_stopwords)
        else:
            self.sents = self._split_scentence(filePath_str)
            self.words_pro = self._get_words(self.sents, use_stopwords)

    def _split_scentence(self,document):
        #文档分为一句一句
        document = [sentence for sentence in re.split('[。！？?!]', document)]
        return document

    def _get_words(self, sents,  use_stopwords):

        words = list()

        if len(sents) < 1:
            return None

        for s in sents:#分词
            s= s.replace('，', '').replace('。', '').replace('？', '').replace('；', ''). \
                replace('’', '').replace('·', '').replace('「', ''). \
                replace('、', '').replace('《', '').replace('》', ''). \
                replace('：', '').replace('（', '').replace('）', ''). \
                replace('(', '').replace(')', '').replace(' ', '').replace('】', ''). \
                replace('！', '').replace('【', '').replace('…', '').replace('“', ''). \
                replace('|', '').replace('[', '').replace(']', '').replace('-', ''). \
                replace('—', '').replace('\'', '').replace("*", '').replace('”', ''). \
                replace(' ', '').replace('　', '').replace('#', '').replace('+', ''). \
                replace(',', '').replace('/', '').replace('&', '').replace('～', '')
            cut_s  = jieba.cut(s,cut_all=False)

            #得到分词后的列表
            cut_s = [w for w in cut_s]

            #再次清洗
            cut_s = [word for word in cut_s if len(word) > 1]

            if use_stopwords:
                cut_s = [w.strip() for w in cut_s if w.strip() not in self.stop_list]
            words.append(cut_s)
        return words

