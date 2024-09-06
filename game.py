import pygame
from menu import *
from pygame import mixer
from gameworld import GameWorld

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chicken Kicker')
        self.font_name = 'Commodore Pixelized v1.2.ttf'
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1270, 720
        self.display = pygame.Surface ((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode (((self.DISPLAY_W, self.DISPLAY_H)))
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        mixer.music.load('Kevin MacLeod - Pixelland  NO COPYRIGHT 8-bit Music.mp3')
        mixer.music.play(1)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill((0,205,255))
            self.draw_text('Game Over', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit game
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            
            if event.type ==  pygame.KEYDOWN:
                if event.key  == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    # 
    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        
    # function to reset keys
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False   