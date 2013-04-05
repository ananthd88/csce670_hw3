import HW3Index as Index
import re
import math

class Document:
   numOfDocsCreated = 0
   def __init__(self, dictionary, queryCode):
      Document.numOfDocsCreated += 1
      self.id           = Document.numOfDocsCreated
      
      self.title        = dictionary.get("Title", "").lower()
      self.url          = dictionary.get("Url", "").lower()
      self.source       = dictionary.get("Source", "").lower()
      self.description  = dictionary.get("Description", "").lower()
      self.queryCode    = queryCode      
      self.tfidfVector  = {}
      self.tfidfLength  = -1
      self.cluster      = False
      self.tempCluster  = False
   
   def __hash__(self):
      return hash(self.title)
   
   def __eq__(self, other):
      return (self.title, self.url, self.source, self.description) == (other.title, other.url, other.source, other.description)
   
   def getTFIDF(self, word):
      #TODO: Remove the calls to lower() for all methods in this class?
      word = word.lower()
      indexEntry = self.tfidfVector.get(word, Index.IndexEntry())
      return indexEntry.getTFIDF()
   
   def joinToIndex(self, word, indexEntry):
      word = word.lower()
      self.tfidfVector[word] = indexEntry
   
   def getBagOfWords(self):
      array1 = re.split('[^a-zA-Z0-9_@]', self.title)
      array2 = re.split('[^a-zA-Z0-9_@]', self.description)
      bagOfWords = array1 + array2
      return bagOfWords
   
   def getSetOfWords(self):
      return set(self.tfidfVector.keys())
      
   def computeTFIDFLength(self):
      self.tfidfLength  = 0
      for word in self.tfidfVector:
         tfidf = self.getTFIDF()
         self.tfidfLength  += tfidf * tfidf
      self.tfidfLength  = math.sqrt(self.tfidfLength)
      return self.tfidfLength
   
   def getTFIDFLength(self):
      if self.tfidfLength < 0:
         return self.computeTFIDFLength()
      return self.tfidfLength
      
   def tfidfDotProduct(self, other):
      dotProduct        = 0
      for word in self.tfidfVector:
         dotProduct    += self.getTFIDF(word) * other.getTFIDF(word)
      return dotProduct
      
   def cosineSimilarity(self, other):
      dotProduct        = self.tfidfDotProduct(other)
      return dotProduct/(self.getTFIDFLength() * other.getTFIDFLength())      
   
   def distanceTo(self, other):
      bagOfWordsSelf    = set( self.tfidfVector.keys())
      bagOfWordsOther   = set(other.tfidfVector.keys())
      bagOfWords        = bagOfWordsSelf | bagOfWordsOther
      distance          = 0
      for word in bagOfWords:
         diff           = self.getTFIDF(word) - other.getTFIDF(word)
         distance      += diff * diff
      return math.sqrt(distance)
   
   def printDocument(self, keys = {'all': 1}):
      if keys.get("all", 0):
         print "Title = " + self.title
         print "URL = " + self.url
         print "Source = " + self.source
         print "Description = " + self.description
         print "queryCode = " + str(self.queryCode)
      else:
         if keys.get("title", 0):
            print "Title = " + self.title
         if keys.get("URL", 0):
            print "URL = " + self.url
         if keys.get("Source", 0):
            print "Source = " + self.source
         if keys.get("Description", 0):
            print "Description = " + self.description
         if keys.get("queryCode", 0):
            print "queryCode = " + self.queryCode
   
   def computeCentroidOf(self, setOfDocs):
      if not setOfDocs:
         print "Empty cluster found"
      numDocs = len(setOfDocs)
      #TODO: Take care of case when numDocs == 0
      setOfWords = set()
      for doc in setOfDocs:
         setOfWords |= doc.getSetOfWords()
      self.tfidfVector = {}
      for word in setOfWords:
         indexEntry = Index.IndexEntry()
         indexEntry.tfidf = 0.0
         for doc in setOfDocs:
            indexEntry.tfidf += doc.getTFIDF(word)
         indexEntry.tfidf /= float(numDocs)
         self.tfidfVector[word] = indexEntry
