'''
Created on 21/05/2013

@author: Ignasi
'''
import numpy as np
import os
import csv
import datetime
from root.nested.settings.connectionMongoDB import fetchDeputyParty,\
    insertFiles, fetchAssistance, fetchSessionType
from sklearn.tree import tree 
from sklearn.ensemble import RandomForestClassifier
import StringIO
import pydot
from numpy.core.fromnumeric import size
from root.nested.settings.encoder import converter, encodeParty, encodeState,\
    decoder

class decisionTree(object):
    '''
    classdocs
    '''
    def __init__(self, opt):
        '''
        Constructor
        '''
        self.option = opt
    
    def createDecisionTree(self, path):
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
                clf = tree.DecisionTreeClassifier()
                clf.fit(x, y)
                ##self.printTree(clf)
                self.testPrediction(clf, path, 'dtreeResult')
    
    def createRDecisionTrees(self, path):
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
                                presence = fetchAssistance(line[7], line[2])
                                sessao = fetchSessionType(line[7], line[8])
                                data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[7]), converter(line[9]), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state']), converter(presence), converter(sessao)]
                                y.append(converter(line[6]))
                                x.append(data)
                clf = RandomForestClassifier(n_estimators=5)
                clf.fit(x, y)
                ##self.printTree(clf)
                self.testPrediction(clf, path, 'dtreeResult')
    
    def testPrediction(self, clf, path, database):        
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
                            presence = fetchAssistance(line[6], line[2])
                            sessao = fetchSessionType(line[6], line[7])
                            data = [converter(line[2]), converter(line[3]), converter(line[4]), converter(line[6]), converter(line[8]), encodeParty(auxDeputy['party']), encodeState(auxDeputy['state']), converter(presence), converter(sessao)]
                        auxResult = clf.predict(data)
                        resultDict = {}
                        resultDict['Voter'] = line[0]
                        resultDict['vote'] = decoder(auxResult[0])
                        print 'id:', line[0], auxResult
                        insertFiles(resultDict, database)
    
    def printTree(self, clf):
        dot_data = StringIO.StringIO() 
        tree.export_graphviz(clf, out_file=dot_data) 
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'treeClassifier.pdf') 
        graph.write_pdf(Path) 
