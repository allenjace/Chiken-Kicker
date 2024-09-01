import pygame 
from pygame import mixer

class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect (0, 0 , 20, 20)
        self.offset = -125
        

    def draw_cursor(self):
        self.game.draw_text('*', 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h # + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50 # + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90# +80
        self.quitx, self.quity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) 
        

    def display_menu(self):
        self.backgroundimage = pygame.image.load('/Users/allenjace/Desktop/Chiken Kicker/assets/ACHoFe2GPYzlyWtFHaxnTxKvVnruOsDr.jpg.webp')
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0,205,255))
            self.game.draw_text('Chiken Kicker', 150, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 175)
            self.game.draw_text('Play Game', 40, self.startx, self.starty - 5) # -10
            self.game.draw_text('Options', 25, self.optionsx, self.optionsy - 5) # - 40
            self.game.draw_text('Credits', 25, self.creditsx, self.creditsy - 5) # + 10
            self.game.draw_text('Quit', 25, self.quitx, self.quity - 10)
            self.game.window.blit(self.backgroundimage, (0,0))
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                pygame.display.quit()
                pygame.quit()
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            #if self.game.START_KEY or self.game.BACK_KEY:
                #self.game_curr_menu = self.game.main_menu
                #self.run_display = False
            self.game.display.fill((0,205,255))
            self.game.draw_text('Nothing here', 100, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'Back':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game_curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill((0,205,255))
            self.game.draw_text('Credits:', 100, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Ryan Lu', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 75)
            self.game.draw_text('Allen Jace Pulido', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'Back':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
