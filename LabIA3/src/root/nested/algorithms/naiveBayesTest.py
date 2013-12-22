'''
Created on 20/05/2013

@author: Ignasi
'''
from root.nested.settings.connectionMongoDB import fetchListVotes, fetchDocument, fetchIDFArray,\
    insertFiles, fetchResultFiles
from numpy import argmax

class naiveBayesTest(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''    
    def testBayes(self):
        dictTrial = fetchResultFiles('test')
        for item in dictTrial:
            ##Test for the document
            if len(item) > 0:
                print 'Trying to get the votes of the document:', item['full_ref'], 'for the deputy:', item['deputado_id']  
                votePredicted = self.predictDeputyVote(item['full_ref'], item['number'], item['year'], item['type'], item['deputado_id'] )
            else:
                ##Value by default: S
                votePredicted = 'S'
            insertItem = {}
            insertItem['id'] = item['idvoto']
            insertItem['vote'] = votePredicted
            print insertItem
            insertFiles(insertItem, 'result')
        
    def predictDeputyVote(self, document, number, year, aType, aDeputy):
        "Predictor of the vote of the deputy"
        valueVote = [0,0,0,0]
        valueVote[0] = 0 #Nao
        valueVote[1] = 0 #Sim
        ##valueVote[2] = 0 #Abs
        ##valueVote[3] = 0 #Obs
        valueVote[0] = self.calculeProbabilities(document, number, year, aType, fetchListVotes(aDeputy, 'S'))
        valueVote[1] = self.calculeProbabilities(document, number, year, aType, fetchListVotes(aDeputy, 'N'))
        ##valueVote[2] = self.calculeProbabilities(document, number, year, aType, fetchListVotes(aDeputy, 'A'))
        ##valueVote[3] = self.calculeProbabilities(document, number, year, aType, fetchListVotes(aDeputy, 'O'))
        index = self.argMax(valueVote)
        if index == 0:
            return 'S'
        elif index == 1:
            return 'N'
        elif index == 2:
            return 'A'
        elif index == 3:
            return 'O'
    
    def calculeProbabilities(self, documentName, number, year, aType, listOfDocuments):
        "Calculates the probabilities for every file-deputy tuple"
        auxValue = 1
        auxItem = fetchDocument(number, year, aType)
        if auxItem is not None:            
            originalLaw = fetchDocument(number, year, aType)['PARAMVALUES']
        else:
            ##The document doesnt exists
            return 0
        if len(listOfDocuments)==0:
            ##No votes of this type for the deputy
            return 0
        for word in originalLaw:
            for item in listOfDocuments:
                if item != documentName:
                    if listOfDocuments[item] is not None:
                        ##If document exists then we multiply:
                        auxList=listOfDocuments[item]['PARAMVALUES']
                        if auxList.has_key(word):
                            auxFl2 = float(auxList[word])
                            auxValorAnterior = auxValue
                            auxValue = float(auxValue) * float(auxFl2)
                            ##Python reduces the value to 0.
                            ##case when some number is < 10^-55
                            if auxValue == 0:
                                return auxValorAnterior
        return auxValue
     
    def argMax(self, list):
        max = 0
        maxIndex = 0
        for i in range(len(list)):
            if list[i] > max:
                max = list[i]
                maxIndex = i
        return maxIndex
          
            