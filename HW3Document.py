import HW3Index as Index
import re
import math

class Document:
   numOfDocsCreated = 0
   def __init__(self, dictionary = {}, queryCode = False, category = False):
      Document.numOfDocsCreated += 1
      self.id           = Document.numOfDocsCreated
      self.title        = dictionary.get("Title", "").lower()
      self.url          = dictionary.get("Url", "").lower()
      self.source       = dictionary.get("Source", "").lower()
      self.description  = dictionary.get("Description", "").lower()
      self.queryCode    = queryCode
      self.tfidfVector  = {}
      self.tfidfLength  = -1.0
      self.cluster      = False
      self.category     = category
   
   def __hash__(self):
      return hash(self.title)
   
   def __eq__(self, other):
      return (self.title, self.url, self.source, self.description) == (other.title, other.url, other.source, other.description)
   
   def getTFIDF(self, word):
      documentEntry = self.tfidfVector.get(word, 0)
      if documentEntry:
         return documentEntry.getTFIDF()
      else:
         return 0.0
   def getQueryCode(self):
      return self.queryCode
   def getCategory(self):
      return self.category
   #TODO: Might not be used
   def setCategory(self, category):
      self.category = category
   def getPredictedCategory(self):
      return self.predictedCategory
   def setPredictedCategory(self, category):
      self.predictedCategory = category
   def getTitle(self):
      return self.title
   def getDescription(self):
      return self.description
   def joinToIndex(self, word, documentEntry):
      self.tfidfVector[word] = documentEntry
   
   def getBagOfWords(self):
      array1 = re.split('[^a-zA-Z0-9_@]', self.title)
      array2 = re.split('[^a-zA-Z0-9_@]', self.description)
      bagOfWords = array1 + array2
      return bagOfWords
   
   def getSetOfWords(self):
      #TODO: Performance! This is called several times for recomputation of centroids
      return set(self.tfidfVector.keys())
      
   def computeTFIDFLength(self):
      self.tfidfLength  = 0.0
      for word in self.tfidfVector:
         tfidf = self.getTFIDF(word)
         self.tfidfLength  += tfidf * tfidf
      self.tfidfLength  = math.sqrt(self.tfidfLength)
      return self.tfidfLength
   
   def getTFIDFLength(self):
      if self.tfidfLength < 0.0:
         return self.computeTFIDFLength()
      return self.tfidfLength
      
   def tfidfDotProduct(self, other):
      dotProduct        = 0.0
      for word in self.tfidfVector:
         dotProduct    += self.getTFIDF(word) * other.getTFIDF(word)
      return dotProduct
      
   def cosineSimilarity(self, other):
      dotProduct        = self.tfidfDotProduct(other)
      return dotProduct/(self.getTFIDFLength() * other.getTFIDFLength())
   
   def distanceTo(self, other):
      setOfWords        = self.getSetOfWords() | other.getSetOfWords()
      distance          = 0.0
      for word in setOfWords:
         diff           = self.getTFIDF(word) - other.getTFIDF(word)
         distance      += diff * diff
      return math.sqrt(distance)
   
   def normalDistanceTo(self, other):
      setOfWords        = self.getSetOfWords() | other.getSetOfWords()
      distance          = 0.0
      for word in setOfWords:
         diff           = (self.getTFIDF(word)/self.getTFIDFLength()) - (other.getTFIDF(word)/other.getTFIDFLength())
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
      #TODO: Empty Clusters
      #if not setOfDocs:
         #print "Empty cluster found"
      numDocs = len(setOfDocs)
      setOfWords = set()
      for doc in setOfDocs:
         setOfWords |= doc.getSetOfWords()
      self.tfidfVector = {}
      for word in setOfWords:
         tfidf = 0.0
         for doc in setOfDocs:
            tfidf += doc.getTFIDF(word)            
         if numDocs:
            tfidf /= float(numDocs)
         documentEntry = Index.DocumentEntry()
         documentEntry.setTFIDF(tfidf)
         self.tfidfVector[word] = documentEntry
