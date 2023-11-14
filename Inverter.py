import os
import math
from ply import lex
from hashtable import HashTable
import sys
import nltk
from nltk.corpus import stopwords
#from HTMLLexer import HTMLLexer

nltk.download('stopwords')

class HTMLInverter:
    #initizlize
    def __init__(self, total_docs):
        self.total_docs = 0           
        self.frequency = {}
        self.longest_key = 30
        self.global_ht = []
        self.global_ht = HashTable(15000)
        self.stopwords = stopwords.words('english')

    #initialize the global hash table after getting the no of tokens
    # def buildGlobalHT(self):
    #     self.global_ht = HashTable(self.n_tokens)  

    #after processing a document, this function is called to update global_ht
    def updateGlobalHT(self, doc_id, freq, num_toks):

        for key in freq:
            # if len(key) > self.longest_key:
            #     self.longest_key = len(key)
            self.global_ht.insert(key,[doc_id, freq[key]/num_toks, freq[key]])  # freq of that token/ total
                                                                    # num tokens in doc
            
    def truncate_key(self, key):
        return key[:self.longest_key]

    #opens inputFile, tokenizes it, then writes the tokens to outputFile. updates the frequency count of tokens
    def processTokens(self, tokens, doc_id):
        #Count the frequency of tokens for this file
        freq = {}
        for x in tokens:
            if len(x) == 1 or x in self.stopwords: continue
            if (x in freq):
                freq[self.truncate_key(x)] += 1
            else:
                freq[self.truncate_key(x)] = 1
        
        num_tok = len(tokens)

        self.total_docs += 1
        #update the global count of token frequencies
        self.updateGlobalHT(doc_id, freq, num_tok)


    def format_dict_record(self, key, num_docs, start):
        key = key.ljust(self.longest_key)
        num_docs = str(num_docs).ljust(4)
        start = str(start).ljust(6)

        sep = '|'

        record = key + sep + num_docs + sep + start + "\n"
        return record
    
    def format_post_record(self, doc_id, wt):
        doc_id = str(doc_id).ljust(4)
        wt = str(wt)[:15].ljust(15)

        sep = '|'

        record = doc_id + sep + wt + "\n"
        return record

    def finish(self, dir_name):
        f_dict = os.path.join(dir_name, "dict.txt")
        f_post = os.path.join(dir_name, "post.txt")

        # iterate over sorted keys and write dict and post files
        start = 0
        for idx in range(self.global_ht.size):
            # num_docs = len(self.global_ht[key])
            data_pairs = self.global_ht.hashtable[idx]
            key = data_pairs.key
            num_docs = len(data_pairs.data)
            write_post = True
            with open(f_dict, 'a') as f:
                # filter out low frequency words
                if num_docs > 1 or (num_docs > 0 and data_pairs.data[0][2] > 1):
                    f.write(self.format_dict_record(key,num_docs,start))
                else:
                    write_post = False
                    f.write(self.format_dict_record("empty",-1,-1))

            #write the post file
            if write_post:
                with open(f_post, 'a') as f:
                    for x in data_pairs.data:
                        idf = 1 + math.log10(self.total_docs/num_docs)    # idf computation (correct?)
                        
                        f.write(self.format_post_record(x[0],idf*x[1])) # idf * rtf
                    start += num_docs
                