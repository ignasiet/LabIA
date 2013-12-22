#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 11/05/2013

@author: Ignasi
'''
import sys
import os 
from root.nested.algorithms import naiveBayesTest, decisionTree, supportVectorMachine,\
    portfolioClassificator
from root.nested.settings.connectionMongoDB import fetchResultFiles,\
    cleanDatabaseSelected
from root.nested.settings import BuilderClass

def main(argv = None):
    if argv is None:
        argv=sys.argv
    print('Program Start.')
    print('-'*40)
    builder = BuilderClass.BuilderClass()
    mydata = raw_input('Do you want to import all words? (Re-calculate TFiDF)')
    auxPath = os.path.join(os.path.dirname(__file__), 'Files', 'inteiro_teor\*.*')
    deptPath = os.path.join(os.path.dirname(__file__), 'Files', 'csv')
    Path = os.path.join(os.path.dirname(__file__), 'Files')
    if mydata == 'yes':        
        auxCont = builder.countFiles(auxPath)
        builder.cleanDataBase()
        print "Number of files:", auxCont
        ##Import the words and calculate their frequency
        builder.importWords(auxPath)
        builder.calculateTF(auxPath, auxCont)
        builder.saveTFIDF(auxPath)
        ##Import the list of deputies
        builder.importCSVFiles(deptPath, 'deputados.csv')
        ##Import the train files
        builder.importCSVFiles(Path, 'train.csv')
        ##Import the test Files
        builder.importCSVFiles(Path, 'test.csv')
        ##import the presence files
        builder.importCSVFiles(deptPath, 'presence.csv')
        ##import the session files
        builder.importCSVFiles(deptPath, 'sessao.csv')
        ##import the session files
        builder.importCSVFiles(deptPath, 'sessao.csv')  
    else:       
        print ('Using data already stored.')            
    # #Starting test
    alg = False
    while alg == False:
        print 'MAIN MENU'
        print('-'*40)
        print 'Please, specify wich algorithm to use:'
        print '(1) Naive Bayes'
        print '(2) Decision Trees'
        print '(3) Decision Trees with Heuristic' 
        print '(4) Random Forests'
        print '(5) Support Vector Machines'
        print '(6) Combined Approach (Naive Bayes + Random Trees)'
        algorithm_select = raw_input()
        if algorithm_select == '1':
            alg = True
            print 'Starting Test-Prediction: Naive-Bayes'
            naiveBayes = naiveBayesTest.naiveBayesTest() 
            naiveBayes.testBayes()
        elif algorithm_select == '2':
            alg = True
            print 'Starting Test-Prediction: Decission Trees'
            decTree = decisionTree.decisionTree(1)
            decTree.createDecisionTree(Path)
        elif algorithm_select == '3':
            alg = True
            print 'Starting Test-Prediction: Decission Trees Optimized'
            decTree = decisionTree.decisionTree(2)
            decTree.createDecisionTree(Path)
        elif algorithm_select == '4':
            alg = True
            print 'Starting Test-Prediction: Random Forest'
            cleanDatabaseSelected('dtreeResult')
            decTree = decisionTree.decisionTree(2)
            decTree.createRDecisionTrees(Path)
        elif algorithm_select == '5':
            alg = True
            cleanDatabaseSelected('svmResults')
            print 'Starting Test-Prediction: Support Vector Machines'
            svm = supportVectorMachine.supportVectorMachine(2)
            svm.createSVMachine(Path)
        elif algorithm_select == '6':
            alg = True
            cleanDatabaseSelected('combinedResults')
            print 'Starting Test-Prediction: Combined approach'
            comb = portfolioClassificator.portfolioClassificator(2)
            comb.portofolioClassificator(Path)            
    writeOutputFile(algorithm_select)

def writeOutputFile(algorithm):
    if algorithm == '1':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputPredictMoreOptions.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles()
        for line in auxDict:
            auxString = str(line['id']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
    elif algorithm == '2':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputDecisionTree.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles('dtreeResult')
        for line in auxDict:
            auxString = str(line['Voter']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
    elif algorithm == '3':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputDTreeHeuristic.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles('dtreeResult')
        for line in auxDict:
            auxString = str(line['Voter']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
    elif algorithm == '4':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputRandomForests.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles('dtreeResult')
        for line in auxDict:
            auxString = str(line['Voter']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
    elif algorithm == '5':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputSVM.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles('svmResults')
        for line in auxDict:
            auxString = str(line['Voter']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
    elif algorithm == '6':
        Path = os.path.join(os.path.dirname(__file__), 'Files', 'outputCombined.csv')
        f = open(Path, 'w')
        auxDict = fetchResultFiles('combinedResult')
        for line in auxDict:
            auxString = str(line['id']) + ',' + str(line['vote']) + '\n'
            f.write(auxString)
        f.close()
           
if __name__ == '__main__':
    main()
    

