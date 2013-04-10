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
   collection.setIncludeAll(True)
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
   collection.computeAllMI()
   
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
   testCollection.hashTable = {}
   
   maf1 = collection.naiveBayesClassifierNew_v2(testCollection)
   #filename = "train3.varinfo"
   #filehandle = open(filename, "r")
   #lines = filehandle.readlines()
   #filehandle.close()
   #numLines = len(lines)
   #limit = numLines/2
   # 
   #hashMAF1 = {}
   #margin = 0
   #collection.useAllWords = False
   #print "\n\n\n"
   #while(margin < limit):
   #   margin += 250
   #   print "\nMargin = " + str(margin)
   #   collection.resetImportantWords()
   #  for line in lines[:margin]:
   #      line = line.decode('utf8')
   #     attributes = re.split(" +", line)
   #      word = attributes[0][1:]
   #      weight = attributes[5][1:]
   #      if weight[-1] == "\n":
   #         weight = attributes[4][1:]
   #      weight = float(weight)
   #      collection.setWeightOfWord(word, weight)
   #   for line in lines[-margin:]:
   #      line = line.decode('utf8')
   #      attributes = re.split(" +", line)
   #      word = attributes[0][1:]
   #      weight = attributes[5][1:]
   #      if weight[-1] == "\n":
   #         weight = attributes[4][1:]
   #      weight = float(weight)
   #      collection.setWeightOfWord(word, weight)
   #   maf1 = collection.naiveBayesClassifierNew(testCollection)
   #   hashMAF1[margin] = maf1
   # 
   #for key in sorted(hashMAF1.keys()):
   #   print str(key) + " - " + str(hashMAF1[key])
   #collection.useAllWords = True
   
   
if __name__ == '__main__':
    main()
