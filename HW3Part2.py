import HW3Collection as Collection
import gc

def main():
   gc.enable()
   collection = Collection.Collection()
   queries = [ "bing",    "amazon",  "twitter",    "yahoo",  "google", 
               "beyonce", "bieber",  "television", "movies", "music",
               "obama",   "america", "congress",   "senate", "lawmakers"]
   categories = ["Entertainment", 
                 "Business", 
                 "Politics"]
   collection.addQueries(queries)
   collection.addCategories(categories)
   numQueries = len(queries)
   numCategories = len(categories)
   totalRequestsMade = 0
   for queryCode in range(numQueries):
      for categoryCode in range(numCategories):
         numRequestsMade = collection.processAPIQueries(queryCode, categoryCode, 30)
         if numRequestsMade:
            print str(numRequestsMade) + " requests to the Bing API were made."
         totalRequestsMade += numRequestsMade
         #TODO: Should this be moved outside the outer for loop ?
         #      To avoid all duplicates, and not just within (query,category) groups
         collection.hashTable = {}
   collection.printCollection()
   print "Total requests made = %d" % (totalRequestsMade)
if __name__ == '__main__':
    main()
