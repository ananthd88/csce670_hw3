import HW3Document as Document
import HW3Collection as Collection
import HW3Index as Index
import sys

class Cluster:       # Class that abstracts a cluster
   numOfClustersCreated = 0   # Keeps track number of clusters created, 
                              #  also used to give unique IDs to each cluster
   def __init__(self, seed, distanceMetric = 0):  # Create a new cluster and initialize its 
                              #  centroid with the seed
      Cluster.numOfClustersCreated += 1
      self.id              = Cluster.numOfClustersCreated
      self.members         = set()  # Set of documents in this cluster
      self.centroid        = Document.Document()
      self.majorityClass   = -1
      self.majorityCount   = 0
      self.rss             = 0.0
      self.distanceMetric  = distanceMetric
      newSet = set()
      newSet.add(seed)
      self.centroid.computeCentroidOf(newSet)
      
   def __str__(self):
      string = "Cluster ID: %d" % (self.id)
      string += "No. of documents: %d\n" % (len(self.members))
      for member in self.members:
         query = member.getQuery()
         title = member.getTitle()
         string += "\t(%s): %s\n" % (query, title)
      string += "\n"
      string = string.encode('utf-8')
      return string
   
   # Generic accessor methods
   def getCode(self):
      return self.id
   
   # Methods that are used during in the clustering algorithm
   def recomputeCentroid(self):
      self.centroid.computeCentroidOf(self.members)
   def distanceTo(self, dataPoint):
      # Metric used to calculate "distance" from the centroid of the cluster to a document
      return [
         self.centroid.cosineDistanceTo(dataPoint),
         self.centroid.normalDistanceTo(dataPoint),
         self.centroid.distanceTo(dataPoint)
      ][self.distanceMetric]
   
   # Methods that operate on the members of the cluster
   def add(self, member):
      if member in self.members:
         return False
      self.members.add(member)
      if member.cluster and not member.cluster.remove(member):
         print "Inconsistency detected for member when adding to a cluster:"
         print member.document2String()
      member.cluster = self
      return True
   def remove(self, member):
      if member not in self.members:
         return False
      self.members.remove(member)
      member.cluster = False
      return True
   
   # Methods that compute the clustering quality metrics
   def computeMajorityClass(self):
      classes = {}
      for member in self.members:
         queryCode = member.getQueryCode()
         count = classes.get(queryCode, 0)
         if not count:
            classes[queryCode] = 0
         classes[queryCode] += 1
      for (entry, count) in classes.items():
         if count > self.majorityCount:
            self.majorityClass = entry
            self.majorityCount = count            
   def computeRSS(self):
      oldrss = self.rss
      self.rss = 0.0
      for member in self.members:
         distance = self.distanceTo(member)
         self.rss += distance * distance
      return self.rss < oldrss
