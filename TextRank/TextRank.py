from PreProcess import PreProcess
import Util

from collections import Counter


class TextRank(PreProcess):

    def __init__(self,
                 text=None, windows=2,
                 use_stopwords=True, stopWordsFilePath=None,
                 pr_config={'alpha': 0.85, 'max_iter': 100}):
        super(TextRank, self).__init__(text, use_stopwords, stopWordsFilePath)

        self.pr_config = pr_config
        self.windows = windows
        self.word_index, self.index_word, self.word_num = Util.words_info(self.words_pro)
        self.sorted_words = self._score_items(is_word=True)
        self.sorted_sents = self._score_items(is_word=False)

    def _build_adjacency_matrix(self, is_word=True):

        if is_word:
            adj_matrix = Util.word_adj_matrix(self.words_pro,
                                               self.windows,
                                               self.word_num,
                                               self.word_index)
        else:
            adj_matrix = Util.sent_adj_matrix(self.words_pro)

        return adj_matrix

    def _score_items(self, is_word=True):
        if is_word:
            adj_matrix = self._build_adjacency_matrix(is_word=is_word)
            scores = Util.cal_score(adj_matrix, **self.pr_config)
            sorted_items = Util.get_sorted_items(scores, self.index_word)
        else:
            adj_matrix = self._build_adjacency_matrix(is_word=is_word)
            scores = Util.cal_score(adj_matrix, **self.pr_config)
            index_sent = dict(zip(range(len(self.sents)), self.sents))
            sorted_items = Util.get_sorted_items(scores, index_sent)

        return sorted_items

    def get_n_keywords(self, N):
        return self.sorted_words[:N]

    def get_n_sentences(self, N):
        return self.sorted_sents[:N]

if __name__ == "__main__":
    #pre_process=PreProcess("test.txt",True,"./cn_stopwords.txt")
    textRank=TextRank("test.txt",2,True,"./cn_stopwords.txt")
    print(textRank.get_n_keywords(10))