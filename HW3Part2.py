import HW3Document as Document
import HW3Collection as Collection
import json
import requests
import re
import os.path
import gc

def processAPIQueries(collection, queryCode, categoryCode, numResults):
   query    = collection.getQuery(queryCode)
   category = collection.getCategoryName(categoryCode)
   skip            = 0
   uniqueCount     = 0
   numRequestsMade = 0
   numTimesRead    = 0
   while uniqueCount < numResults and numTimesRead < 4:
      readFromFile    = 0
      filename = query + "_" + category + "_" + str(skip) + ".json"
      if os.path.exists(filename):
         print "Reading results from json file %s" % (filename)
         try:
            filehandle = open(filename, "r")
            # Slurp the whole file into memory as a single string
            line = filehandle.read().decode('utf8')
         except IOError:
            print "Error: File " + filename + " doesn\'t exist or could not read data"
            continue
         else:
            filehandle.close()
            readFromFile = 1
            numTimesRead += 1
      else:         
         if skip:
            skipString = "&$skip=" + str(skip)
         else:
            skipString = ""
         categoryString = "&NewsCategory=%27rt_" + category + "%27"
         requestString = 'https://api.datamarket.azure.com/Bing/Search/News?Query=%27' + query + '%27' + "&$format=json" + categoryString + skipString
         print "Request String = " + requestString
         print "Sending request..."
         try:
            r = requests.get(requestString, auth = ('ananthd@outlook.com','LFxcEgWSyDOzG8zUzLQgUwl+9tV+B7CHeigeFPMJV40='))
         except ConnectionError:
            #TODO: Other Exceptions - http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
            print "Connection Error!"
            return 0
         else:
            print "Request completed successfully"
            numRequestsMade += 1
            numTimesRead += 1
            line = r.text
      data = json.loads(line)
      for jsonDocument in data["d"]["results"]:
         newDocument = Document.Document(jsonDocument, queryCode, collection.getCategory(categoryCode))
         success = collection.addDocument(newDocument)
         if success:
            uniqueCount += 1
            if uniqueCount == numResults:
               break
      #print "Added %s documents to the collection" % (uniqueCount)      
      # Write the results to a json file on disk for posterity
      if not readFromFile:
         filehandle = open(filename, "w")
         filehandle.write(line.encode('utf8'))
         filehandle.close()
      skip += 15
   return numRequestsMade
   
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
