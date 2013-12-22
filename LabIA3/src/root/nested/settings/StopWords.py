#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 12/05/2013

@author: Ignasi
'''
 
class StopWords(object):
    """Represents the words we don't take into account."""
    words = ['o', 'O', 'um', 'Um', 'uma', 'Uma', 'e', 'do', '-', ',', '.', '', '\\', '/',
                      'a', 'A', 'os', 'Os', 'as', 'As', 'uns', 'umas', 'Uns', 'Umas',
                      'de', 'De', 'dos', 'Dos', 'da', 'Das', 'que', 'e', 'para', 'com'
                      'n�o', 'no', 'se', 'na', 'por', 'mais', 'mas', 'como', 'ao', 'ele'
                      '�', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'j�', 'eu', 'tambem'
                      's�', 'pelo', 'pela', 'at�', 'isso', 'ela', 'entre', 'depois', 'sem'
                      'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 
                      'eles', 'voc�', 'essa', 'num', 'pelos', 'elas', 'qual', 'nos', 'lhe',
                      'deles', 'essas', 'esses', 'pelas', 'este', 'dele', '']
    
def isStopWord(word):
    "Verify if the word is a Stop Word"
    auxWord = word.lower()
    if auxWord in StopWords.words:
        return True
    else:
        return False
    
    def __init__(self):
        '''
        Constructor
        '''    
    