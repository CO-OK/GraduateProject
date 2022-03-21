import os, sys, lucene

from java.nio.file import Paths
from java.lang import System
from java.text import DecimalFormat
from java.util import Arrays

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.search import IndexSearcher, TermQuery, MatchAllDocsQuery
from org.apache.lucene.store import FSDirectory, NIOFSDirectory
from org.apache.lucene.index import (IndexWriter, IndexReader,
                                     DirectoryReader, Term,
                                     IndexWriterConfig)
from org.apache.lucene.document import Document, Field, TextField,IntPoint,StoredField
from org.apache.lucene.facet import DrillSideways, DrillDownQuery
from org.apache.lucene.facet import (Facets, FacetField, FacetResult,
                                     FacetsConfig, FacetsCollector)
from org.apache.lucene.facet.taxonomy import FastTaxonomyFacetCounts
from org.apache.lucene.facet.taxonomy.directory import (DirectoryTaxonomyWriter,DirectoryTaxonomyReader)

from org.apache.lucene.search import Query
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis import TokenStream
from java.io import StringReader
from org.apache.lucene.search.highlight import Highlighter

import logging

logger = logging.getLogger('logger')

class Indexer(object):
    def __init__(self,Titles,Texts):
        """
        初始化Indexer类
        :param Titles:标题列表
        :param Texts:文章正文列表
        """
        self.Titles=Titles
        self.Texts=Texts
        logger.info("Init Indexer")

    def index(self,indexDir,config=None):
        """
        为文档创建索引
        :param indexDir:创建后的索引所在文件夹
        :param config:IndexWriter的config信息，IndexWriter控制从文档得到索引
        :return:
        """
        #配置config
        if(config==None):

            IndexerConfig=IndexWriterConfig(SmartChineseAnalyzer())
            IndexerConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        else:
            IndexerConfig=config

        #构建indexerWriter实例
        _indexDir=FSDirectory.open(Paths.get(indexDir))
        _IndexerWriter=IndexWriter(_indexDir, IndexerConfig)

        ids=[1,2,3]
        #创建索引
        logger.info("Document indexing...")
        nDocsAdded = 0
        for docNum in range(len(Texts)):
            doc = Document()
            doc.add(IntPoint("id",nDocsAdded))
            doc.add(StoredField("id",nDocsAdded))
            doc.add(TextField("title", Titles[docNum], Field.Store.YES))
            doc.add(TextField("text", Texts[docNum], Field.Store.YES))
            _IndexerWriter.addDocument(doc)
            nDocsAdded += 1
        logger.info("%d documents indexed",nDocsAdded)
        #print(nDocsAdded)
        _IndexerWriter.close()


class Seacher(object):
    def __init__(self):
        pass
    def NormalSearch(self,indexDir,queryStr):
        """
        使用索引进行常规查找
        :param indexDir:索引所在文件路径
        :param queryStr:用户的查找输入
        :return:
        """
        _indexDir=FSDirectory.open(Paths.get(indexDir))
        reader=DirectoryReader.open(_indexDir)
        searcher=IndexSearcher(reader)
        analyzer=SmartChineseAnalyzer()
        parser=QueryParser("text",analyzer)
        query = parser.parse(queryStr)
        docs = searcher.search(query, 10)


        for scoreDoc in docs.scoreDocs:

            doc = searcher.doc(scoreDoc.doc)
            tcontent = doc.get("text")
            id=doc.get("id")
            print(tcontent)
            print(id)
            # if(tcontent!=None):
            #     tokenStream = analyzer.tokenStream("text", StringReader(tcontent))
            #     summary = Highlighter.getBestFragment(tokenStream, tcontent)
            #     print(summary)




if __name__ == '__main__':
    Titles=["标题1","标题2","标题3"]
    Texts=[
        "内容1内容啊哈哈哈",
        "内容2内容啊哈哈哈",
        "内容3内容啊哈哈哈"
    ]
    lucene.initVM()
    indexer=Indexer(Titles,Texts)
    indexer.index("./test.Index")

    searcher=Seacher()
    searcher.NormalSearch("./test.Index","啊哈哈哈")