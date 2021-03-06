# -*- coding: utf-8 -*-
import nltk
import string
import jieba.posseg as pseg
from heapq import nlargest
from nltk.tag import pos_tag
from string import punctuation
from inspect import getsourcefile
from collections import defaultdict
from nltk.tokenize import word_tokenize
from os.path import abspath, join, dirname
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import RegexpTokenizer
import re
import jieba


class Summarizer:
    """
    Input:
        text: 要处理文本
        lexical_chain: 构造好的词汇链
        n: 选取前n个结果
    Output:
        summary: 排序以后的前n个句子
    """

    def __init__(self, threshold_min=0.1, threshold_max=0.9):
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self._stopwords = set()#暂时没加载停用词列表



    def return_frequencies(self, words, lexical_chain):
        """
        依据词汇链对每一个句子中的词做一个词频字典，为后面排序做准备
        words:每个句子分词后的列表
        lexical_chain:词汇链
        """
        frequencies = defaultdict(int)
        for word in words:
            for w in word:
                # 词长度大于1且不在停用词列表
                if (w not in self._stopwords and len(word) > 1):
                    flag = 0
                    for i in lexical_chain:
                        # 如果在词汇链中就用词汇链的词频
                        if w in list(i.keys()):
                            frequencies[w] = sum(list(i.values()))
                            flag = 1
                            break
                    if flag == 0:
                        # 不在则加1
                        frequencies[w] += 1
        m = float(max(frequencies.values()))
        for w in list(frequencies.keys()):
            # 正则化
            frequencies[w] = frequencies[w] / m
            # 删除不要的数据
            if frequencies[w] >= self.threshold_max or frequencies[w] <= self.threshold_min:
                del frequencies[w]
        return frequencies



    def summarize(self, sentence, lexical_chain, n):
        """
        首先做一个排序，返回重要性最高的前n个句子
        sentence:section中的句子集合
        lexical_chain:词汇链
        n:前n个句子
        """
        assert n <= len(sentence)
        # word_sentence = [word_tokenize(s.lower()) for s in sentence]
        word_sentence = [list(jieba.cut(sent)) for sent in sentence]
        self.frequencies = self.return_frequencies(word_sentence, lexical_chain)
        ranking = defaultdict(int)

        # 排序，找出前n个句子
        for i, sent in enumerate(word_sentence):
            for word in sent:
                if word in self.frequencies:
                    ranking[i] += self.frequencies[word]
                    idx = self.rank(ranking, n)
        # 最后前n位的索引
        final_index = sorted(idx)
        return [sentence[j] for j in final_index]



    def rank(self, ranking, n):
        """
        找到前n大的值
        """
        return nlargest(n, ranking, key=ranking.get)


