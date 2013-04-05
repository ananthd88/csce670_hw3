import HW3Document as Document
import HW3Index as Index
import math

class Collection:
   def __init__(self):
      #TODO modify this to a set instead of an array.
      self.documents = []
      self.hashTable = {}
      self.queries   = []
      self.index     = Index.Index()
      
   def addDocument(self, document):
      if self.hashTable.get(document, 0):
         print "Duplicate hashID found"
         return 0
      else:
         self.hashTable[document] = 1
         self.documents.append(document)
         self.index.processDocument(document)         
         return 1
   
   def printCollection(self):
      for document in self.documents:
         print self.queries[document.queryCode] + " -> " + document.title
   
   def computeAllTFIDF(self):
      print "Calculating TFIDF of every term in every doc..."
      numDocs = len(self.documents)
      logNumDocs = math.log(float(numDocs), 2)
      vocabulary = self.index.getVocabulary()
      for word in vocabulary.keys():
         postings = self.index.getPostings(word)
         df = len(postings)
         logdf = logNumDocs - math.log(float(df), 2)
         for (document, indexEntry) in postings.keys():
            tf = indexEntry.getCount()
            logtf = 1 + math.log(float(tf), 2)
            tfidf = logtf * logdf
            indexEntry.setTFIDF(tfidf)
            document.joinToIndex(word, indexEntry)
