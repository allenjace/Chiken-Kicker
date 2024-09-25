import pygame, os, sys
from pygame import mixer
from gameworld import *
from game import *

pygame.init()

class Menu():
    # initiates the display for the menu
    def __init__(self,game): 
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect (0, 0 , 20, 20)
        self.offset = -125
        
         # set up path 
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd,'Commodore Pixelized v1.2.ttf'))
        
    # draws cursor for main menu navigation
    def drawCursor(self):
        self.game.drawText('*', 25, self.cursor_rect.x, self.cursor_rect.y)

    # 
    def blitScreen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.resetKeys()

# Main Menu class that initiates states and variables for the menu screen
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h # + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50 # + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90# +80
        self.quitx, self.quity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) 
        self.mouseclick = False
        
    # displays the menu while the game is still running
    def displayMenu(self):
        cwd = os.getcwd()
        self.backgroundpath =(os.path.join(cwd,'ACHoFe2GPYzlyWtFHaxnTxKvVnruOsDr.jpg.webp'))
        self.backgroundimage = pygame.image.load(self.backgroundpath) # adds a background image
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255))
            self.game.display.blit(self.backgroundimage, (0,0))
            self.game.drawText('Chicken Kicker', 100, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 175)
            self.game.drawText('Play Game', 30, self.startx, self.starty - 5) # -10
            self.game.drawText('Options', 25, self.optionsx, self.optionsy - 5) # - 40
            self.game.drawText('Credits', 25, self.creditsx, self.creditsy - 5) # + 10
            self.game.drawText('Quit', 25, self.quitx, self.quity - 10)
            self.drawCursor() # draws the cursor the be able to click on text
            self.blitScreen() 
            self.checkMouse() # checks for mouse input

    #checks the mouse is clicked
    def checkMouse(self):
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not self.mouseclick:
            self.mouseclick = True

            if self.mouseOnText('Play Game', self.startx, self.starty - 5, 30):
                self.game.playing = True
                self.run_display = False
            elif self.mouseOnText('Options', self.optionsx, self.optionsy - 5, 25):
                self.game.curr_menu = self.game.options
                self.run_display = False
            elif self.mouseOnText('Credits', self.creditsx, self.creditsy - 5, 25):
                
                self.game.curr_menu = self.game.credits
                self.run_display = False
            elif self.mouseOnText('Quit', self.quitx, self.quity - 10, 25):
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0] == 0:
            self.mouseclick = False

    #checks if the mouse is over text
    def mouseOnText(self, text, x, y, font_size):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + text_width and y <= mouse_y <= y + text_height

    # moves the cursor based on the state it is currently on
    def moveCursor(self):
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

    #checks if the enter or back button is clicked and an action will happen
    def checkInput(self):
        self.moveCursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

#class for the options menu
class OptionsMenu(Menu):
    #initiates states and button for the options menu
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)
        self.mouseclick = False

    # function to display text, cursor for the options menu while the display is running
    # also checks if mouse is clicked
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255))
            self.game.drawText('Options:', 75, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.drawText('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.drawCursor()
            self.blitScreen()
            self.checkMouse()


    # fullscreen or windowed option
    #def change_viewmode(self):
        #self.pygame.display.toggle_fullscreen()
    # creates dropdown box of screen options
    #def screen_dropdown(self):


    #checks if mouse was clicked
    def checkMouse(self):
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not self.mouseclick:
            self.mouseclick = True

            if self.mouseOnText('Back', self.backbuttonx, self.backbuttony - 5, 25):
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            else:
                self.game.curr_menu = self.game.options
                self.run_display = False
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.mouseclick = False

    #checks if the mouse is over text
    def mouseOnText(self, text, x, y, font_size):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + text_width and y <= mouse_y <= y + text_height
    
    #checks for specific keyboard input
    def checkInput(self):
        if self.game.START_KEY:
            if self.state == 'Back':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

#class to initiate the credits state
class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)
        self.mouseclick = False

    #function to display text for the credits menu
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255)) # fills the display with cyan color
            self.game.drawText('Credits:', 75, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.drawText('Ryan Lu', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 35)
            self.game.drawText('Kenny Garcia', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.drawText('Allen Jace Pulido', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.drawText('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.drawCursor()
            self.blitScreen()
            self.checkMouse()

    #checks if mouse was clicked
    def checkMouse(self):
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not self.mouseclick:
            self.mouseclick = True

            if self.mouseOnText('Back', self.backbuttonx, self.backbuttony - 5, 25):
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            else:
                self.game.curr_menu = self.game.credits
                self.run_display = False
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.mouseclick = False

    #checks if the mouse is over text
    def mouseOnText(self, text, x, y, font_size):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + text_width and y <= mouse_y <= y + text_height
    
    #checks for specific keyboard input
    def checkInput(self):
        if self.game.START_KEY:
            if self.state == 'Back':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
