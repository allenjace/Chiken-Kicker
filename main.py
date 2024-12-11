import pygame 
import os
from cpu import *
from fighter import Fighter

pygame.init()
class Main():
    def __init__(self, screen_width, screen_height):
# create game window
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        # create screen display
        self.screen = None
        pygame.display.set_caption("Brawler")

        # set frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # define colors
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        # define fighter variables
        self.player_chicken_SIZE = 200
        self.player_chicken_SCALE = 1
        self.player_chicken_OFFSET = [0, 0]
        self.player_chicken_DATA = [self.player_chicken_SIZE, self.player_chicken_SCALE, self.player_chicken_OFFSET]
        self.cpu_chicken_SIZE = 200
        self.cpu_chicken_SCALE = 1
        self.cpu_chicken_OFFSET = [0, 0]
        self.cpu_chicken_DATA = [self.cpu_chicken_SIZE, self.cpu_chicken_SCALE, self.cpu_chicken_OFFSET]

        # load background image
        cwd = os.getcwd()
        bg_imagepath = (os.path.join(cwd, "background_3.jpg"))
        self.bg_image = pygame.image.load(bg_imagepath).convert_alpha()

        # load sprite sheets
        cwd = os.getcwd()
        player_chicken_imagepath = (os.path.join(cwd, "chkn_sprite_shit.png"))
        self.player_chicken_sheet = pygame.image.load(player_chicken_imagepath).convert_alpha()

        cpu_chicken_imagepath = (os.path.join(cwd, "cpu_sprite_shit.png"))
        self.cpu_chicken_sheet = pygame.image.load(cpu_chicken_imagepath).convert_alpha()

        # define number of steps in each animation
        self.player_chicken_ANIMATION_STEPS = [2, 7, 1, 5, 4, 4]
        self.cpu_chicken_ANIMATION_STEPS = [2, 7, 1, 5, 4, 4]
        
      # function for drawing background
    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))

    # function for drawing fighter health bars
    def draw_health_bar(self, health, x, y):
        self.ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * self.ratio, 30))
        
    def set_screen(self, screen, width, height):
            self.screen = screen
            self.SCREEN_WIDTH = width
            self.SCREEN_HEIGHT = height
            
            # Now that we have the screen dimensions, initialize fighters
            self.fighter_1 = Fighter(x=width // 4, y=height - 100, flip=False, data=self.player_chicken_DATA, sprite_sheet=self.player_chicken_sheet, animation_steps=self.player_chicken_ANIMATION_STEPS,width= width, height=height)
            self.fighter_2 = CPU(3 * width // 4, height - 100, True, self.cpu_chicken_DATA, self.cpu_chicken_sheet, self.cpu_chicken_ANIMATION_STEPS, width, height)
    # game loop
    def game_loop(self):

        if self.screen is None:
            return
        self.clock.tick(self.FPS)
        #draw background
        self.draw_bg()

        # show player stats
        self.draw_health_bar(self.fighter_1.health, 20, 20)
        self.draw_health_bar(self.fighter_2.health, self.SCREEN_WIDTH - 420, 20)


        # move fighters
        self.fighter_1.move(self.SCREEN_WIDTH,self.SCREEN_HEIGHT-100, self.screen, self.fighter_2)
        self.fighter_2.update_mvmt(self.SCREEN_WIDTH,self.SCREEN_HEIGHT-100,self.fighter_1)

        
        # update fighters
        self.fighter_1.update()
        self.fighter_2.update()

        # draw fighters
        self.fighter_1.draw(self.screen)
        self.fighter_2.draw(self.screen)


        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update display
        pygame.display.update()
