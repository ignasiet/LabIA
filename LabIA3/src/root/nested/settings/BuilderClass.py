'''
Created on 17/05/2013

@author: Ignasi
'''
import os
import csv
import glob
from root.nested.settings import document, Tfidf, StopWords
from root.nested.settings.connectionMongoDB import cleanDatabase, find, insertFiles,\
    fetchIDFArray, fetchResultFiles
from root.nested.settings.StopWords import isStopWord

class BuilderClass(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor of the IDF and TF
        '''
    
    def importCSVFiles(self, path, contentFileName):
        "Import the content of the diferent files of CSV"
        print "Importing train files:", contentFileName
        print('-'*40)
        rownum = 0  
        for filename in os.listdir(path):
            if filename==contentFileName:
                with open(os.path.join(path,filename)) as infile:
                    reader = csv.reader(infile)
                    for row in reader:
                        ##First row
                        auxDict = {}
                        if rownum == 0:
                            header = row
                            if contentFileName == 'test.csv':
                                header[0] = 'idvoto'
                        else:
                            colnum = 0
                            for col in row:
                                auxDict[header[colnum]] = col
                                colnum += 1
                            if contentFileName == 'train.csv':
                                insertFiles(auxDict, 'trial')
                            elif contentFileName == 'test.csv':
                                insertFiles(auxDict, 'test')
                            elif contentFileName == 'presence.csv':
                                insertFiles(auxDict, 'presence')
                            elif contentFileName == 'sessao.csv':
                                insertFiles(auxDict, 'sessao')
                            else:
                                insertFiles(auxDict, 'register')
                        rownum+=1
                                                    
    
    def cleanDataBase(self):
        "Clean the mongoDB: Documentos."
        cleanDatabase()
        print('Cleaning Database:')       

    def countFiles(self, Path):
        numberOfFiles = 0
        for files in glob.glob(Path):
            numberOfFiles = numberOfFiles + 1
        return numberOfFiles  
    
    def importWords(self, Path):
        """Open the file with read-only permit and
        put all words in the dictionaries
        Path contains the path to the files inside the project."""
        print('Fetching Documents:')
        # #Read all files
        for files in glob.glob(Path):
            print "Reading", files
            doc = document.document()
            dirname, filename = os.path.split(files)
            doc.setName(filename)
            ##Open file for reading
            f = open(files, 'r')
            lines = f.readlines() 
            for line in lines:
                line.replace('\0','')
                Data = line.split()
                try:
                    for word in Data:
                        ##If the word is not a stopWord and has len > 0
                        if not isStopWord(word) and len(word)>0:
                            doc.addWord(word)
                except IndexError:
                    print 'You have an empty row'
                # #Store the document in the db
            doc.insertRecord()
        
    def calculateTF(self, path, numberOfFiles):
        """This function calculates the TF of every word in the document"""
        "Number of files read"
        print "Calculating TF and IDF."
        print('-'*40)
        for files in glob.glob(path): 
            tfDoc = Tfidf.Tfidf(numberOfFiles)
            print "Fetching", files
            dirname, filename = os.path.split(files)
            tfDoc.calculateTfIdf(find(filename)) 
        Tfidf.insertIDF()
        print 'Execution completed. Database ready'
    
    def saveTFIDF(self, path):
        "This function calculates the TFIDF for every document"
        allFiles = fetchResultFiles('tfidf')
        idfArray = fetchIDFArray()['PARAMVALUES']
        for file in allFiles:
            auxDictionarySend = {}
            auxDictionary = {}
            texto = file['PARAMVALUES']
            auxDictionarySend['YEAR'] = file['YEAR']
            auxDictionarySend['TYPE'] = file['TYPE']
            auxDictionarySend['ID'] = file['ID']
            auxDictionarySend['ID_FILE_NAME'] = file['ID_FILE_NAME']
            for word in texto:
                auxValue = texto[word] * idfArray[word] 
                if auxValue > 0:
                    auxDictionary[word] = auxValue
            auxDictionarySend['PARAMVALUES'] = auxDictionary
            insertFiles(auxDictionarySend, 'tfidf')
        print 'Execution completed. Database ready'
        