class LexicalChain:
    # 封装词汇链相关操作
    def __init__(self, input_text):
        # 原始文本
        self.original_text = input_text
        # 分句
        self.sentence = None
        # 分词
        self.tokens = None
        # 得到所有名词,展平
        self.nouns = None
        # 创建语义关系
        self.relation = None
        # 建立最初的词汇链
        self.lexical = None
        # 返回最终结果
        self.final_lexical = None

    def chinese_sent_tokenize(self, text):
        """
        中文分句,返回text分句后的结果
        text: 一段文本
        """
        sents_temp = re.split('(：|:|,|，|。|！|\!|\.|？|\?)', text)
        sents = []
        for i in range(len(sents_temp) // 2):
            sent = sents_temp[2 * i] + sents_temp[2 * i + 1]
            sents.append(sent)
        return sents

    def chinese_word_tokenize(self, str):
        """
        中文分词
        str：输入的一句话
        """
        # 去除标点
        str = str.replace('，', '').replace('。', '').replace('？', '').replace('；', ''). \
            replace('’', '').replace('·', '').replace('「', ''). \
            replace('、', '').replace('《', '').replace('》', ''). \
            replace('：', '').replace('（', '').replace('）', ''). \
            replace('(', '').replace(')', '').replace(' ', '').replace('】', ''). \
            replace('！', '').replace('【', '').replace('…', '').replace('“', ''). \
            replace('|', '').replace('[', '').replace(']', '').replace('-', ''). \
            replace('—', '').replace('\'', '').replace("*", '').replace('”', ''). \
            replace(' ', '').replace('　', '').replace('#', '').replace('+', ''). \
            replace(',', '').replace('/', '').replace('&', '').replace('～', '')
        # 分词
        document_cut = list(pseg.cut(str))
        position = ['n', 'nr', 'ns', 'nt', 'nz']
        # 只返回长度大于1的名词
        return [w.word for w in document_cut if (len(w.word) > 1 and w.flag in position)]

    def relation_list(self, nouns):
        """
        为每一个词创造词典，然后词典中存储与这个词有关的一系列词汇
        """
        relation_list = defaultdict(list)
        
        for k in range(len(nouns)):
            relation = []
            # 同义词集合
            for syn in wordnet.synsets(nouns[k], pos=wordnet.NOUN, lang='cmn'):
                for l in syn.lemmas():  # 同义关系
                    relation.append(l.name())
                    if l.antonyms():  # 反义
                        relation.append(l.antonyms()[0].name())
                for l in syn.hyponyms():  # 下位(子类)
                    if l.hyponyms():  #
                        relation.append(l.hyponyms()[0].name().split('.')[0])
                for l in syn.hypernyms():  # 上位(父类)
                    if l.hypernyms():
                        relation.append(l.hypernyms()[0].name().split('.')[0])
            relation_list[nouns[k]].append(relation)
        return relation_list

    def check_relation(self, word, l):
        """
        检查word的同义词、上位词、下位词是否在l中
        """
        for syn in wordnet.synsets(word, pos=wordnet.NOUN, lang='cmn'):
            for lemma in syn.lemmas():
                if (lemma.name() in l):
                    return True
            for h in syn.hyponyms():
                if (h.name() in l):
                    return True
            for h in syn.hypernyms():
                if (h.name() in l):
                    return True
        return False

    def create_lexical_chain(self, nouns, relation_list):
        """
        根据阈值以及词义相似关系选择性构造词汇链
        nouns:词汇列表
        relation_list:关系映射字典
        """
        lexical = []
        threshold = 0.5
        for noun in nouns:
            flag = 0
            for j in range(len(lexical)):
                if (flag == 0):
                    for key in list(lexical[j]):
                        if (key == noun and flag == 0):
                            # 如果key和noun是一个词，那么计数加1
                            lexical[j][noun] += 1
                            flag = 1
                        elif (self.check_relation(key, relation_list[noun][0]) and flag == 0):
                            syns1 = wordnet.synsets(key, pos=wordnet.NOUN, lang='cmn')
                            syns2 = wordnet.synsets(noun, pos=wordnet.NOUN, lang='cmn')
                            # syns1 = wordnet.synsets(key, pos=wordnet.NOUN)
                            # syns2 = wordnet.synsets(noun, pos=wordnet.NOUN)
                            if (syns1[0].wup_similarity(syns2[0]) >= threshold):
                                # 如果不是一个词但是之间有语义联系，则加入该词汇链
                                # print("in 1")
                                lexical[j][noun] = 1
                                flag = 1
                        elif (self.check_relation(noun, relation_list[key][0]) and flag == 0):
                            syns1 = wordnet.synsets(key, pos=wordnet.NOUN, lang='cmn')
                            syns2 = wordnet.synsets(noun, pos=wordnet.NOUN, lang='cmn')
                            # syns1 = wordnet.synsets(key, pos=wordnet.NOUN)
                            # syns2 = wordnet.synsets(noun, pos=wordnet.NOUN)
                            if (syns1[0].wup_similarity(syns2[0]) >= threshold):
                                # 如果不是一个词但是之间有语义联系，则加入该词汇链
                                # print("in 2")
                                lexical[j][noun] = 1
                                flag = 1
                else:
                    break
            if (flag == 0):
                dic_nuevo = {}
                dic_nuevo[noun] = 1
                lexical.append(dic_nuevo)
                flag = 1
        return lexical

    def prune(self, lexical):
        """
        过滤词汇链，删除只出现一次的
        """
        final_chain = []
        while lexical:
            result = lexical.pop()
            if len(result.keys()) == 1:
                for value in result.values():
                    if value != 1:
                        final_chain.append(result)
            else:
                final_chain.append(result)
        return final_chain

    def get_final_chain(self):
        # 得到最终的词汇链
        # 分句
        self.sentence = self.chinese_sent_tokenize(self.original_text)
        # 分词
        self.tokens = [self.chinese_word_tokenize(sent) for sent in self.sentence]
        # 得到所有名词,展平
        self.nouns = [word for token in self.tokens for word in token]
        # 创建语义关系
        self.relation = self.relation_list(self.nouns)
        # 建立最初的词汇链
        self.lexical = self.create_lexical_chain(self.nouns, self.relation)
        # 返回最终结果
        self.final_lexical = self.prune(self.lexical)
        return self.final_lexical

if __name__ == "__main__":

    """
    Read the .txt in this folder.
    """
    in_txt = join(dirname(abspath(getsourcefile(lambda:0))) , "chinese_input.txt")
    with open(in_txt, "r", encoding="utf-8" ) as f:
        input_txt = f.read()
        f.close()

    """
    Return the nouns of the entire text.
    """


    # # 分句
    # sentence = chinese_sent_tokenize(input_txt)
    #
    # # 分词
    # tokens = [chinese_word_tokenize(sent) for sent in sentence]
    #
    # # 得到所有名词并且去重
    # nouns =[word for token in tokens for word in token]
    # relation = relation_list(nouns)
    # lexical = create_lexical_chain(nouns, relation)
    chain=LexicalChain(input_txt)
    final_chain = chain.get_final_chain()
    """
    Print the lexical chain.
    """
    for i in range(len(final_chain)):
        print("Chain "+ str(i+1) + " : " + str(final_chain[i]))

    """
    Summarize the text taking into account the lexical chain and the number
    of sentence we want in the final summary.
    """
    if len(chain.sentence) >= 5:
        n = 5
    else:
        n = 2
    fs = Summarizer()
    for s in fs.summarize(chain.sentence, final_chain,n):
        print(s)
        print('----------------------------------------')

