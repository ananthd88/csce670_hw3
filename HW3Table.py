import HW3Record as Record

class Table:
   def __init__(self):
      self.records = []
      self.hashTable = {}
      self.queries = []
   def addRecord(self, record):
      existingRecord = self.hashTable.get(record.title, 0)
      if existingRecord:
         print "Duplicate hashID found"
         return 0
      else:
         self.hashTable[record.title] = record
         self.records.append(record)
         return 1
   def printTable(self):
      for record in self.records:
         print self.queries[record.queryCode] + " -> " + record.title
   def findTFIDF(self):
      
