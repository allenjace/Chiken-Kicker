import pygame
import time
from game import *

class GameWorld():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.start = 180
        self.font.SysFont(None, 100)
        self.text = self.font.render(str(self.start), True, (0,128,0))
        self.timer_event = pygame.USEREVENT + 1
        pygame.timer.set_timer(self.timer_event, 1000)
        self.playing = True
        self.Timer()
    