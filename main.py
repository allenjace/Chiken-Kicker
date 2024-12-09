import pygame 
import os
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
        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72, 56]
        self.WARRIOR_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET]
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [112, 107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET]

        # load background image
        cwd = os.getcwd()
        bg_imagepath = (os.path.join(cwd, "background_3.jpg"))
        self.bg_image = pygame.image.load(bg_imagepath).convert_alpha()

        # load sprite sheets
        cwd = os.getcwd()
        warrior_imagepath = (os.path.join(cwd, "warrior.png"))
        self.warrior_sheet = pygame.image.load(warrior_imagepath).convert_alpha()
        wizard_imagepath = (os.path.join(cwd, "wizard.png"))
        self.wizard_sheet = pygame.image.load(wizard_imagepath).convert_alpha()

        # define number of steps in each animation
        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
        
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
            self.fighter_1 = Fighter(x=width // 4, y=height - 100, flip=False, data=self.WARRIOR_DATA, sprite_sheet=self.warrior_sheet, animation_steps=self.WARRIOR_ANIMATION_STEPS,width= width, height=height)
            self.fighter_2 = CPU(3 * width // 4, height - 300, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, width, height)
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
