'''
Created on Dec 28, 2011

@author: panmari
'''
import SoundPlayer
class MissionPlayer(object):
    '''
    This class can be fed with an event (ie phase1start)
    and plays then the according sound file in the appropriate langauge.
    '''

    def __init__(self):
        self.player = SoundPlayer()
        self.player.play('test.ogg')
        
    def getSoundInLanguage(self, fileName):
        