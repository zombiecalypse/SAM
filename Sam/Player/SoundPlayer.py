'''
Created on Dec 28, 2011

@author: panmari
'''

import pygame.mixer as player

class SoundPlayer(object):
    '''
    Helper class to play sounds
    '''
    def __init__(self):
        player.init()
    def play(self, soundfile):
        sound = player.Sound(soundfile)
        sound.play()