import pygame
import os
import sys
from pygame.locals import *
from gameworld import *
from game import *

pygame.init()
clock = pygame.time.Clock()

class Menu():
    # initiates the display for the menu
    def __init__(self,game): 
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0 , 20, 20)
        self.offset = -150
        
         # set up path 
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd,'Commodore Pixelized v1.2.ttf'))
        
    # draws cursor for main menu navigation
    def drawCursor(self):
        self.game.drawText('*', 25, self.cursor_rect.x, self.cursor_rect.y)

    # 
    def blitScreen(self):
        self.game.window.blit(self.game.display, (0,0))
        self.game.resetKeys()

# Main Menu class that initiates states and variables for the menu screen
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h - 100 # + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 10# + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90# +80
        self.quitx, self.quity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) 
        self.mouseclick = False
        
    # displays the menu while the game is still running
    def displayMenu(self):
        cwd = os.getcwd()
        self.backgroundpath =(os.path.join(cwd,'background.jpg.webp'))
        self.background_x, self.background_y = 50, 0
        self.backgroundimage = pygame.image.load(self.backgroundpath)
        self.backgroundimage.set_alpha(128)# adds a background image
        self.run_display = True
        
        self.title_y = self.game.DISPLAY_H / 2 - self.game.DISPLAY_H * 0.4  # Adjust the title 40% from the center
        self.play_y = self.game.DISPLAY_H / 2 - self.game.DISPLAY_H * 0.1  # 10% above the center
        self.options_y = self.play_y + self.game.DISPLAY_H * 0.1  # 10% spacing below 'Play Game'
        self.credits_y = self.options_y + self.game.DISPLAY_H * 0.1  # 10% spacing below 'Options'
        self.quit_y = self.credits_y + self.game.DISPLAY_H * 0.1  # 10% spacing below 'Credits'
        while self.run_display:
            clock.tick(60)
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255))
            self.game.display.blit(self.backgroundimage, (0,0))
            self.game.drawText('Chicken Kicker', 125, self.game.DISPLAY_W/2, self.title_y-10)
            self.game.drawText('Play Game', 30, self.game.DISPLAY_W/2, self.play_y-5) # -10
            self.game.drawText('Options', 25, self.game.DISPLAY_W/2, self.options_y+10) # - 40
            self.game.drawText('Credits', 25, self.game.DISPLAY_W/2, self.credits_y-10) # + 10
            self.game.drawText('Quit', 25, self.game.DISPLAY_W/2, self.quit_y)
            self.drawCursor() # draws the cursor the be able to click on text
            self.blitScreen() 
            self.checkMouse() # checks for mouse input
            pygame.display.update()

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
        self.game = game
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)
        self.mouseclick = False
        self.lastclick = 0

    # function to display text, cursor for the options menu while the display is running
    # also checks if mouse is clicked
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255))
            self.game.drawText('Options:', 75, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.drawText('Mute', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 25)
            self.game.drawText('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.blitScreen()
            self.drawCursor()
            self.checkMouse()
            self.muteoption()
            pygame.display.update() 


    # fullscreen or windowed option
    #def change_viewmode(self):
        #self.pygame.display.toggle_fullscreen()
    # creates dropdown box of screen options
    #def screen_dropdown(self):

    def muteoption(self):
    # Create the button surface
        self.font = pygame.font.Font(None, 25)
        self.buttonsurface = pygame.Surface((150, 50))
        self.clickcooldown = 500
        
        # Set the button text depending on the music state
        if pygame.mixer.music.get_busy():
            self.text = self.font.render("Mute", True, (255, 255, 255))  # Display "Mute" if music is playing
        else:
            self.text = self.font.render("Unmute", True, (255, 255, 255))  # Display "Unmute" if music is paused

        self.centertext = self.text.get_rect(center=(self.buttonsurface.get_width() / 2, self.buttonsurface.get_height() / 2))
        self.buttonrect = pygame.Rect((self.game.DISPLAY_W / 2) + 75, (self.game.DISPLAY_H / 2) + 5, 150, 50)
        
        # Draw the button
        self.buttonsurface.fill((0, 205, 255))
        self.buttonsurface.blit(self.text, self.centertext)
        pygame.draw.rect(self.game.window, (255, 255, 255), self.buttonrect)
        self.game.window.blit(self.buttonsurface, (self.buttonrect.x, self.buttonrect.y))

        # Get the mouse position and detect clicks
        self.pos = pygame.mouse.get_pos()
        self.currentclick = pygame.time.get_ticks()
        
        # Check if the button is clicked
        if pygame.mouse.get_pressed()[0] == 1 and self.buttonrect.collidepoint(self.pos) and self.currentclick - self.lastclick > self.clickcooldown:
            # Toggle between mute/unmute when the button is clicked
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()  # Pause the music
                print("Music paused (muted)")
                self.text = self.font.render("Mute", True, (255, 255, 255))  # Display "Mute" if music is playing
            else:
                pygame.mixer.music.unpause()  # Unpause the music
                print("Music unpaused")
                self.text = self.font.render("Unmute", True, (255, 255, 255))  # Display "Unmute" if music is paused
            
            self.lastclick = self.currentclick

        # Reset the click detection so it doesn't continuously toggle on hold
        if pygame.mouse.get_pressed()[0] == 0:
            self.mouseclick = False
        


                    
    #checks if mouse was clicked
    def checkMouse(self):
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not self.mouseclick:
            self.mouseclick = True

            if self.mouseOnText('Back', self.backbuttonx, self.backbuttony - 5, 40):
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
        self.game = game
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
            self.game.drawText('Ryan Lu', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.drawText('Kenny Garcia', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.drawText('Allen Jace Pulido', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.drawText('Back', 25, self.backbuttonx, self.backbuttony - 5)
            self.drawCursor()
            self.blitScreen()
            self.checkMouse()
            pygame.display.update()

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
