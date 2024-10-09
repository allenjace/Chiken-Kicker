import pygame
import os
from menu import *
from pygame import *
from gameworld import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chicken Kicker') # displays Chicken Kicker as the caption of the window
        # set up path 
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd,'Commodore Pixelized v1.2.ttf'))
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screeninfo = pygame.display.Info()
        self.DISPLAY_W, self.DISPLAY_H = self.screeninfo.current_w, self.screeninfo.current_h
        #self.DISPLAY_W, self.DISPLAY_H = 1280,800 
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H),pygame.FULLSCREEN)
        self.display = pygame.Surface ((self.DISPLAY_W, self.DISPLAY_H))
        #self.window = pygame.display.set_mode ((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.gameworld = GameWorld(self)
        self.curr_menu = self.main_menu

        # loads and plays music
        cwd = os.getcwd()
        self.musicpath = (os.path.join(cwd,'Kevin MacLeod - Pixelland  NO COPYRIGHT 8-bit Music.mp3'))
        pygame.mixer.init()
        self.sound = pygame.mixer
        self.sound.music.load(self.musicpath)
        self.sound.music.play(-1)

    # game loop
    def game_loop(self):
        while self.playing:
            self.checkEvents()
            if self.START_KEY:
                self.playing = False
            self.display.fill((0,205,255))

            self.gameworld.run()

            self.window.blit(self.display, (0,0))
            self.resetKeys()
            pygame.display.update()

    def checkEvents(self):
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
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True

    # 
    def drawText(self, text, size, x, y, outline_color=(0, 175, 255), text_color=(255, 255, 255), outline_thickness=3.5):
        pygame.font.init()
        font = pygame.font.Font(self.fontpath, size)
        
        # Render the text itself
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Render the outline by rendering the text slightly offset in all directions
        outline_surfaces = []
        for dx in [-outline_thickness, 0, outline_thickness]:
            for dy in [-outline_thickness, 0, outline_thickness]:
                if dx != 0 or dy != 0:  # Skip the center point (original text)
                    outline_surface = font.render(text, True, outline_color)
                    outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
                    self.display.blit(outline_surface, outline_rect)

        # Blit the original text on top of the outline
        self.display.blit(text_surface, text_rect)


#function to reset keys
    def resetKeys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False


if __name__ == "__main__":
    runGame = Game()
    while runGame.running:
        runGame.curr_menu.displayMenu()
        runGame.game_loop()
