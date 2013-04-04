class Record:
   numberOfRecords = 0
   def __init__(self, dictionary, queryCode):
      Record.numberOfRecords += 1
      self.id           = Record.numberOfRecords
      
      self.title        = dictionary.get("Title", "")
      self.url          = dictionary.get("Url", "")
      self.source       = dictionary.get("Source", "")
      self.description  = dictionary.get("Description", "")
      self.queryCode    = queryCode
      #self.hashID       = dictionary.get("ID", "")
   
   def printRecord(self, keys = {'all': 1}):
      if keys.get("all", 0):
         print "Title = " + self.title
         print "URL = " + self.url
         print "Source = " + self.source
         print "Description = " + self.description
         print "queryCode = " + self.queryCode
      else:
         if keys.get("title", 0):
            print "Title = " + self.title
         if keys.get("URL", 0):
            print "URL = " + self.url
         if keys.get("Source", 0):
            print "Source = " + self.source
         if keys.get("Description", 0):
            print "Description = " + self.description
         if keys.get("queryCode", 0):
            print "queryCode = " + self.queryCode
