import pygame, os
from menu import *
from pygame import mixer
from gameworld import *

# game class
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chicken Kicker') # displays Chicken Kicker as the caption of the window

        # set up path 
        cwd = os.getcwd('/Users/allenjace/Desktop/Chiken Kicker/')
        self.fontpath = (os.path.join(cwd,'Commodore Pixelized v1.2.ttf'))
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280,800
        self.display = pygame.Surface ((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode (((self.DISPLAY_W, self.DISPLAY_H)))
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.gameworld = GameWorld(self)
        self.curr_menu = self.main_menu

        # loads and plays music
        cwd = os.getcwd('/Users/allenjace/Desktop/Chiken Kicker/')
        self.musicpath = (os.path.join(cwd,'Kevin MacLeod - Pixelland  NO COPYRIGHT 8-bit Music.mp3'))
        mixer.music.load(self.musicpath)
        mixer.music.play(1)

    # game loop
    def game_loop(self):
        start_ticks = pygame.time.get_ticks()
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill((0,205,255))

            # Calculate the elapsed time for the countdown timer
            elapsed_ticks = pygame.time.get_ticks() - start_ticks
            elapsed_time = elapsed_ticks // 1000  # Convert milliseconds to seconds

            # Render the countdown timer on the game display
            timer_surface,timer_rect = self.gameworld.countdown_timer(elapsed_time)
            self.display.blit(timer_surface, timer_rect)  # Display the timer at the top-left corner

            # Check for menu and state transitions
            if self.main_menu.game.START_KEY:
                if self.main_menu.state == 'Start Game':
                    GameWorld.__init__(self)
            
            self.window.blit(self.display, (0,0))
            self.gameworld.createQueue()
            self.gameworld.createPlayerHand()
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
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True

    # 
    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font(self.fontpath, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
        
    # function to reset keys
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False   
