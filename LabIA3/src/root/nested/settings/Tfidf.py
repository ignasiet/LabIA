'''
Created on 15/05/2013

@author: Ignasi
'''
from root.nested.settings.connectionMongoDB import insertFiles
from math import log
class Tfidf(object):
    numberOfFiles = 0
    IDFDictionary = {}
    
    def __init__(self, numberOfFiles):
        self.dictionary = {}
        self.outPutDict = {}
        self.Nome = None
        self.MaxFreq = 0
        Tfidf.numberOfFiles = numberOfFiles
    
    def setMaxFreq(self, maxFreq):
        self.MaxFreq = maxFreq
    
    def calculateTfIdf(self, dictOld):
        "Read the dictionary and create another with the calculated TF-values"
        self.Nome = dictOld['ID_FILE_NAME']
        self.MaxFreq = dictOld['MAX_FREQUENCE_VALUE']
        self.dictionary = dictOld['PARAMVALUES']
        self.insertTF(dictOld)
    
    def insertTF(self, dictionaryOLD): 
        "Calculate the TF for each document."       
        for key in self.dictionary:
            if len(key)>0:
                if Tfidf.IDFDictionary.has_key(key):
                    Tfidf.IDFDictionary[key] = Tfidf.IDFDictionary[key] + 1
                else:
                    Tfidf.IDFDictionary[key] = 1
                self.outPutDict[key] = float(self.dictionary[key])/self.MaxFreq
        self.insertRecord(self.outPutDict)
    
    def insertRecord(self, dictionary):
        "Insert new records of TF"
        newDictionary = {}
        newDictionary['ID_FILE_NAME'] = self.Nome
        newDictionary['PARAMVALUES'] = dictionary
        auxNome = self.Nome.split('_')
        newDictionary['TYPE'] = auxNome[0]
        newDictionary['YEAR'] = auxNome[1]
        newDictionary['ID'] = auxNome[2].split('.')[0]            
        insertFiles(newDictionary, 'tf')
    
def insertIDF():
    base = 10
    for key in Tfidf.IDFDictionary:
        Tfidf.IDFDictionary[key] = log(Tfidf.numberOfFiles / Tfidf.IDFDictionary[key], base)
    newDictionary = {}
    newDictionary['PARAMVALUES'] = Tfidf.IDFDictionary
    newDictionary['ID_FILE_NAME'] = 'IDF_DOCUMENT'
    insertFiles(newDictionary, 'idf')


    
