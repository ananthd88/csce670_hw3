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

class Category:
   def __init__(self, code):
      self.code = code
      self.numMembers = 0
      self.totalTokens = 0
   def __hash__(self):
      return hash(self.code)
   def __eq__(self, other):
      return (self.code, len(self.members), len(self.terms)) == (other.code, len(other.members), len(other.terms))
   
   def getCount(self):
      return self.numMembers
   def incrementCount(self):
      self.numMembers += 1
   def getTotalTokens(self):
      return self.totalTokens
   def incrementTokensBy(self, count):
      self.totalTokens += count
      
      
class Collection:
   def __init__(self):
      #TODO modify this to a set instead of an array.
      self.documents = []
      self.hashTable = {}
      self.index     = Index.Index()
      self.clusters  = False
      self.purity    = 0.0
      self.rss       = 0.0
      self.queries   = []
      self.categories   = []
      self.categoryNames = []
      
   def getQuery(self, queryCode):
      if queryCode >= len(self.queries):
         return False
      return self.queries[queryCode]
   
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
      
   def addDocument(self, document):
      if self.hashTable.get(document, 0):
         print "Duplicate document found, rejecting it."
         return 0
      else:
         self.hashTable[document] = 1
         self.documents.append(document)
         self.index.processDocument(document.getCategory(), document)
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
         documentList = self.index.getDocumentList(word)
         df = len(documentList)
         logdf = logNumDocs - math.log(float(df), 2)
         for (document, documentEntry) in documentList.items():
            tf = documentEntry.getCount()
            logtf = 1.0 + math.log(float(tf), 2)
            tfidf = logtf * logdf
            documentEntry.setTFIDF(tfidf)
            document.joinToIndex(word, documentEntry)
            #print "(%s) - (%f)" % (document.id, tfidf)

   def kMeansCluster(self, k):
      # Initialization with seeds
      seeds = random.sample(self.documents, k)
      self.clusters = []
      for seed in seeds:
         self.clusters.append(Cluster.Cluster(seed))
      
      # Reset the cluster fields populated from any previous runs
      for document in self.documents:
         document.cluster = False
      
      change = True
      iterations = 0
      # Assign to clusters and recompute centroids
      #while(change and iterations < 4):
      while(change):
         change = False
         # Assign each document to 'nearest' cluster
         for document in self.documents:
            if document.cluster:
               minDistance = document.cluster.distanceTo(document)
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
            #print cluster
            cluster.recomputeCentroid()
            
         iterations += 1
         #print "Completed iteration %d" % (iterations)
         #print "RSS = %f" % (rssCounts)
         #raw_input("Press any key...")
      purityCounts = 0.0
      rssCounts = 0.0
      for cluster in self.clusters:
         cluster.computeMajorityClass()
         purityCounts += cluster.majorityCount
         cluster.computeRSS()
         rssCounts += cluster.rss
      self.purity = float(purityCounts)/float(len(self.documents))
      self.rss = rssCounts
      print
      print "Finished %d-clustering in %d iterations" % (k, iterations)
      print "Purity for the clustering = %f" % (self.purity)
      print "RSS for clustering = %lf" % (self.rss)
   
   def processAPIQueries(self, queryCode, categoryCode, numResults):
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
            print "Reading results from json file %s" % (filename)
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
            if category >= 0:
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
            newDocument = Document.Document(jsonDocument, queryCode, self.getCategory(categoryCode))
            success = self.addDocument(newDocument)
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
