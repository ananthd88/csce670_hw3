import HW3Document as Document
import HW3Index as Index
import HW3Cluster as Cluster
import sys
import math
import random

class Collection:
   def __init__(self):
      #TODO modify this to a set instead of an array.
      self.documents = []
      self.hashTable = {}
      self.queries   = []
      self.index     = Index.Index()
      self.clusters  = False
      self.purity    = 0.0
      
   def addDocument(self, document):
      if self.hashTable.get(document, 0):
         print "Duplicate document found, rejecting it."
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
         for (document, indexEntry) in postings.items():
            tf = indexEntry.getCount()
            logtf = 1.0 + math.log(float(tf), 2)
            tfidf = logtf * logdf
            indexEntry.setTFIDF(tfidf)
            document.joinToIndex(word, indexEntry)
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
