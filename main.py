import pygame 
from fighter import Fighter
from deck import *

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# create screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load background image
# bg_image = pygame.image.load("background_3.jpg").convert_alpha()

# load sprite sheets
warrior_sheet = pygame.image.load("warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("wizard.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


# function for drawing background
# def draw_bg():
#     scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
#     screen.blit(scaled_bg, (0, 0))

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    # pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    # pygame.draw.rect(screen, RED, (x, y, 400, 30))
    # pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

deck = Deck()

# create two objects of fighter
temp = [deck.deck[i] for i in range(1,7)]
print(temp)
fighter_1 = Fighter(300, 200, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, temp+deck.fill_hand(3,180))
fighter_2 = Fighter(600, 200, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, temp+deck.fill_hand(3,300))

# draw_bg()
screen.fill('black')
pygame.display.flip()

# draw fighters
fighter_1.draw(screen)
fighter_2.draw(screen)

# game loop
run = True
while run:
    print("----------------Turn start----------------")
    clock.tick(FPS)
    # draw background

    pygame.display.update()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    print("-------player pos-------")
    print("p1 ", fighter_1.rect.x, fighter_1.rect.y)
    print("p2 ", fighter_2.rect.x, fighter_2.rect.y)

    print ("-------draw card-------")
    fighter_1.print_cards()
    fighter_2.print_cards()

    print ("-------p1 turn-------")
    for i in range(0,3):
        choice = int(input("pick card: "))
        if choice > len(fighter_1.playerhand)-1 or choice < 0 or len(fighter_1.playerhand) == 0:
            break
        fighter_1.add_card(fighter_1.playerhand[choice])
        print("remaining cards ",fighter_1.playerhand)
        
    print ("-------p2 turn-------")
    for i in range(0,3):
        choice = int(input("pick card: "))
        if choice > len(fighter_2.playerhand)-1 or choice < 0 or len(fighter_2.playerhand) == 0:
            break
        fighter_2.add_card(fighter_2.playerhand[choice])
        print("remaining cards ",fighter_2.playerhand)

    print("-------playing cards-------")
    while (not fighter_2.playerqueue.empty()) or (not fighter_1.playerqueue.empty()):
        print("end turn")
        if not fighter_1.playerqueue.empty():
            f1_action = fighter_1.playerqueue.get()
            print('p1 action: ',f1_action)
            f1_hitbox = fighter_1.create_hitbox(f1_action)
            fighter_1.card_move(f1_action[3], fighter_2)
            
            print("p1 ", fighter_1.rect.x, fighter_1.rect.y)
        if not fighter_2.playerqueue.empty():
            f2_action = fighter_2.playerqueue.get()
            print('p2 action: ', f2_action)
            f2_hitbox = fighter_2.create_hitbox(f2_action)
            fighter_2.card_move(f2_action[3], fighter_1)
        # draw_bg()
        screen.fill('black')
        pygame.display.flip()
        
        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        pygame.draw.rect(screen, (255,0,0), f1_hitbox)
        pygame.draw.rect(screen, (255,0,0), f2_hitbox)

        print("-------Detect Collision-------")
        if f1_hitbox.colliderect(fighter_2.rect):
            print("f2 hit")
            fighter_2.health -= f1_action[7]
            fighter_2.card_move(f1_action[4], fighter_1)
        if f2_hitbox.colliderect(fighter_1.rect):
            print("f1 hit")
            fighter_1.health -= f2_action[7]
            fighter_1.card_move(f2_action[4], fighter_2)


    print("-------filling hand-------")
    fighter_1.playerhand.append(deck.fill_hand(3-len(fighter_1.playerhand),50))
    fighter_2.playerhand.append(deck.fill_hand(3-len(fighter_2.playerhand),50))
    

    # move fighters
    # fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)

    # update fighters
    # fighter_1.update()
    # fighter_2.update()
    

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

    next = input('next turn: ')
    if next=='q':
        break
#exist pygame
pygame.quit()
