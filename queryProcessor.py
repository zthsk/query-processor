import os
import sys
from hashtable import HashTable

class QueryProcessor:   
    def __init__(self, queries, inv_dir):
        self.queries = [q.lower() for q in queries]
        self.inv_dir = inv_dir
        self.accumulator = {}
        self.dict_file = f'{inv_dir}/dict.txt'
        self.post_file = f'{inv_dir}/post.txt'
        self.map_file = f'{inv_dir}/map.txt'
        self.hashtable = HashTable(15000)
        if self.checkFileExists(): sys.exit()
    
    #read the data from the inverted files from the line number the data is stored in
    @staticmethod   
    def readLineFile(file_path, line_number, bytes_to_read):
        byte_offset = line_number * bytes_to_read
        with open(file_path, 'rb') as file:
            file.seek(byte_offset)
            data = file.read(bytes_to_read)
            return data

    #check if the inverted file exists  
    def checkFileExists(self):
        flag = False
        if not os.path.exists(self.dict_file):
            print('Error: Dictionary File not found!!!')
            flag = True
        if not os.path.exists(self.post_file):
            print('Error: Postings File not found!!!')
            flag = True
        if not os.path.exists(self.map_file):
            print('Error: Mappings File not found!!!')
            flag = True
        return flag     
    
    #run the query processor to update the accumulator bucket
    def runQueryProcessor(self):
        for query in self.queries:
            dict_content = self.seekDictionary(query)
            if dict_content is not None:
                rec = Records(dict_content, self)
                postings = rec.seekPostings()
                self.updateAccumulator(postings)
            # else:
            #     print(f'{query} does not exist in dictionary!')
        

    #get the filename for the doc Id 
    def getFileName(self, doc_id):
        content = self.readLineFile(self.map_file, doc_id, bytes_to_read=18).decode()
        record = content.strip().split('|')
        record = [i.strip() for i in record]
        return record[1]
    
    #ge the dictionary content for a query token
    def seekDictionary(self, query):
        index = self.hashtable.__find__(query)
        while True:
            line_content = self.readLineFile(self.dict_file, index, bytes_to_read=43).decode()
            dict_rec = self.formatRecords(line_content)
            if dict_rec[0] == query:
                return dict_rec
            elif dict_rec[1] == -1:
                return None
            
            index += 1

    #update the accumulator bucket for the query
    def updateAccumulator(self, postings):
        for post in postings:
            doc_id, wt = post
            if doc_id in self.accumulator:
                self.accumulator[doc_id] += wt
            else:
                self.accumulator[doc_id] = wt

    #sort in descending order and return the final accumulated bucket
    def getAccumulator(self):
        return dict(sorted(self.accumulator.items(), key=lambda item: item[1], reverse=True))
    
    @staticmethod
    def formatRecords(content):
        record = content.strip().split('|')
        record = [i.strip() for i in record]
        record[1], record[2] = int(record[1]), int(record[2])
        return tuple(record)
    

            
class Records:
    def __init__(self, dict_content, queryprocessor):
        self.token, self.num_docs, self.start = dict_content
        # self.start = int(self.start)
        # self.num_docs = int(self.num_docs)
        self.postings = []
        self.qp = queryprocessor

    #format the dicionary and postings record 
    @staticmethod
    def formatRecords(content):
        record = content.strip().split('|')
        record = [i.strip() for i in record]
        record[0], record[1] = int(record[0]), float(record[1])
        return tuple(record)

    #get the postings for each query
    def seekPostings(self):
        for _ in range(self.num_docs):
            line_content = self.qp.readLineFile(self.qp.post_file, self.start, 21).decode()
            self.postings.append(self.formatRecords(line_content))
            self.start += 1
        return self.postings
