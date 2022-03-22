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
from org.apache.lucene.index import LeafReaderContext

import logging

logger = logging.getLogger('logger')

class Indexer(object):
    def __init__(self):
        """
        初始化Indexer类
        :param Titles:标题列表
        :param Texts:文章正文列表
        """
        lucene.initVM()
        # self.Titles=Titles
        # self.Texts=Texts
        # self.ids=ids
        logger.info("Init Indexer")

    def SectionIndex(self,indexDir,sectionTexts,ids,DocTitle,path,config=None):
        """
        为文档的章节创建索引
        :param indexDir:创建后的索引所在文件夹
        :param sectionTexts:每个章节的文本组成的列表
        :param ids:章节在文档中对应的编号
        :param DocTitle:章节所对应的文章的题目
        :param path:章节所对应的文档的路径
        :param config:IndexWriter的config信息，IndexWriter控制从文档得到索引

        :return:
        """
        #配置config
        if(config==None):

            IndexerConfig=IndexWriterConfig(SmartChineseAnalyzer())
            IndexerConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
        else:
            IndexerConfig=config

        #构建indexerWriter实例
        _indexDir=FSDirectory.open(Paths.get(indexDir))
        _IndexerWriter=IndexWriter(_indexDir, IndexerConfig)

        # #得到当前已经索引的文件数量
        # reader = DirectoryReader.open(_indexDir)

        #创建索引
        logger.info("Document indexing...")
        nDocsAdded = 0
        for docNum in range(len(sectionTexts)):
            doc = Document()
            doc.add(IntPoint("id",int(ids[nDocsAdded])))
            doc.add(StoredField("id",int(ids[nDocsAdded])))
            doc.add(TextField("title", DocTitle, Field.Store.YES))
            doc.add(TextField("text", sectionTexts[docNum], Field.Store.NO))
            doc.add(TextField("path",path,Field.Store.YES))
            _IndexerWriter.addDocument(doc)
            nDocsAdded += 1
        logger.info("%d documents indexed",nDocsAdded)
        #print(nDocsAdded)
        _IndexerWriter.close()


class Searcher(object):
    def __init__(self):
        lucene.initVM()
        pass
    def NormalSearch(self,indexDir,queryStr):
        """
        使用索引进行常规查找
        :param indexDir:索引所在文件路径
        :param queryStr:用户的查找输入
        :return:
        """
        _indexDir=FSDirectory.open(Paths.get(indexDir))

        # 检查文件夹是否为合法的索引文件夹
        if(not DirectoryReader.indexExists(_indexDir)):
            return [],[],1

        reader = DirectoryReader.open(_indexDir)
        searcher=IndexSearcher(reader)

        analyzer=SmartChineseAnalyzer()
        parser=QueryParser("text",analyzer)
        query = parser.parse(queryStr)
        docs = searcher.search(query, 10)
        results=[]

        if(len(docs.scoreDocs)!=0):
            fields=[f.name() for f in searcher.doc(0).getFields()]
            # print(fields)
            for scoreDoc in docs.scoreDocs:
                res=[]
                doc = searcher.doc(scoreDoc.doc)
                res.append(doc.get("id"))
                res.append(doc.get("title"))
                res.append(doc.get("path"))
                results.append(res)
            return results,fields,0
        return results,[],2





if __name__ == '__main__':
    Titles=["标题1","标题2","标题3"]
    Texts=[
        "内容1内容啊哈哈哈",
        "内容2内容啊哈哈哈",
        "内容3内容啊哈哈哈"
    ]
    lucene.initVM()
    # indexer=Indexer()
    # indexer.SectionIndex("./test",Texts,[0,1,2],"cnm","../..")

    searcher=Searcher()
    res,field,flag=searcher.NormalSearch("../../Data/index","1")

    pass