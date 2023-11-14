# Created by Thao Pham
# October 26, 2021
# Adapted Dr. Susan Gauch cpp version

from typing import NamedTuple
import atexit

class StringIntPair(NamedTuple):
    key: str
    data: int

class StringListPair(NamedTuple):
    key: str
    data: list

# numkeys = 40
class HashTable:
    def __init__(self, NumKeys):
        self.size = NumKeys * 3 # we want the hash table to be 2/3 empty
        self.used = 0
        self.collisions = 0
        self.lookups = 0

        # initialize the hashtable
        # self.hashtable = [StringIntPair('', 0)] * self.size
        self.hashtable = [StringListPair('', [])] * self.size

        # register cleanup when exit
        atexit.register(self.cleanup)

    # Similar to destructor in cpp to clean up resources
    def cleanup(self):
        self.hashtable.clear()

    # ------------------------------ Accessors ------------------------------
    
    # print the contents of the hash table currently, only prints non-null entries
    def print(self, filename):
        fpout = open(filename, 'w')

        for i in range(self.size):
            if self.hashtable[i].key != "":
                fpout.write(self.hashtable[i].key + " " + str(self.hashtable[i].data)+ "\n")

        fpout.close()
        print("Collisions: ", self.collisions, ", Used: ", self.used, 
        ", Lookups: ", self.lookups)


    # insert or add a word with its frequency count in hashtable
    def insert(self, key, data):
        index = -1
        if self.used >= self.size:
            print("The hashtable is full; cannot insert.")
        else:
            index = self.__find__(key)

            # If not already in the table, insert it
            if self.hashtable[index].key == "":       
                self.hashtable[index] = StringIntPair(key, [data])   
                # self.hashtable[index] = StringIntPair(key, data)
                # # self.hashtable[index].key = key
                # # self.hashtable[index].data = Data
                self.used += 1
            # else do nothing
            else:
                self.hashtable[index].data.append(data)

    # return the data or -1 if Key is not found
    def getData(self, key):
        self.lookups += 1
        index = self.__find__(key)
        if self.hashtable[index].key == "":
            return -1
        else:
            return self.hashtable[index].data

    # return the number of collisions
    def getUsage(self):
        return (self.used, self.collisions, self.lookups)
    
    # -------------------------- Private Functions ----------------------------

    # return the index of the word in the table, or the index of the free space in which to store the word
    def __find__(self, key):
        sum = 0
        index = -1

        # add all the characters of the key together
        for i in range(len(key)):
            sum = (sum * 19) + ord(key[i])   # Mult sum by 19, add byte value of char
   
        index = sum % self.size
        
        # Check to see if word is in that location
        # If not there, do linear probing until word found
        # or empty location found.
        while self.hashtable[index].key != key and self.hashtable[index].key != "":
            index = (index + 1) % self.size
            self.collisions += 1
       
        return index