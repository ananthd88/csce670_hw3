import HW3Collection as Collection
import gc

def main():
   gc.enable()
   collection = Collection.Collection()
   queries = ["texas aggies",
              "texas longhorns",
              "duke blue devils",
              "dallas cowboys",
              "dallas mavericks"]
   collection.addQueries(queries)
   numQueries = len(queries)
   for queryCode in range(numQueries):
      numRequestsMade = collection.processAPIQueries(queryCode, -1, 30, True, False)
      print str(numRequestsMade) + " requests to the Bing API were made."
      collection.hashTable = {}
   collection.computeAllTFIDF()
   
   k = 15
   distanceMetric = 1
   clustering1 = collection.kMeansCluster(k, distanceMetric)   
   #print "Running k-means clustering algorithm with k = %d" % (k)
   #print "Distance metric being used is %s" % (distanceMetricNames[distanceMetric])
   #clustering2 = collection.kMeansCluster(k, distanceMetric)   
   #count = 0
   #matches = 0
   #mismatches = 0
   #for count in range(collection.getNumDocuments()):
   #   if clustering1[count] == clustering2[count]:
   #      matches += 1
   #   else:
   #      mismatches += 1
   #print "RI = %f" % (float(matches/(matches + mismatches))
   
if __name__ == '__main__':
    main()
