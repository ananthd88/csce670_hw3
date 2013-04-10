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
   
   print "This program runs k-means clustering for k = 2 to 15 (10 times each)"
   print "This might take a while"
   print
   print
   distanceMetric = 1
   metricArray = []
   for k in range(2, 16):
      bestPurity = 0.0
      bestRSS = 0.0
      for i in range(0, 10):
         collection.kMeansCluster(k, distanceMetric)
         if bestPurity < collection.purity:
            bestPurity = collection.purity
         if bestRSS < collection.rss:
            bestRSS = collection.rss
      metric = {"purity": bestPurity, "rss": bestRSS}
      metricArray.append(metric)
   
   k = 2
   for metric in metricArray:
      print "\nBest %d-clustering purity = %f" % (k, metric["purity"])
      print "Best %d-clustering RSS = %f" % (k, metric["rss"])
      k += 1
if __name__ == '__main__':
    main()
