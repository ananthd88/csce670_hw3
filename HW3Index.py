#from nltk.corpus import stopwords
import math
class DocumentEntry:             # Index -> Dictionary of Terms -> TermEntry -> List Of DocumentEntry -> DocumentEntry
   def __init__(self, document):
      self.count = 0             # Count of number of times tokens of this term appears in a particular document
      self.tfidf = 0             # TFIDF of this term in this document
      self.document = document   # Pointer to the document
   
   def getCount(self):
      return self.count   
   def incrementCount(self):      
      self.count += 1
      
   def getTFIDF(self):
      return self.tfidf   
   def setTFIDF(self, tfidf):
      self.tfidf = tfidf
   
   def getDocument(self):
      return self.document

class CategoryEntry:             # Index -> Dictionary of Terms -> TermEntry -> List Of CategoryEntry -> CategoryEntry
   def __init__(self):
      self.count = 0             # Count of number of times tokens of this term appears in a particular category
      self.docs  = set()         # Set of documents in this category that has tokens of this term
   
   def getCount(self):
      return self.count
   def incrementCount(self):
      self.count += 1
      
   def getNumDocs(self):
      return len(self.docs)
   def addDoc(self, document):
      self.docs.add(document.getID())
   
class TermEntry:                 # Index -> Dictionary of Terms -> TermEntry
   def __init__(self):
      self.documentList = {}     # Hashtable of DocumentEntries
      self.categoryList = {}     # Hashtable of CategoryEntries
      self.totalCount   = 0      # Count of total number of tokens of this term in all the documents in the collection
      self.miValues = []         # List of Mutual Information (MI) values for this term in each category
                                 # indexed by the category's code
   
   # Methods operating on the documentList
   def getDocumentList(self):
      return self.documentList   
   def getNumDocs(self):
      return len(self.documentList)
   def addDocument(self, document):
      #TODO: Should we call incrementDocumentCount(document) ?
      documentEntry = self.documentList.get(document.getID(), 0)
      if documentEntry:
         return False
      else:
         self.documentList[document.getID()] = DocumentEntry(document)
         return True      
   def isDocumentPresent(self, document):
      for doc in self.documentList.keys():
         if document.getID() == doc:
            return True
      return False      
   
   # Methods operating on a particular documentEntry
   def getDocumentCount(self, document):        # Get count of tokens of this term in a given document
      documentEntry = self.documentList.get(document.getID(), 0)
      if documentEntry:
         return documentEntry.getCount()
      else:
         return 0
   def incrementDocumentCount(self, document):  # Increment the count of tokens of this term in a given document
      documentEntry = self.documentList.get(document.getID(), 0)
      if documentEntry:
         documentEntry.incrementCount()
         return True
      else:
         return False
   def getTFIDF(self, document):                # Get the TFIDF for of term for a particular document
      documentEntry = self.documentList.get(document.getID(), 0)
      if documentEntry:
         return documentEntry.getTFIDF()         
      else:
         return 0.0      
   def setTFIDF(self, document, tfidf):         # Set the TFIDF for of term for a particular document
      documentEntry = self.documentList.get(document.getID(), 0)
      if documentEntry:
         documentEntry.setTFIDF(tfidf)
         return True
      else:
         return False
   
   # Methods operating on the categoryList
   def getCategoryList(self):
      return self.categoryList
   def addCategory(self, category):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         return False
      else:
         self.categoryList[category] = CategoryEntry()
         return True      
   def isCategoryPresent(self, category):
      return category in self.categoryList.keys()
      
   # Methods operating on a particular categoryEntry
   def getCategoryCount(self, category):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         return categoryEntry.getCount()
      else:
         return 0
   def incrementCategoryCount(self, category, document):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         categoryEntry.incrementCount()
         categoryEntry.addDoc(document)
         return True
      else:
         return False
   
   # Methods that operate on the MI values for this term
   def initializeMIValues(self, numCategories):
      self.miValues = [0.0] * numCategories
   def getTotalCount(self):
      return self.totalCount
   def incrementTotalCount(self):
      self.totalCount += 1      
      
   # Methods that operate on both a given DocumentEntry as well as a CategoryEntry
   def forceIncrementAllCounts(self, category, document):
      if category:
         if not self.isCategoryPresent(category):
            self.addCategory(category)
         self.incrementCategoryCount(category, document)
      if document:
         if not self.isDocumentPresent(document):
            self.addDocument(document)
         self.incrementDocumentCount(document)
      self.incrementTotalCount()
      
