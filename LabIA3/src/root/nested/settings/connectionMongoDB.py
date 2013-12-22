#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 15/05/2013

@author: Ignasi
'''
from pymongo import MongoClient, errors
import collections
class connectionMongoDB(object):
    connection = MongoClient('localhost', 27017)
    db = connection['mydb']

def cleanDatabase():
    "Clean the documentos Database in Mongo, previous to restart the program"
    connectionMongoDB.db.documentos.remove()
    connectionMongoDB.db.tf.remove()
    connectionMongoDB.db.idf.remove()
    connectionMongoDB.db.tfidf.remove()
    connectionMongoDB.db.register.remove()
    connectionMongoDB.db.result.remove()
    connectionMongoDB.db.dtreeResult.remove()
    connectionMongoDB.db.svmResults.remove()
    connectionMongoDB.db.trial.remove()
    connectionMongoDB.db.test.remove()
    connectionMongoDB.db.presence.remove()

def cleanDatabaseSelected(aDatabase):
    "Clean only the database selected"
    connectionMongoDB.db[aDatabase].remove()
    
    
def insert(object):
    "Insert the Object passed as an argument into the MongoDB"
    id = connectionMongoDB.db.documentos.insert(object)
    return id

def find(id_file_name):
    "Finds and return the document by id. Used to construct the TF-IDF"
    obj = connectionMongoDB.db.documentos.find_one({'ID_FILE_NAME': id_file_name}, fields={'_id': False, 'PARAMVALUES': True, 'ID_FILE_NAME': True, 'MAX_FREQUENCE_VALUE': True})
    return obj

def insertFiles(object, collection):
    "Insert a file of the trial document. Used to insert the results of the classifiers, and the TF-IDF."
    try:
        id = connectionMongoDB.db[collection].insert(object)
        return id
    except errors.OperationFailure, e:
            print 'Error saving to database:', e
    except errors.InvalidDocument, e:
            print 'Error saving to database:', e  

def fetchRandomTrialFiles(numOfFiles):
    "Used before only to test. Currently not used in code"
    try:
        obj = connectionMongoDB.db.trial.find({}, fields={'_id': False, 'vote': True, 'full_ref': True, 'deputado_id': True, 'number': True, 'year': True, 'type': True}, limit = int(numOfFiles))
    except:
        print 'Error retrieving trial files.'
    return obj

def fetchResultFiles(collection):
    "Returns the entire collection selected"
    try:
        obj = connectionMongoDB.db[collection].find({}, fields={'_id': False})
    except:
        print 'Error retrieving trial files.'
    return obj

def fetchListDeputies():
    "Get a list of all the deputies. Used to get their data about Party."
    try:
        obj = connectionMongoDB.db.register.find({}, fields={'_id': False, 'id':True, 'name':True, 'party':True, 'state':True})
        return obj
    except:
        print 'Error retrieving deputies.'
        
def fetchDeputyParty(aDeputyNumber):
    "Get the party of a deputy. Used to get their data about State."
    try:
        obj = connectionMongoDB.db.register.find_one({'id': aDeputyNumber}, fields={'_id': False, 'party':True, 'state':True})
        return obj
    except:
        print 'Error retrieving deputies.'

def fetchListVotes(aDeputy, aVote):
    "Get all the documents with votes of one deputy. Used in the classifiers of the SCIKIT"
    auxDict = {}
    try:
        obj = connectionMongoDB.db.trial.find({'deputado_id': aDeputy, 'vote': aVote}, fields={'_id': False, 'vote': True, 'full_ref': True, 'deputado_id': True, 'number':True, 'year': True, 'type': True})
        for item in obj:
            auxDict[item['full_ref']] = fetchDocument(item['number'], item['year'], item['type'])
        return auxDict
    except:
        print 'Error retrieving trial positive files.'

def fetchDocument(aLawName, aYear, aType):
    "Return the asked document. Used to get the tfidf for calculating the probabilities in the Naive Bayes."
    try:
        obj = connectionMongoDB.db.tfidf.find_one({'ID': aLawName, 'YEAR': aYear, 'TYPE': aType}, fields={'_id': False, 'PARAMVALUES': True, 'ID_FILE_NAME': True})
        if obj is not None:
            return_obj = sorted(obj['PARAMVALUES'].items(), key=lambda item: item[1], reverse = True)
            i = 0
            aux_obj = {}
            for word in return_obj:
                if i < 20:
                    aux_obj[word[0]] = word[1]
                    i+= 1
                else:
                    break
            obj = {}
            obj['PARAMVALUES'] = aux_obj
            return obj
    except:
        print 'Error retrieving file:', aLawName, aYear, aType
        
def fetchIDFArray():
    "Return the IDF document."
    try:
        obj = connectionMongoDB.db.idf.find_one({}, fields={'_id': False, 'PARAMVALUES': True})
        return obj
    except:
        print 'Error retrieving IDF file'
        
def fetchVote(aLawName, aYear, aType, aDeputy):
    "Returns the vote of a deputy, or the value Abstençao that will be trated after."
    try:
        obj = connectionMongoDB.db.trial.find_one({'number': aLawName, 'year': aYear, 'type': aType, 'deputado_id': aDeputy}, fields={'_id': False, 'vote': True, 'full_ref': True, 'deputado_id': True, 'number': True, 'year': True, 'type': True})
        if obj is not None:
            return obj['vote']
        else:
            return 'Abstencao'
    except:
        print 'Error retrieving votes.'
        
def fetchAssistance(aSessaoID, aDeputy):
    "Returns the assistance of a deputy to a session"
    try:
        obj = connectionMongoDB.db.presence.find_one({'deputado_id': aDeputy, 'sessao_id': aSessaoID}, fields={'_id': False})
        if obj is not None:
            return obj['presente']
        else:
            return '0'
    except:
        print 'Error retrieving votes.'

def fetchSessionType(sessao_id, aDate):
    "Returns the type of a session. ORDINARY or EXTRAORDINARY"
    try:
        obj = connectionMongoDB.db.sessao.find({'sessao_id': sessao_id.zfill(3), 'date':aDate}, fields={'_id': False})
        for item in obj:
            if item is not None:
                if item['type'].startswith('EXT'):
                    return '1'
                else:
                    return '0'
            else:
                return '1'
        print item
    except:
        print 'Error retrieving votes.'
