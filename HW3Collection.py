import HW3Document as Document
import HW3Index as Index
import HW3Cluster as Cluster
import sys
import math
import random
import re
import os.path
import requests
import json

class Category:      # Class that abstracts a category of documents
   def __init__(self, code):
      self.code = code
      self.numMembers = 0
      self.members = []
      self.totalTokens = 0
      self.FN = 0
      self.FP = 0
      self.TN = 0
      self.TP = 0
      self.setOfWords = set()
      self.numOfImportantTokens = 0
      
   def __hash__(self):
      return hash(self.code)
   def __eq__(self, other):
      return self.code == other.code
   
   # Basic methods for the classification quality metrics
   def incrementFN(self):
      self.FN += 1
   def incrementFP(self):
      self.FP += 1
   def incrementTP(self):
      self.TP += 1
   def getFN(self):
      return self.FN
   def getFP(self):
      return self.FP
   def getTN(self):
      return self.TN
   def getTP(self):
      return self.TP
   def computeTN(self, total):
      self.TN = total - self.TP - self.FP - self.FN
   def resetMetrics(self):
      self.TP = 0
      self.FP = 0
      self.FN = 0
      self.TN = 0
   def printConfusionMatrix(self, name):
      print "Confusion matrix for category %s" % (name)
      print "TP = %d" % (self.TP)
      print "FP = %d" % (self.FP)
      print "FN = %d" % (self.FN)
      print "TN = %d" % (self.TN)
   
   def getCode(self):
      return self.code
   #def incrementCount(self):
   #   self.numMembers += 1
   def getNumDocs(self):
      return len(self.members)
   def getTotalTokens(self):
      return self.totalTokens
   def incrementTokensBy(self, count):
      self.totalTokens += count
   def addWord(self, word):
      self.setOfWords.add(word)
   def getSetOfWords(self):
      return self.setOfWords
   def getNumOfImportantTokens(self):
      return self.numOfImportantTokens
   def setNumOfImportantTokens(self, count):
      self.numOfImportantTokens = count
   def addDocument(self, document):
      #TODO: Call to incrementCount()
      self.members.append(document)
   def getMembers(self):
      return self.members
      