class Index:                     # Index for a collection
   def __init__(self):
      self.vocabulary = {}       # Hashtable of terms pointing to a TermEntry
      self.numDocs = 0           # Total number of docs indexed
   
   # Methods that operate on the number of documents
   def getNumDocs(self):
      return self.numDocs
   def incrementNumDocs(self):
      self.numDocs += 1
   
   # Methods that operate on all the TermEntries in the Vocabulary or the Vocabulary itself
   def getVocabulary(self):
      return self.vocabulary
   def getSizeOfVocabulary(self):
      return len(self.vocabulary)
   def inVocabulary(self, word):
      return word in self.vocabulary
   def initializeAllMI(self, numCategories):
      for word in self.vocabulary:
         self.vocabulary[word].initializeMIValues(numCategories)
   def processDocument(self, category, document, clustering = True, classifying = True, includeAll = False):
      self.incrementNumDocs()
      bagOfWords = document.getBagOfWords(includeAll)
      #TODO: Handle stopwords here
      #bagOfWords = [w for w in bagOfWords if not w in stopwords.words('english')]
      for word in bagOfWords:
         if not len(word):
            continue
         if not self.inVocabulary(word):
            self.vocabulary[word] = TermEntry()
         if clustering and classifying:
            self.vocabulary[word].forceIncrementAllCounts(category, document)
            category.addWord(word)
         elif clustering:
            self.vocabulary[word].forceIncrementAllCounts(False, document)
         elif classifying:
            self.vocabulary[word].forceIncrementAllCounts(category, False)
            category.addWord(word)
         else:
            self.vocabulary[word].incrementTotalCount()
      if classifying:      
         category.addDocument(document)
         category.incrementTokensBy(len(bagOfWords))

   
   # Wrappers to operate on data in Index -> TermEntry
   def getDocumentList(self, word):
      if not self.inVocabulary(word):
         return {}
      return self.vocabulary[word].getDocumentList()
   def numDocumentsContaining(self, word):
      return len(self.getDocumentList(word))
   def isInDocument(self, word, document):
      if not self.inVocabulary(word):
         return False
      return self.vocabulary[word].isDocumentPresent(document)
   def getCategoryList(self, word):
      if not self.inVocabulary(word):
         return {}
      return self.vocabulary[word].getCategoryList()
   def numCategoriesContaining(self, word):
      return len(self.getCategoryList(word))
   def isInCategory(self, word, category):
      if not self.inVocabulary(word):
         return False
      return self.vocabulary[word].isCategoryPresent(category)
   def getMI(self, word, category):
      if self.vocabulary.get(word, False):
         return self.vocabulary[word].miValues[category.getCode()]
      return 0.0
   def computeMI(self, word, category):
      N  = float(self.getNumDocs())
      T  = float(self.vocabulary[word].getNumDocs())
      C  = float(category.getNumDocs())
      categoryEntry = self.vocabulary[word].getCategoryList().get(category, False)
      if not categoryEntry:
         TC = 0.0
      else:
         TC = float(categoryEntry.getNumDocs())
      
      NXX = N + 1.0
      N00 = N - T - C + TC + 1.0
      N01 = C - TC + 1.0
      N10 = T - TC + 1.0
      N11 = TC + 1.0
      NX0 = N - C + 1.0
      NX1 = C + 1.0
      N0X = N - T + 1.0
      N1X = T + 1.0
      
      mi  = (N11/NXX)*math.log((NXX*N11)/(N1X*NX1)) 
      mi += (N01/NXX)*math.log((NXX*N01)/(N0X*NX1)) 
      mi += (N10/NXX)*math.log((NXX*N10)/(N1X*NX0)) 
      mi += (N00/NXX)*math.log((NXX*N00)/(N0X*NX0))
      
      self.vocabulary[word].miValues[category.getCode()] = mi
   
   # Wrappers to operate on data in Index -> TermEntry -> DocumentEntry
   def getDocumentCount(self, word, document):
      if not self.isInDocument(word, document):
         return 0
      return self.vocabulary[word].getDocumentCount(document)
      
   # Wrappers to operate on data in Index -> TermEntry -> CategoryEntry
   def getCategoryCount(self, word, category):
      if not self.isInCategory(word, category):
         return 0
      return self.vocabulary[word].getCategoryCount(category)
