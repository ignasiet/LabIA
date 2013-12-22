'''
Created on 23/05/2013

@author: Ignasi
'''
import os
import csv
from sklearn import svm
from root.nested.settings.connectionMongoDB import insertFiles,\
    fetchDeputyParty
from numpy.core.fromnumeric import size
from root.nested.settings.encoder import converter, decoder, encodeParty,\
    encodeState

class supportVectorMachine(object):
    '''
    classdocs
    '''
    def __init__(self, opt):
        '''
        Constructor
        '''
        self.option = opt
        
    def createSVMachine(self, path):
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
                clf = svm.SVC()
                clf.fit(x, y)
                ##self.printTree(clf)
                self.testPrediction(clf, path)
    
    def testPrediction(self, clf, path):        
        for filename in os.listdir(path):
            if filename=='test.csv':
                with open(os.path.join(path,filename)) as infile:
                    f = csv.reader(infile)
                    aux = f.next()
                    for line in f:
                        if self.option == 1:
                            data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[6]), converter(line[8])]
                        elif self.option == 2:
                            auxDeputy = fetchDeputyParty(line[2])
                            data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[6]), converter(line[8]), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state'])]
                        auxResult = clf.predict(data)
                        resultDict = {}
                        resultDict['Voter'] = line[0]
                        resultDict['vote'] = decoder(auxResult[0])
                        print 'id:', line[0], auxResult
                        insertFiles(resultDict, 'svmResults')