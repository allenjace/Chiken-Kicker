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
        
        # Scale vertical spacing based on display height
        spacing = self.game.DISPLAY_H * 0.1  # 10% of screen height
        
        # Position menu items
        self.startx, self.starty = self.mid_w, self.mid_h - spacing
        self.optionsx, self.optionsy = self.mid_w, self.mid_h
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + spacing
        self.quitx, self.quity = self.mid_w, self.mid_h + spacing * 2
        
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) 
        self.mouseclick = False
        
        # set up background
        cwd = os.getcwd()
        self.backgroundpath =(os.path.join(cwd,'background.jpg.webp'))
        self.backgroundimage = pygame.image.load(self.backgroundpath)
        self.backgroundimage.set_alpha(200)

    # displays the menu while the game is still running
    def displayMenu(self):
        self.run_display = True
        
         # Scale font sizes based on display height
        title_size = int(self.game.DISPLAY_H * 0.1)  # 10% of screen height
        menu_item_size = int(self.game.DISPLAY_H * 0.03)  # 3% of screen height
        
        # Scale vertical positions
        self.title_y = self.game.DISPLAY_H * 0.1  # 10% from top
        self.play_y = self.game.DISPLAY_H * 0.4  # 40% from top
        self.options_y = self.game.DISPLAY_H * 0.5  # 50% from top
        self.credits_y = self.game.DISPLAY_H * 0.6  # 60% from top
        self.quit_y = self.game.DISPLAY_H * 0.7  # 70% from top
        
        while self.run_display:
            clock.tick(60)
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0,205,255))
            self.game.display.blit(self.backgroundimage, (0,0))
            
            self.game.drawText('Chicken Kicker', title_size, self.game.DISPLAY_W/2, self.title_y)
            self.game.drawText('Play Game', menu_item_size, self.game.DISPLAY_W/2, self.play_y)
            self.game.drawText('Options', menu_item_size, self.game.DISPLAY_W/2, self.options_y)
            self.game.drawText('Credits', menu_item_size, self.game.DISPLAY_W/2, self.credits_y)
            self.game.drawText('Quit', menu_item_size, self.game.DISPLAY_W/2, self.quit_y)
            
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

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game = game
        self.state = 'Back'
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)
        self.mouseclick = False
        self.lastclick = 0
        
        # Display settings
        self.resolutions = {
            'resolutions': [
                "1280x720",
                "1366x768",
                "1440x900",
                "1920x1080",
                "2560x1440",
                "3440x1440",
                "3840x2160"],
            'current_resolution_index': 0,
            'fullscreen': True}
        # UI elements
        self.settings_rects = {
            'resolution': pygame.Rect(self.game.DISPLAY_W / 2 + 150, self.game.DISPLAY_H / 2 - 155, 150, 30),
            'fullscreen': pygame.Rect(self.game.DISPLAY_W / 2 + 150,self.game.DISPLAY_H / 2 - 80, 150, 30)}
        self.dropdown_open = False

    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            self.checkInput()
            self.game.display.fill((0, 205, 255))
            
            # Draw menu options
            self.game.drawText('Options:', 75, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.drawText('Resolution', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.game.drawText('Fullscreen', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 75)
            self.game.drawText('Music coming soon!', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 25)
            self.game.drawText('Back', 25, self.backbuttonx, self.backbuttony - 5)
            
            self.drawCursor()
            self.blitScreen()
            self.checkMouse()
            self.display_settings()
            pygame.display.update()

    def display_settings(self):
        font = pygame.font.Font(None, 25)
        
        # Draw resolution dropdown
        pygame.draw.rect(self.game.window, (255, 255, 255), self.settings_rects['resolution'])
        current_res = self.resolutions['resolutions'][self.resolutions['current_resolution_index']]
        text = font.render(current_res, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.settings_rects['resolution'].center)
        self.game.window.blit(text, text_rect)
        
        # Draw resolution dropdown options if open
        if self.dropdown_open:
            for i, resolution in enumerate(self.resolutions['resolutions']):
                option_rect = pygame.Rect(
                    self.settings_rects['resolution'].x, 
                    self.settings_rects['resolution'].y + (i + 1) * self.settings_rects['resolution'].height,
                    self.settings_rects['resolution'].width,
                    self.settings_rects['resolution'].height)
                pygame.draw.rect(self.game.window, (255, 255, 255), option_rect)
                text = font.render(resolution, True, (0, 0, 0))
                text_rect = text.get_rect(center=option_rect.center)
                self.game.window.blit(text, text_rect)
        
        # Draw fullscreen toggle
        pygame.draw.rect(self.game.window, (255, 255, 255), self.settings_rects['fullscreen'])
        text = font.render("On" if self.resolutions['fullscreen'] else "Off", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.settings_rects['fullscreen'].center)
        self.game.window.blit(text, text_rect)

    def update_display_mode(self, new_resolution=None):
        # Update resolution if provided
        if new_resolution:
            width, height = map(int, new_resolution.split('x'))
            self.game.DISPLAY_W, self.game.DISPLAY_H = width, height
        else:
            width, height = self.game.DISPLAY_W, self.game.DISPLAY_H
        
        # Set display mode with current fullscreen setting
        flags = pygame.FULLSCREEN if self.resolutions['fullscreen'] else 0
        pygame.display.set_mode((width, height), flags)
        
        # Update menu positions
        self.mid_w, self.mid_h = width / 2, height / 2
        self.backbuttonx, self.backbuttony = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.backbuttonx + self.offset, self.backbuttony)
        
        # Update settings rects positions
        self.settings_rects['resolution'].x = width / 2 + 150
        self.settings_rects['resolution'].y = height / 2 - 155
        self.settings_rects['fullscreen'].x = width / 2 + 150
        self.settings_rects['fullscreen'].y = height / 2 - 80

    def checkMouse(self):
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and not self.mouseclick:
            self.mouseclick = True
            
            # Check resolution dropdown
            if self.settings_rects['resolution'].collidepoint(self.pos):
                self.dropdown_open = not self.dropdown_open
            elif self.dropdown_open:
                for i, _ in enumerate(self.resolutions['resolutions']):
                    option_rect = pygame.Rect(
                        self.settings_rects['resolution'].x,
                        self.settings_rects['resolution'].y + (i + 1) * self.settings_rects['resolution'].height,
                        self.settings_rects['resolution'].width,
                        self.settings_rects['resolution'].height
                    )
                    if option_rect.collidepoint(self.pos):
                        self.resolutions['current_resolution_index'] = i
                        new_resolution = self.resolutions['resolutions'][i]
                        self.update_display_mode(new_resolution)
                        self.dropdown_open = False
                        break
            
            # Check fullscreen toggle
            elif self.settings_rects['fullscreen'].collidepoint(self.pos):
                self.resolutions['fullscreen'] = not self.resolutions['fullscreen']
                self.update_display_mode()
            
            # Check back button
            elif self.mouseOnText('Back', self.backbuttonx, self.backbuttony - 5, 40):
                self.game.curr_menu = self.game.main_menu
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