class Collection:
   def __init__(self):
      #TODO modify this to a set instead of an array.
      self.documents = []
      self.hashTable = {}
      self.index     = Index.Index()
      self.clusters  = False
      self.purity    = 0.0
      self.rss       = 0.0
      self.maPrecision = 0.0
      self.maRecall = 0.0
      self.queries   = []
      self.categories   = []
      self.categoryNames = []
      self.classification = []
      self.useAllWords = True
      self.importantWords = {}
      self.setOfImportantWords = set()
      self.includeAll = False    
      
   def computeAllMI(self):
      print "Calculating MI of every term for each category..."
      self.index.initializeAllMI(len(self.categories))
      vocabulary = self.index.getVocabulary()
      for word in vocabulary:         
         for category in self.categories:
            self.index.computeMI(word, category)
   def getQuery(self, queryCode):
      if queryCode >= len(self.queries):
         return False
      return self.queries[queryCode]
   def getMAF1(self):
      print "Precision = %f" % (self.maPrecision)
      print "Recall = %f" % (self.maRecall)
      if self.maPrecision == 0.0 and self.maRecall == 0.0:
         return 0.0
      return 2.0*self.maRecall*self.maPrecision/(self.maRecall + self.maPrecision)
   def getNumDocuments(self):
      return len(self.documents)
   def getDocuments(self):
      return self.documents
   def getCategories(self):
      return self.categories
   def getSetOfImportantWords(self):
      return self.setOfImportantWords
   def getIncludeAll(self):
      return self.includeAll
   def setIncludeAll(self, includeAll):
      self.includeAll = includeAll
   def getWeightOfWord(self, word):
      if self.importantWords.get(word, 0) == 0:
         return 0.0001
      return self.importantWords.get(word, 2.0)
   def setWeightOfWord(self, word, weight):
      self.importantWords[word] = weight
      self.setOfImportantWords.add(word)
   def resetImportantWords(self):
      self.importantWords = {}
      self.setOfImportantWords = set()
      
   def getSizeOfVocabulary(self):
      return self.index.getSizeOfVocabulary()
   def getNumQueries(self):
      return len(self.queries)
   
   def getCategory(self, categoryCode):
      if categoryCode < 0 or categoryCode >= len(self.categories):
         return False
      return self.categories[categoryCode]
   
   def getCategoryName(self, categoryCode):
      if categoryCode >= len(self.categories):
         return False
      return self.categoryNames[categoryCode]
   
   def getCategoryTotalTokenCount(self, category):
      return category.getTotalTokens()
   def getCategoryMemberCount(self, category):
      return category.getNumDocs()
      
   def addQueries(self, queries):
      for query in queries:
         self.queries.append(query)
         
   def addCategories(self, categories):
      count = 0
      self.categories = []
      for category in categories:
         self.categories.append(Category(count))
         self.categoryNames.append(category)
         count += 1
   
   def addDocument(self, document, clustering = True, classifying = True):
      if self.hashTable.get(document, 0):
         #print "Duplicate document found, rejecting it."
         return 0
      else:
         self.hashTable[document] = 1
         self.documents.append(document)
         self.index.processDocument(document.getCategory(), document, clustering, classifying, self.includeAll)
         return 1
   
   def getNumTokensInCategory(self, word, category):
      return self.index.getCategoryCount(word, category)
   def getNumTokensInDocument(self, word, document):
      return self.index.getDocumentCount(word, document)
      
   def printCollection(self):
      for document in self.documents:
         print self.queries[document.queryCode] + " -> " + document.title
      
   def computeAllTFIDF(self):
      print "Calculating TFIDF of every term in every doc..."
      numDocs = len(self.documents)
      logNumDocs = math.log(float(numDocs), 2)
      vocabulary = self.index.getVocabulary()
      for word in vocabulary.keys():
         documentList = self.index.getDocumentList(word)
         df = len(documentList)
         logdf = logNumDocs - math.log(float(df), 2)
         for (docID, documentEntry) in documentList.items():
            tf = documentEntry.getCount()
            logtf = 1.0 + math.log(float(tf), 2)
            tfidf = logtf * logdf
            documentEntry.setTFIDF(tfidf)
            documentEntry.getDocument().joinToIndex(word, documentEntry)
   
   def kMeansCluster(self, k, distanceMetric):
      distanceMetricNames = ["Cosine Similarity",
                             "Euclidean distance using normalized TFIDF vectors",
                             "Simple Euclidean distance"]
      print "Running k-means clustering algorithm with k = %d" % (k)
      print "Distance metric being used is %s" % (distanceMetricNames[distanceMetric])
      Cluster.Cluster.numOfClustersCreated = 0
      # Initialization with seeds
      seeds = random.sample(self.documents, k)
      self.clusters = []
      for seed in seeds:
         self.clusters.append(Cluster.Cluster(seed, distanceMetric))
      # Reset the cluster fields populated from any previous runs
      for document in self.documents:
         document.cluster = False
      
      change = True
      iterations = 0
      while(change and iterations < 4):
         print "Iteration %d" % (iterations)
         change = False
         # Assign each document to 'nearest' cluster
         for document in self.documents:
            if document.cluster:
               minDistance = cluster.distanceTo(document)
            else:
               minDistance = sys.float_info.max
            for cluster in self.clusters:
               distance = cluster.distanceTo(document)
               if distance < minDistance:
                  minDistance = distance
                  success = cluster.add(document)
                  if success:
                     change = True
         for cluster in self.clusters:
            cluster.recomputeCentroid()
            
         iterations += 1         
      purityCounts = 0.0
      rssCounts = 0.0
      for cluster in self.clusters:
         cluster.computeMajorityClass()
         purityCounts += cluster.majorityCount
         cluster.computeRSS()
         rssCounts += cluster.rss         
         print cluster
      self.purity = float(purityCounts)/float(len(self.documents))
      self.rss = rssCounts
      print
      print "Finished %d-clustering in %d iterations" % (k, iterations)
      print "Purity for the clustering = %f" % (self.purity)
      print "RSS for clustering = %lf" % (self.rss)
      
   def processAPIQueries(self, queryCode, categoryCode, numResults, clustering = True, classifying = True):
      query    = self.getQuery(queryCode)
      subqueries = re.split('\W+', query)
      if categoryCode >= 0:
         category = self.getCategoryName(categoryCode)         
      skip            = 0
      uniqueCount     = 0
      numRequestsMade = 0
      numTimesRead    = 0
      while uniqueCount < numResults and numTimesRead < 4:
         readFromFile    = 0
         filename = "_".join(subqueries) + "_"
         if categoryCode >= 0:
            filename += category + "_"
         filename += str(skip) + ".json"
         if os.path.exists(filename):
            #print "Reading results from json file %s" % (filename)
            try:
               filehandle = open(filename, "r")
               line = filehandle.read().decode('utf8')
            except IOError:
               print "Error: File " + filename + " doesn\'t exist or could not read data"
               continue
            else:
               filehandle.close()
               readFromFile = 1
               numTimesRead += 1
         else:         
            queryString = "Query=%27" + "_".join(subqueries) + "%27"
            formatString = "&$format=json"
            if categoryCode >= 0:
               categoryString = "&NewsCategory=%27rt_" + category + "%27"
            else:
               categoryString = ""
            if skip:
               skipString = "&$skip=" + str(skip)
            else:
               skipString = ""
            requestString = 'https://api.datamarket.azure.com/Bing/Search/News?' + queryString + formatString + categoryString + skipString
            print "Request String = " + requestString
            print "Sending request..."
            try:
               r = requests.get(requestString, auth = ('ananthd@outlook.com','LFxcEgWSyDOzG8zUzLQgUwl+9tV+B7CHeigeFPMJV40='))
            except ConnectionError:
               #TODO: Other Exceptions - http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
               print "Connection Error!"
               return 0
            else:
               print "Request completed successfully"
               numRequestsMade += 1
               numTimesRead += 1
               line = r.text
         data = json.loads(line)
         for jsonDocument in data["d"]["results"]:
            newDocument = Document.Document(jsonDocument, queryCode, query, self.getCategory(categoryCode))
            success = self.addDocument(newDocument, clustering, classifying)
            if success:
               uniqueCount += 1
               if uniqueCount == numResults:
                  break
         #print "Added %s documents to the collection" % (uniqueCount)      
         # Write the results to a json file on disk for posterity
         if not readFromFile:
            filehandle = open(filename, "w")
            filehandle.write(line.encode('utf8'))
            filehandle.close()
         skip += 15
      return numRequestsMade
   
   def naiveBayesClassifierNew_v2(self, test):
      print "Starting new naive bayes classifier v2"
      train = self
      test.classification = []
      numTrainDocs = float(train.getNumDocuments())
      sizeTrainVocabulary = train.getSizeOfVocabulary()
      thresholdMI = 0.0001
      for document in test.documents:
         maxLogProbability = None
         predictedCategory = False
         for category in train.categories:
            logProbability  = 0.0
            # P(c) = (No. of docs in c)/(No. of training docs)
            logProbability += math.log(float(category.getNumDocs()), 2) - math.log(numTrainDocs, 2)
            bagOfWords = document.getBagOfWords()
            numIgnored = 0
            for word in bagOfWords:
               if len(word):
                  mi = train.index.getMI(word, category)
                  if mi > thresholdMI:
                     logProbability += math.log(float(train.getNumTokensInCategory(word, category)) + 1.0, 2) + 200.0*math.log(mi + 1.0, 2)
                  else:
                     numIgnored += 1
               else:
                  numIgnored += 1
            logProbability -= float(len(bagOfWords) - numIgnored) * math.log(float((category.getTotalTokens() + sizeTrainVocabulary)), 2)
            if maxLogProbability < logProbability:
               maxLogProbability = logProbability
               predictedCategory = category
            # If the log of probabilities for two classes are equal
            elif maxLogProbability == logProbability:
               # Select the class which has more documents assigned to it
               # which would imply a greater value for P(c), 
               # since P(c) = (Num of docs classified as c)/(Num of docs in collection)
               if predictedCategory.getNumDocs() < category.getNumDocs():
                  predictedCategory = category
         predictedCategory = test.getCategory(predictedCategory.getCode())
         document.setPredictedCategory(predictedCategory)
         realCategory = document.getCategory()
         if realCategory == predictedCategory:
            realCategory.incrementTP()
         else:
            realCategory.incrementFN()
            predictedCategory.incrementFP()
            
      # Print out the documents prefixed with their assigned category
      for predictedCategory in test.categories:
         print "Predicted Category: %s\nNo. of docs: %d\n" % (test.getCategoryName(predictedCategory.getCode()), predictedCategory.getNumDocs())
         for document in predictedCategory.getMembers():
            print "\t(%s) : %s" % (test.getCategoryName(document.getCategory().getCode()), document.getTitle())
      
      sumTP = 0
      sumFP = 0
      sumFN = 0
      for category in test.getCategories():
         category.computeTN(test.getNumDocuments())
         category.printConfusionMatrix(test.getCategoryName(category.getCode()))
         sumTP += category.getTP()
         sumFP += category.getFP()
         sumFN += category.getFN()
         # Important to clear the metrics once you are done calculating
         category.resetMetrics()
      print "Sum(TP) = %d" %(sumTP)
      print "Sum(FP) = %d" %(sumFP)
      print "Sum(FN) = %d" %(sumFN)
      print "Total documents in test set = %d" % (test.getNumDocuments())
      test.maPrecision = float(sumTP)/float(sumTP + sumFP)
      test.maRecall = float(sumTP)/float(sumTP + sumFN)
      maf1 = test.getMAF1()
      print "Microaveraged F1 for test set = %f" % (maf1)
      print "Finished naive bayes classification"
      return maf1
      
   def naiveBayesClassifier(self, test):
      print "Starting naive bayes classifier"
      train = self
      numTrainDocs = float(train.getNumDocuments())
      sizeTrainVocabulary = train.getSizeOfVocabulary()
      for document in test.documents:
         maxLogProbability = None
         predictedCategory = False
         for category in train.categories:
            logProbability  = 0.0
            # P(c) = (No. of docs in c)/(No. of training docs)
            logProbability += math.log(float(category.getNumDocs()), 2) - math.log(numTrainDocs, 2) 
            bagOfWords = document.getBagOfWords()
            for word in bagOfWords:
               if len(word):
                  # Add one smoothing
                  logProbability += math.log(float(train.getNumTokensInCategory(word, category)) + 1.0, 2)
            logProbability -= float(len(bagOfWords)) * math.log(float((category.getTotalTokens() + sizeTrainVocabulary)), 2)
            if maxLogProbability < logProbability:
               maxLogProbability = logProbability
               predictedCategory = category
            # If the log of probabilities for two classes are equal
            elif maxLogProbability == logProbability:
               # Select the class which has more documents assigned to it
               # which would imply a greater value for P(c), 
               # since P(c) = (Num of docs classified as c)/(Num of docs in collection)
               if predictedCategory.getNumDocs() < category.getNumDocs():
                  predictedCategory = category
         predictedCategory = test.getCategory(predictedCategory.getCode())
         document.setPredictedCategory(predictedCategory)
         realCategory = document.getCategory()
         if realCategory == predictedCategory:
            realCategory.incrementTP()
         else:
            realCategory.incrementFN()
            predictedCategory.incrementFP()
            
      # Print out the documents prefixed with their assigned category
      for predictedCategory in test.categories:
         print "Predicted Category: %s\nNo. of docs: %d\n" % (test.getCategoryName(predictedCategory.getCode()), predictedCategory.getNumDocs())
         for document in predictedCategory.getMembers():
            print "\t(%s) : %s" % (test.getCategoryName(document.getCategory().getCode()), document.getTitle())
      
      sumTP = 0
      sumFP = 0
      sumFN = 0
      for category in test.getCategories():
         category.computeTN(test.getNumDocuments())
         category.printConfusionMatrix(test.getCategoryName(category.getCode()))
         sumTP += category.getTP()
         sumFP += category.getFP()
         sumFN += category.getFN()
         # Important to clear the metrics once you are done calculating
         category.resetMetrics()
      print "Sum(TP) = %d" %(sumTP)
      print "Sum(FP) = %d" %(sumFP)
      print "Sum(FN) = %d" %(sumFN)
      print "Total documents in test set = %d" % (test.getNumDocuments())
      test.maPrecision = float(sumTP)/float(sumTP + sumFP)
      test.maRecall = float(sumTP)/float(sumTP + sumFN)
      maf1 = test.getMAF1()
      print "Microaveraged F1 for test set = %f" % (maf1)
      print "Finished naive bayes classification"
      return maf1
