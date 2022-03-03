import jieba
import re
from Util import words_info
import  numpy as np
class PreProcess:
    def __init__(self, filePath, use_stopwords,stopWordsFilePath=None):
        """
            filePath 原文件路径
            use_property: 是否根据词性进行筛选
            use_stopwords: 是用停用词
        """
        if(use_stopwords):
            #加载停用词
            self.stop_list = [line.strip() for line in open(stopWordsFilePath, 'r', encoding='utf-8').readlines()]
        with open(filePath, encoding='utf-8') as f:
            document = f.read()
            self.sents = self._split_scentence(document)
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

