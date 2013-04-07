class DocumentEntry:
   def __init__(self):
      self.count = 0
      self.tfidf = 0
   
   def getCount(self):
      return self.count   
   def incrementCount(self):
      self.count += 1
      
   def getTFIDF(self):
      return self.tfidf   
   def setTFIDF(self, tfidf):
      self.tfidf = tfidf

class CategoryEntry:
   def __init__(self):
      self.count = 0      
   
   def getCount(self):
      return self.count
   def incrementCount(self):
      self.count += 1   
   
class TermEntry:
   def __init__(self):
      self.documentList = {}
      self.categoryList = {}
      self.totalCount   = 0
   
   def getDocumentList(self):
      return self.documentList   
   def getCategoryList(self):
      return self.categoryList
   def getTotalCount(self):
      return self.totalCount
   def incrementTotalCount(self):
      self.totalCount += 1
         
   def isCategoryPresent(self, category):
      return self.categoryList.get(category, False) == True
   def isDocumentPresent(self, document):
      return self.documentList.get(document, False) == True
      
   def addCategory(self, category):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         return False
      else:
         self.categoryList[category] = CategoryEntry()
         return True      
   def addDocument(self, document):
      documentEntry = self.documentList.get(document, 0)
      if documentEntry:
         return False
      else:
         self.documentList[document] = DocumentEntry()
         return True      
      
   def getCategoryCount(self, category):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         return categoryEntry.getCount()
      else:
         return 0
   def incrementCategoryCount(self, category):
      categoryEntry = self.categoryList.get(category, 0)
      if categoryEntry:
         categoryEntry.incrementCount()
         return True
      else:
         return False
      
   def getDocumentCount(self, document):
      documentEntry = self.documentList.get(document, 0)
      if documentEntry:
         return documentEntry.getCount()
      else:
         return 0
   def incrementDocumentCount(self, document):
      documentEntry = self.documentList.get(document, 0)
      if documentEntry:
         documentEntry.incrementCount()
         return True
      else:
         return False
      
   def getTFIDF(self, document):
      documentEntry = self.documentList.get(document, 0)
      if documentEntry:
         return documentEntry.getTFIDF()         
      else:
         return 0.0      
   def setTFIDF(self, document, tfidf):
      documentEntry = self.documentList.get(document, 0)
      if documentEntry:
         documentEntry.setTFIDF(tfidf)
         return True
      else:
         return False
   
   def forceIncrementAllCounts(self, category, document):
      if category:
         if not self.isCategoryPresent(category):
            self.addCategory(category)
         self.incrementCategoryCount(category)
      if not self.isDocumentPresent(document):
         self.addDocument(document)
      self.incrementDocumentCount(document)
      self.incrementTotalCount()
      
class Index:
   def __init__(self):
      self.vocabulary = {}
   
   def getVocabulary(self):
      return self.vocabulary
   def inVocabulary(self, word):
      return word in self.vocabulary
   def getDocumentList(self, word):
      if not self.inVocabulary(word):
         return {}
      return self.vocabulary[word].getDocumentList()
   def getCategoryList(self, word):
      if not self.inVocabulary(word):
         return {}
      return self.vocabulary[word].getCategoryList()
   
   def isInDocument(self, word, document):
      if not self.inVocabulary(word):
         return False
      return self.vocabulary[word].isDocumentPresent(document)
   def isInCategory(self, word, category):
      if not self.inVocabulary(word):
         return False
      return self.vocabulary[word].isCategoryPresent(category)
   
   def processDocument(self, category, document):
      bagOfWords = document.getBagOfWords()
      for word in bagOfWords:
         if not self.inVocabulary(word):
            self.vocabulary[word] = TermEntry()
         self.vocabulary[word].forceIncrementAllCounts(category, document)
      if category:
         category.incrementCount()
         category.incrementTokensBy(len(bagOfWords))

   def numDocumentsContaining(self, word):
      return len(self.getDocumentList(word))
   def numCategoriesContaining(self, word):
      return len(self.getCategoryList(word))
      
   def isWordInDocument(self, word, document):
      if not inVocabulary(word):
         return False
      return self.vocabulary[word].isDocumentPresent(document)
   def isWordInCategory(self, word, category):
      if not inVocabulary(word):
         return False
      return self.vocabulary[word].isCategoryPresent(category)
      
   def getDocumentCount(self, word, document):
      if not self.isInDocument(word, document):
         return 0
      return self.vocabulary[word].getDocumentCount(document)
   def getCategoryCount(self, word, category):
      if not self.isInCategory(word, category):
         return 0
      return self.vocabulary[word].getCategoryCount(category)
