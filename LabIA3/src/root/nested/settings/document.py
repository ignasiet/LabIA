#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 12/05/2013

@author: Ignasi
'''
from pymongo import MongoClient
from pymongo import errors
import re
class document(object):
    '''
    classdocs
    '''
    ##Create the connection to the Database for all classes
    connection = MongoClient('localhost', 27017)
    db = connection['mydb']
    def __init__(self):
        '''
        Constructor
        '''
        self.dictionary = {}
        self.nome = None
        self.MaxFreq = 0
    
    def setName(self, title):
        self.nome = title
    
    def addWord(self, word):
        "This function creates the DF for every word"
        word = self.stripSpecialCharacters(word)
        if len(word) > 0 and not '\x00' in word:
            if self.dictionary.has_key(word):
                self.dictionary[word] = self.dictionary[word]+1
                if self.dictionary[word]>self.MaxFreq:
                    self.MaxFreq = self.dictionary[word] 
            else:
                self.dictionary[word] = 1          
            
    def stripSpecialCharacters(self, word):
        auxWord = re.sub('[!@#.,:;()/\-�]', '', word)
        return auxWord
    
    def insertRecord(self):
        "This function inserts the record in the database"
        post = {}
        post['ID_FILE_NAME'] = self.nome
        auxNames = self.nome.split('_')
        post['TYPE'] = auxNames[0]
        post['YEAR'] = auxNames[1]
        post['ID'] = auxNames[2].split('.')[0]
        post['PARAMVALUES'] = self.dictionary
        post['MAX_FREQUENCE_VALUE'] = self.MaxFreq
        try:
            id = document.db.documentos.insert(post)                        
        except errors.OperationFailure, e:
            print 'Error saving to database:', e
        except errors.InvalidDocument, e:
            print 'Error saving to database:', e
            print post 
        