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
      numRequestsMade = collection.processAPIQueries(queryCode, -1, 30)
      print str(numRequestsMade) + " requests to the Bing API were made."
      collection.hashTable = {}
   collection.computeAllTFIDF()
   print
   print
   metricArray = []
   for k in range(2, 16):
      bestPurity = 0.0
      bestRSS = 0.0
      for i in range(0, 10):
         collection.kMeansCluster(k)
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
   
   numCategories = len(categories)
   for queryCode in range(numQueries):
      for categoryCode in range(numCategories):
         numRequestsMade = processAPIQueries(collection, queryCode, categoryCode, 30)
         if numRequestsMade:
            print str(numRequestsMade) + " requests to the Bing API were made."
         #TODO: Should this be moved outside the outer for loop ?
         #      To avoid all duplicates, and not just within (query,category) groups
         collection.hashTable = {}

   collection.printCollection()
if __name__ == '__main__':
    main()
