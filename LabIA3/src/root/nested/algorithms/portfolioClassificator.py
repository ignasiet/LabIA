'''
Created on 25/05/2013

@author: Ignasi
'''
from root.nested.settings.connectionMongoDB import insertFiles, fetchDeputyParty,\
    fetchResultFiles, fetchListVotes, fetchDocument
import os
from os import path
import csv
from numpy.core.fromnumeric import size
from sklearn.ensemble.forest import RandomForestClassifier
from root.nested.settings.encoder import converter, decoder, encodeParty,\
    encodeState

class portfolioClassificator(object):
    '''
    classdocs
    '''
    def __init__(self, opt):
        '''
        Constructor
        '''
        self.option = opt
        
    def portofolioClassificator(self, Path):
        dictTrial = fetchResultFiles('test')
        ##Init the classifier:
        classifier = self.initDecTrees(Path)
        for item in dictTrial:
            ##Test for the document
            if len(item) > 0:
                votePredicted = self.predictDeputyVote(item['full_ref'], item['number'], item['year'], item['type'], item['deputado_id'] )
            else:
                ##Value of the classificator
                auxDeputy = fetchDeputyParty(item['deputado_id'])
                data = [converter(item['deputado_id']), converter(item['year']), converter(item['number']), converter(item['sessao_id']), converter(item['type']), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state'])]
                votePredicted = self.decoder(classifier.predict(data)[0])
            insertItem = {}
            insertItem['id'] = item['idvoto']
            if votePredicted == 'Draw':
                auxDeputy = fetchDeputyParty(item['deputado_id'])
                data = [converter(item['deputado_id']), converter(item['year']), converter(item['number']), converter(item['sessao_id']), converter(item['type']), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state'])]
                votePredicted = decoder(classifier.predict(data)[0])
            insertItem['vote'] = votePredicted
            print insertItem
            insertFiles(insertItem, 'combinedResult')  
    
    def initDecTrees(self, path):
        for filename in os.listdir(path):
            if filename=='train.csv':
                with open(os.path.join(path,filename)) as infile:
                    f = csv.reader(infile)
                    aux = f.next()  # skip the header
                    x = []
                    y = []
                    for line in f:
                        if size(line) > 1:
                            if self.option == 1:
                                data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[7]), converter(line[9])]
                                y.append(converter(line[6]))
                                x.append(data)
                            elif self.option == 2:
                                auxDeputy = fetchDeputyParty(line[2])
                                data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[7]), converter(line[9]), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state'])]
                                y.append(converter(line[6]))
                                x.append(data)
                clf = RandomForestClassifier(n_estimators=5)
                clf.fit(x, y)
                return clf
    
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
        if valueVote[0] == valueVote[1]:
            return 'Draw'
        else:
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
                        auxList=listOfDocuments[item]['PARAMVALUES']
                        if auxList.has_key(word):
                            auxFl2 = float(auxList[word])
                            auxValorAnterior = auxValue
                            auxValue = float(auxValue) * float(auxFl2)
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