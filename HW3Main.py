import HW3Record as Record
import HW3Table as Table
import json
import requests
import re
import os.path

def processAPIQueries(table, queryCode, numResults):
   query = table.queries[queryCode]
   subqueries = re.split('\W+', query)
   newQuery = "%20".join(subqueries)
   
   skip = 0
   uniqueCount = 0
   numRequestsMade = 0
   readFromFile = 0
   
   while uniqueCount < numResults:
      filename = "_".join(subqueries) + "_" + str(skip) + ".json"
      if os.path.exists(filename):
         print "Reading results from json file on disk"
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
      else:         
         if skip:
            skipString = "&$skip=" + str(skip)
         else:
            skipString = ""
         
         requestString = 'https://api.datamarket.azure.com/Bing/Search/News?Query=%27' + newQuery + '%27&$format=json' + skipString
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
            line = r.text
      
      data = json.loads(line)
      
      for jsonRecord in data["d"]["results"]:
         newRecord = Record.Record(jsonRecord, queryCode)
         success = table.addRecord(newRecord)
         if success:
            uniqueCount += 1
            if uniqueCount == numResults:
               break
      
      print "Added %s records to the table" % (uniqueCount)
      
      # Write the results to a json file on disk for posterity
      if not readFromFile:
         filehandle = open(filename, "w")
         filehandle.write(line.encode('utf8'))
         filehandle.close()
      
      skip += 15
   return numRequestsMade
   
def main(): 
   table = Table.Table()
   table.queries = ["texas aggies",
                    "texas longhorns",
                    "duke blue devils",
                    "dallas cowboys",
                    "dallas mavericks"]
   count = 0
   for query in table.queries:
      numRequestsMade = processAPIQueries(table, count, 30)
      print str(numRequestsMade) + " requests to the Bing API were made."
      table.hashTable = {}
      count += 1
   table.printTable()
   
if __name__ == '__main__':
    main()
