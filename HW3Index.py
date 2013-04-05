class IndexEntry:
   def __init__(self):
      self.count = 0
      self.tfidf = 0
   
   def increment(self):
      self.count += 1
      
   def getCount(self):
      return self.count
   
   def getTFIDF(self):
      return self.tfidf
   
   def setTFIDF(self, tfidf):
      self.tfidf = tfidf
   
class Index:
   def __init__(self):
      self.vocabulary = {}
   
   def processDocument(self, document):
      bagOfWords = document.getBagOfWords()
      for word in bagOfWords:
         postings = self.vocabulary.get(word, {})
         if not postings:
            self.vocabulary[word] = postings
         indexEntry = postings.get(document, IndexEntry())
         if not indexEntry.count:
            postings[document] = indexEntry
         indexEntry.increment()
   
   def getPostings(self, word):
      #TODO: Remove the calls to lower() for all methods in this class?
      word = word.lower()
      return self.vocabulary.get(word, {})
   
   def getVocabulary(self):
      return self.vocabulary
   
   def inVocabulary(word):
      word = word.lower()
      return word in self.vocabulary
   
   def numDocsContaining(self, word):
      word = word.lower()
      return len(self.getPostings(word))
   
   def isWordInDoc(self, word, document):
      word = word.lower()
      return document in self.getPostings(word)
   
   def getTF(self, word, document):
      word = word.lower()
      postings = self.getPostings(word)
      if document in postings:
         return postings[document].getCount()
      return 0 
