import pygame, sys, os
from game import *

class GameWorld:
    def __init__(self,game):
        # Initialize pygame
        pygame.init()

        # Set up display
        self.screen_width, self.screen_height = 1280,800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill((0,205,255))
        # Set up font and its path
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
        self.font = pygame.font.Font(self.fontpath, 40)
        
        # Timer variables (in seconds)
        self.clock = pygame.time.Clock()
        self.start_time = 5 * 60  # 5 minutes in seconds

    def countdown_timer(self, elapsed_time):
        # Calculate the remaining time
        remaining_time = self.start_time - elapsed_time
        if remaining_time < 0:
            remaining_time = 0
        
        # Convert remaining time to minutes and seconds
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        
        # Render the timer text
        time_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.font.render(time_text, True, (255, 255, 255))

        # Center the timer at the top of the screen
        timer_rect = timer_surface.get_rect(center=(self.screen_width // 2, 40))  # 40 pixels from the top
        return timer_surface, timer_rect

    # counting time
    def run(self):
        self.start_ticks = pygame.time.get_ticks()  # Start counting time
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Calculate elapsed time
            elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
            elapsed_time = elapsed_ticks // 1000  # Convert milliseconds to seconds

            # Fill the screen with a color (background)
            self.screen.fill((0, 0, 0))

            # Render and display the countdown timer at the top
            timer_surface, timer_rect= self.countdown_timer(elapsed_time)
            self.screen.blit(timer_surface, timer_rect) #Positioning at the top middle
            
            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            self.clock.tick(60)


    def createQueue(self):
        pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 50), (200, 550)), 2)


    def createPlayerHand(self):
        pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 625), (900, 150)), 2)


#class PauseMenu(GameWorld):
   # self.GameWorld.screen.fill((0,205,255))
    #self.game.draw_text('Nothing here', 75, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
    #self.game.draw_text('Back', 25, self.backbuttonx, self.backbuttony - 5)
    
    #def check_events():

    
       # self.game.check_events()
            #self.check_input()
            #self.draw_cursor()
            #self.blit_screen()
            #self.check_mouse_click()
