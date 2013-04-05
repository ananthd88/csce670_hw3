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
      self.centroid        = Document.Document({}, -1)
      self.majorityClass   = -1
      self.majorityCount   = 0
      #self.centroid = dataPointConstructor({})
      #self.centroid = dataPointConstructor(self.centroid, {})
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
      old = member.cluster
      if old:
         oldDist = old.distanceTo(member)
         old = old.id         
      else:
         old = -1
         oldDist = sys.float_info.max
      new = self.id
      newDist = self.distanceTo(member)
      #print "Doc:%d (%d) -> (%d)" % (member.id, old, new)
      #print "Doc:" + str(member.id) + "("+ str(old) + ") -> (" + str(new) + ")"
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
      return self.centroid.distanceTo(dataPoint)
   
   def computeMajorityClass(self):
      classes = {}
      for member in self.members:
         count = classes.get(member.queryCode, 0)
         if not count:
            classes[member.queryCode] = 0
         classes[member.queryCode] += 1
      for (entry, count) in classes.items():
         if count > self.majorityCount:
            self.majorityCount = count
            self.majorityClass = entry
