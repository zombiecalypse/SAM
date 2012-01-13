'''
Created on Jan 13, 2012

@author: panmari
'''

_languages = [dict(name = 'English', file='', soundFolder=''), 
                dict(name = 'Deutsch', file='translation_de', soundFolder='')]
    
def getAllLanguages():
    return _languages
    
def getCurrentLanguage():
    return None