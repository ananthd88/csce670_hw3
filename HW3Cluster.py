import HW3Document as Document
import HW3Collection as Collection
import HW3Index as Index
import sys

class Cluster:
   numOfClustersCreated = 0
   def __init__(self, seed):
      Cluster.numOfClustersCreated += 1
      self.id              = Cluster.numOfClustersCreated
      self.members         = set()
      self.centroid        = Document.Document()
      self.majorityClass   = -1
      self.majorityCount   = 0
      self.rss             = 0.0
      #Mark centroid of this cluster as equivalent to the seed document
      newSet = set()
      newSet.add(seed)
      self.centroid.computeCentroidOf(newSet)
   
   def __str__(self):
      string = 'Cluster ID: {self.id}\t'.format(self=self)
      string += 'No. members: ' + str(len(self.members)) + '\n\t'
      for member in self.members:
         #string += '\t' + str(member.id) + '\t : ' + member.title + '\n'
         string += str(member.id) + ', '
      return string
   
   def recomputeCentroid(self):
      self.centroid.computeCentroidOf(self.members)
   
   def add(self, member):
      if member in self.members:
         return False
      #old = member.cluster
      #if old:
      #   oldDist = old.distanceTo(member)
      #   old = old.id         
      #else:
      #   old = -1
      #   oldDist = sys.float_info.max
      #new = self.id
      #newDist = self.distanceTo(member)
      #print "Doc:%d (%d)(%f) -> (%d)(%f)" % (member.id, old, oldDist, new, newDist)
      self.members.add(member)
      if member.cluster and not member.cluster.remove(member):
         print "Inconsistency detected for member when adding to a cluster:"
         member.printDocument()
      member.cluster = self
      return True
   
   def remove(self, member):
      if member not in self.members:
         return False
      self.members.remove(member)
      member.cluster = False
      return True
   
   def distanceTo(self, dataPoint):
      # Metric used to calculate "distance" from the centroid of the cluster to a document
      #return self.centroid.distanceTo(dataPoint)
      #return self.centroid.cosineSimilarity(dataPoint)
      return self.centroid.normalDistanceTo(dataPoint)
   
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
