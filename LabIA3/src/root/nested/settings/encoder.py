'''
Created on 26/05/2013

@author: Ignasi
'''

class encoder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
def converter(x):
        if x == 'PL':
            return 1
        elif x == 'PDC':
            return 2
        elif x == 'MPV':
            return 3
        elif x == 'PEC':
            return 4
        elif x == 'PLP':
            return 5
        elif x == 'REP':
            return 6
        elif x == 'S':
            return 1
        elif x == 'N':
            return 2
        elif x=='A':
            return 3
        elif x=='O':
            return 4
        else:
            return float(x)

def decoder(x):
        if x == 1:
            return 'S'
        elif x == 2:
            return 'N'
        elif x == 3:
            return 'A'
        elif x == 4:
            return 'O'   
        
def encodeParty(x):
        if x == 'DEM':
            return 1
        elif x == 'PCdoB':
            return 2
        elif x == 'PDT':
            return 3
        elif x == 'PEN':
            return 4
        elif x == 'PHS':
            return 5
        elif x == 'PMDB':
            return 6
        elif x == 'PMN':
            return 7
        elif x == 'PP':
            return 8
        elif x =='PPS':
            return 9
        elif x == 'PR':
            return 10
        elif x == 'PRB':
            return 11
        elif x == 'PRP':
            return 12
        elif x == 'PRTB':
            return 13
        elif x == 'PSB':
            return 14
        elif x == 'PSC':
            return 15
        elif x == 'PSD':
            return 16
        elif x == 'PSDB':
            return 15
        elif x == 'PSL':
            return 16
        elif x == 'PSOL':
            return 17
        elif x == 'PT':
            return 18
        elif x == 'PTB':
            return 19
        elif x == 'PTC':
            return 20
        elif x == 'PTdoB':
            return 21
        elif x == 'PV':
            return 22
    
def encodeState(x):
        options = {'AC':1, 'AL':2, 'AM':3,
                   'AP':4, 'BA':5, 'CE':6,
                   'DF':7, 'ES':8, 'GO':9,
                   'MA':10, 'MG':11, 'MS':12,
                   'MT':13, 'PA':14, 'PB':16,
                   'PE':17, 'PT':18, 'PR':19,
                   'RJ':20, 'RN':21, 'RO':22,
                   'RR':23, 'SC':24, 'SE':25,
                   'SP':26, 'TO':27}
        return options.get(x, 28) 