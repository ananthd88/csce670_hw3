import HW3Collection as Collection
import gc
import re

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
         numRequestsMade = collection.processAPIQueries(queryCode, categoryCode, 30, True, True)
         if numRequestsMade:
            print str(numRequestsMade) + " requests to the Bing API were made."
         totalRequestsMade += numRequestsMade
         #TODO: Should this be moved outside the outer for loop ?
         #      To avoid all duplicates, and not just within (query,category) groups
         collection.hashTable = {}
   #collection.computeAllTFIDF()
   
   queries = ["apple", "facebook", "westeros", "gonzaga", "banana"]
   numQueries = len(queries)
   testCollection = Collection.Collection()
   testCollection.addQueries(queries)
   testCollection.addCategories(categories)
   totalRequestsMade = 0
   for queryCode in range(numQueries):
      for categoryCode in range(numCategories):
         numRequestsMade = testCollection.processAPIQueries(queryCode, categoryCode, 30, False, False)
         if numRequestsMade:
            print str(numRequestsMade) + " requests to the Bing API were made."
         totalRequestsMade += numRequestsMade
         #TODO: Should this be moved outside the outer for loop ?
         #      To avoid all duplicates, and not just within (query,category) groups
         collection.hashTable = {}
   maf1 = collection.naiveBayesClassifier(testCollection)   
   
if __name__ == '__main__':
    main()
