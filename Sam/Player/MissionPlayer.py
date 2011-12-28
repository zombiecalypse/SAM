'''
Created on Dec 28, 2011

@author: panmari
'''
import SoundPlayer
class MissionPlayer():
    '''
    This class can be feeded with an event (ie phase1start)
    and plays then the according soundfile in the appropriate langauge.
    '''

    def __init__(self):
        self.player = SoundPlayer()
        self.player.play('test.ogg')