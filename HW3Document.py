import HW3Index as Index
import re
import math

class Document:         # Class which abstracts documents
   numOfDocsCreated = 0 # Keeps track number of documents created, 
                        # also used to give unique IDs to each document
   def __init__(self, dictionary = {}, queryCode = False, query = "", category = False):
      Document.numOfDocsCreated += 1
      self.id                 = Document.numOfDocsCreated
      self.title              = dictionary.get("Title", "").lower()
      self.description        = dictionary.get("Description", "").lower()
      self.source             = dictionary.get("Source", "").lower()
      self.url                = dictionary.get("Url", "").lower()
      self.query              = query     # Query that generated this document
      self.queryCode          = queryCode # Code for the query that generated
                                          #  this document
      self.category           = category  # Pointer to the corresponding 
                                          #  category object
      self.predictedCategory  = False
      self.cluster            = False     # Pointer to the corresponding 
                                          #  cluster object
      self.tfidfVector        = {}        # TFIDF vector for the document
      self.tfidfLength        = -1.0      # Length of the TFIDF vector
      
   def __hash__(self):
      return hash(self.title)      
   def __eq__(self, other):
      # Two documents are "equal" if title, description, source and url match
      return (self.title,  self.url,  self.source,  self.description ) == \
             (other.title, other.url, other.source, other.description)
      
   # General accessor methods that operate on the document's fields
   def getID(self):
      return self.id
   def getQuery(self):
      return self.query
   def getQueryCode(self):
      return self.queryCode
   def getCluster(self):
      return self.cluster
   def getClusterCode(self):
      return self.cluster.getCode()
   def getTitle(self):
      return self.title
   def getDescription(self):
      return self.description
   def getBagOfWords(self, includeAll = False):
      array1 = re.split('[^a-zA-Z0-9]', self.title)
      array2 = re.split('[^a-zA-Z0-9]', self.description)
      if includeAll:
         array3 = re.split('[^a-zA-Z0-9]', self.source)
         array4 = re.split('[^a-zA-Z0-9]', self.url)
         stopwords = set(
         [ 
         #"a",
         #"about",
         #"above",
         #"after",
         #"again",
         #"against",
         #"all",
         "am",
         "an",
         "and",
         "any",
         "are",
         "aren",
         "as",
         "at",
         "be",
         #"because",
         #"been",
         #"before",
         #"being",
         #"below",
         #"between",
         #"both",
         "but",
         "by",
         "can",
         "cannot",
         "could",
         "couldn",
         #"did",
         #"didn",
         #"do",
         #"does",
         #"doesn",
         #"doing",
         #"don",
         #"down",
         #"during",
         #"each",
         #"few",
         #"for",
         #"from",
         #"further",
         "had",
         "hadn",
         "has",
         "hasn",
         "have",
         "haven",
         "having",
         "he",
         "d",
         "ll",
         "s",
         "her",
         "here",
         "hers",
         "herself",
         "him",
         "himself",
         "his",
         #"how",
         "i",
         "m",
         "ve",
         "if",
         "in",
         "into",
         "is",
         "isn",
         #"it",
         #"its",
         #"itself",
         #"let",
         "me",
         #"more",
         #"most",
         #"must"
         #"mustn",
         #"my",
         #"myself",
         "no",
         "nor",
         "not",
         "of",
         #"off",
         "on",
         #"once",
         #"only",
         "or",
         #"other",
         #"ought",
         #"our",
         #"ours ",
         #"ourselves",
         #"out",
         #"over",
         #"own",
         #"same",
         #"shan",
         "she",
         #"should",
         #"shouldn",
         "so",
         #"some",
         #"such",
         #"than",
         #"that",
         "the",
         #"their",
         #"theirs",
         #"them",
         #"themselves",
         "then",
         "there",
         #"these",
         "they",
         #"this",
         #"those",
         #"through",
         "to",
         #"too",
         #"under",
         #"until",
         #"up",
         "very",
         #"was",
         #"wasn",
         "we",
         "re",
         "we",
         #"were",
         #"weren",
         #"what"
         #"when",
         #"where",
         #"which",
         #"while",
         #"who",
         #"whom",
         #"why",
         #"with",
         "t",
         #"won",
         "would",
         "wouldn",
         #"you",
         #"your",
         #"yours",
         #"yourself",
         "yourselves"]
         )
         array11 = []
         array22 = []
         array33 = []
         array44 = []
         for word in array1:
            if len(word) > 2 and word not in stopwords:
               array11.append(word)
         for word in array2: 
            if len(word) > 2 and word not in stopwords:
               array22.append(word)
         for word in array3:
            if len(word) > 2 and word not in stopwords:
               array33.append(word)
         for word in array4:
            if len(word) > 2 and word not in stopwords:
               array44.append(word)
         array1 = array11
         array2 = array22
         array3 = array33
         array4 = array44
      if includeAll:
         bagOfWords = array1 + array2 + array3 + array4
      else:
         bagOfWords = array1 + array2
      return bagOfWords
   def getSetOfWords(self):
      #TODO: Performance! This is called several times for recomputation of centroids
      return set(self.tfidfVector.keys())
      
   
   # Methods that operate on the document's TFIDF vector
   def getTFIDF(self, word):
      documentEntry = self.tfidfVector.get(word, 0)
      if documentEntry:
         return documentEntry.getTFIDF()
      else:
         return 0.0
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
   def cosineDistanceTo(self, other):
      cosine = self.cosineSimilarity(other)
      if cosine > 1.0 or cosine < -1.0:
         return float(math.pi/2.0)
      return abs(math.acos(cosine))
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
   def getDifferenceVector(self, other):
      differenceVector = {}
      setOfWords        = self.getSetOfWords() | other.getSetOfWords()
      for word in setOfWords:
         differencevector[word] = self.getTFIDF(word) - other.getTFIDF(word)
      return differenceVector
      
   def joinToIndex(self, word, documentEntry):
      self.tfidfVector[word] = documentEntry
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
         documentEntry = Index.DocumentEntry(False)
         documentEntry.setTFIDF(tfidf)
         self.tfidfVector[word] = documentEntry
   
   # Methods that operate on the document's category or predicted category
   def getCategory(self):
      return self.category
   #TODO: Might not be used
   def setCategory(self, category):
      self.category = category
   def getPredictedCategory(self):
      return self.predictedCategory
   def setPredictedCategory(self, category):
      self.predictedCategory = category
      category.addDocument(self)
   
   # Miscellaneous stringify methods for document
   def document2String(self, keys = {'all': 1}):
      string = ""
      if keys.get("all", 0):
         string += "Title = "       + self.title
         string += "URL = "         + self.url
         string += "Source = "      + self.source
         string += "Description = " + self.description
         string += "QueryCode = "   + str(self.queryCode)
      else:
         if keys.get("title", 0):
            string += "Title = "       + self.title
         if keys.get("URL", 0):
            string += "URL = "         + self.url
         if keys.get("Source", 0):
            string += "Source = "      + self.source
         if keys.get("Description", 0):
            string += "Description = " + self.description
         if keys.get("queryCode", 0):
            string += "queryCode = "   + self.queryCode
      return string
   def document2VowpalData(self):
      string = str(self.category.getCode())
      string += " | "
      set1 = self.getSetOfWords()
      for item in set1:
         if len(item) > 0:
            string += item + ":" + str(self.tfidfVector[item].getCount()) + " "         
      if string[-1] == " ":
         string = string[:-1]
      return string
