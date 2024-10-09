import pygame
import sys
import os
import random
from game import *
from deck import *
from menu import *
from pygame.locals import *

# Initialize pygame
pygame.init()

class GameWorld:
    def __init__(self, game):
        self.game = game
        self.pause_menu = PauseMenu(self)
        # Set up display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screeninfo = pygame.display.Info()
        self.DISPLAY_W, self.DISPLAY_H = self.screeninfo.current_w, self.screeninfo.current_h
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN)
        self.screen.fill((0, 205, 255))
        # Set up font and its path
        cwd = os.getcwd()
        self.fontpath = os.path.join(cwd, 'Commodore Pixelized v1.2.ttf')
        self.font = pygame.font.Font(self.fontpath, 40)
        
        # Timer variables (in seconds)
        self.clock = pygame.time.Clock()
        self.start_time = 5 * 60  # 5 minutes in seconds
        
        # Set up deck
        self.carddeck = Deck(self)
        self.current_card_id = None # current card id
        self.card_images = {} # to store card images
        self.card_rects = {} # to store card rect/outline
        self.hand_cards = []  # To store cards in the player's hand
        self.max_hand_cards = 5  # Limit to 5 cards in the player's hand

        # Load the first card into the deck area
        self.load_next_card()

        # State management for dragging cards
        self.moving = False
        self.selected_card_id = None

        # Store the card being right-clicked to show info
        self.display_cardinfo = None

    def load_next_card(self):
        #Load the next card from the deck into the deck area.
        if self.carddeck.shuffled_deck:
            self.current_card_id = self.carddeck.shuffled_deck.pop(0)  # Get the next card
            image_path = self.carddeck.get_card_img(self.current_card_id)
            self.card_images[self.current_card_id] = pygame.image.load(image_path).convert_alpha()
            # Position card within the deck area
            self.card_rects[self.current_card_id] = self.card_images[self.current_card_id].get_rect(topleft=(1235, 775))
        else:
            self.current_card_id = None  # No more cards in the deck

    def countdown_timer(self, elapsed_time):
        remaining_time = self.start_time - elapsed_time
        remaining_time = max(0, remaining_time)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.font.render(time_text, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=(self.DISPLAY_W // 2, 30))
        return timer_surface, timer_rect

    def run(self):
        self.start_ticks = pygame.time.get_ticks()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                        self.game.playing = False
                        self.game.curr_menu = self.game.main_menu
                        running = False
                    if event.key == pygame.K_ESCAPE:  # Toggle pause menu
                        self.pause_menu.toggle_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.current_card_id:  # LMB for dragging the card from deck
                        rect = self.card_rects[self.current_card_id]
                        if rect.collidepoint(mouse_pos):
                            self.moving = True
                            self.selected_card_id = self.current_card_id
                            self.offset_x = rect.x - mouse_pos[0]
                            self.offset_y = rect.y - mouse_pos[1]
                           #if len(self.hand_cards) < self.max_hand_cards:
                                # Place the card in the player hand
                               # self.hand_cards.append(self.selected_card_id)
                                #hand_x = len(self.hand_cards) * 100  # Position cards in the hand
                               # self.card_rects[self.selected_card_id].topleft = (hand_x - 75, 785)
                               # self.load_next_card()  # Load the next card from the deck
                              #  break
                    elif event.button == 3:  # RMB for showing description
                        for card_id, rect in self.card_rects.items():
                            if rect.collidepoint(mouse_pos):
                                self.display_cardinfo = card_id  # Store the card id to display info
                                break
                elif event.type == MOUSEMOTION and self.moving:
                    if self.selected_card_id is not None and self.selected_card_id in self.card_rects:
                        self.card_rects[self.selected_card_id].x = mouse_pos[0] + self.offset_x
                        self.card_rects[self.selected_card_id].y = mouse_pos[1] + self.offset_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.moving:
                        self.moving = False
                        # Check if the card is placed in the player hand area
                        if self.createPlayerHand().collidepoint(mouse_pos):
                            if len(self.hand_cards) < self.max_hand_cards:
                                # Place the card in the player hand
                                self.hand_cards.append(self.selected_card_id)
                                hand_x = len(self.hand_cards) * 100  # Position cards in the hand
                                self.card_rects[self.selected_card_id].topleft = (hand_x - 75, 775)
                                self.load_next_card()  # Load the next card from the deck
                            else:
                                print("Hand is full. No more cards can be added.")
                        self.selected_card_id = None
                    elif event.button == 3:
                        self.display_cardinfo = None  # Hide card info on RMB release
             # If the pause menu is active, stop game logic and show the menu
            if self.pause_menu.menu_active:
                self.pause_menu.draw_menu()
                self.pause_menu.handle_input()
                pygame.display.update()
                self.clock.tick(60)
                continue  # Skip the rest of the game logic when paused
            
            # Fill the screen with background color
            self.screen.fill((0, 205, 255))
            # Display the countdown timer at the top
            elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
            elapsed_time = elapsed_ticks // 1000
            timer_surface, timer_rect = self.countdown_timer(elapsed_time)
            self.screen.blit(timer_surface, timer_rect)

            # Draw deck area and current card in the deck
            self.createDeck()
            if self.current_card_id:
                self.screen.blit(self.card_images[self.current_card_id], self.card_rects[self.current_card_id])

            # Draw cards in the player's hand
            for card_id in self.hand_cards:
                self.screen.blit(self.card_images[card_id], self.card_rects[card_id])

            # Draw card description if right-clicked
            if pygame.mouse.get_pressed()[2] and self.display_cardinfo is not None:
                card_name = self.carddeck.get_card_name(self.display_cardinfo)
                card_description = self.carddeck.get_card_description(self.display_cardinfo)
                self.card_info(card_name, card_description, self.card_rects[self.display_cardinfo])

            # Draw other UI elements
            self.createArena()
            self.createPlayerHand()
            self.createStage()
            #self.createQueue()

            # Update display
            pygame.display.flip()
            self.clock.tick(60)
    
    def card_info(self, card_name, card_description, rect):
        font = pygame.font.SysFont(None, 24)
        cardname_text = font.render(card_name, True, (255, 255, 255))
        description_text = font.render(card_description, True, (255, 255, 255))
        info_x = rect.right + 10
        info_y = rect.top
        
        pygame.draw.rect(self.screen, (0, 0, 0), (info_x, info_y, 225, 60))
        self.screen.blit(cardname_text, (info_x + 5, info_y + 5))
        self.screen.blit(description_text, (info_x + 5, info_y + 30))
    
    def reset(self):
         # Set up deck again
        self.carddeck = Deck(self)
        self.current_card_id = None 
        self.hand_cards = []  
        self.load_next_card()
        self.start_ticks = pygame.time.get_ticks()

    
   # def createQueue(self):
      #  self.queue = pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 50), (200, 700)), 2)

    def createPlayerHand(self):
        # Define the player hand area and return it for collision detection
        self.playerhand = pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 775), (1100, 150)), 2)
        return self.playerhand

    def createDeck(self):
        # Draw the deck area where cards are placed
        self.createdeck = pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((1175, 775), (250, 150)), 2)

    def createArena(self):
        # Draw the arena where you get knocked out
        self.arena = pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 50), (1400, 700)), 2)
    
    def createStage(self):
        # Draw the stage area 
        self.stage = pygame.draw.rect(self.screen, ((0, 0, 0)), pygame.Rect((150, 125), (1100, 525)), 2)

class Deck():
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.deck = self.create_deck()
        self.shuffled_deck = list(self.deck.keys())  # Shuffle the deck
        random.shuffle(self.shuffled_deck)
        print("Deck created")
    
    def create_deck(self) -> dict:
        deck = dict()
        
        cwd = os.getcwd()
        self.image_path = {
        "common": os.path.join(cwd, 'common_card.png'),
        "rare": os.path.join(cwd, 'rare_card.png'),
        "epic": os.path.join(cwd, 'epic_card.png'),
        "legendary": os.path.join(cwd, 'legendary_card.png'),
        }
        # Common cards
        deck[len(deck) + 1] = ["Move Left", "Moves Left", "common"]
        deck[len(deck) + 1] = ["Move Right", "Moves Right", "common"]
        deck[len(deck) + 1] = ["Move Up", "Moves Up", "common"]
        deck[len(deck) + 1] = ["Move Down", "Moves Down", "common"]
        deck[len(deck) + 1] = ["Duck", "Duck Down", "common"]
        deck[len(deck) + 1] = ["Kick", "Kick aimed towards the family jewels", "common"]
        
        # Rare cards
        deck[len(deck) + 1] = ["Back Kick", "Happy de ume tsukushite", "rare"]
        deck[len(deck) + 1] = ["Flying Kick", "Soaring through the air feet first", "rare"]
        deck[len(deck) + 1] = ["Roundhouse Kick", "Kick with extra knockback", "rare"]
        deck[len(deck) + 1] = ["Axe Kick", "Kick with a chance to stun", "rare"]
        deck[len(deck) + 1] = ["Knee Strike", "Quick knee to the chin", "rare"]
        
        # Epic cards
        deck[len(deck) + 1] = ["Spinning Back Kick", "A powerful spinning kick", "epic"]
        deck[len(deck) + 1] = ["Flying Knee", "A flying knee strike", "epic"]
        deck[len(deck) + 1] = ["Tornado Kick", "Let it rip!", "epic"]
        deck[len(deck) + 1] = ["Sky Drop", "Drop from the sky", "epic"]
        
        # Legendary card
        deck[len(deck) + 1] = ["Roids", "Jump Higher, Run Faster, Kick Harder", "legendary"]
        
        return deck
    
    def get_card_name(self, id: int) -> str:
        return self.deck[id][0]

    def get_card_description(self, id: int) -> str:
        return self.deck[id][1]
    
    def get_card_img(self, id: int) -> str:
        card_type  = self.deck[id][2]
        return self.image_path[card_type]
    

class PauseMenu:
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.game = Game
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
        self.font = pygame.font.Font(self.fontpath, 40)  # Use the same font as the game
        self.menu_options = ["Resume", "Restart", "Options", "Quit"]
        self.selected_option = 0  # Track which option is selected
        self.menu_active = False  # Track if the menu is active
        self.menu_rects = []  # Store button rects for each menu option

    def toggle_menu(self):
        # Toggle the pause menu on/off.
        self.menu_active = not self.menu_active

    def draw_menu(self):
        # Draw the pause menu in the center of the screen
        # Draw semi-transparent background
        self.overlay = pygame.Surface((self.gameworld.DISPLAY_W, self.gameworld.DISPLAY_H), pygame.SRCALPHA)
        self.overlay.fill((0, 205, 255, 150))  # Black with 150 alpha for transparency
        self.gameworld.screen.blit(self.overlay, (0, 0))

        # Draw menu options
        self.menu_width, self.menu_height = 300, 300
        self.menu_x = (self.gameworld.DISPLAY_W // 2) - (self.menu_width // 2)
        self.menu_y = (self.gameworld.DISPLAY_H // 2) - (self.menu_height // 2)

        pygame.draw.rect(self.gameworld.screen, (50, 50, 50), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 0)  # Menu box
        pygame.draw.rect(self.gameworld.screen, (255, 255, 255), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 2)  # Menu border

        # Draw each option
        self.menu_rects = []
        for i, option in enumerate(self.menu_options):
            text_color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text_surface = self.font.render(option, True, text_color)
            text_rect = text_surface.get_rect(center=(self.gameworld.DISPLAY_W // 2, self.menu_y + 50 + i * 60))
            self.gameworld.screen.blit(text_surface, text_rect)
            self.menu_rects.append(text_rect)

    def handle_input(self):
        #Handle keyboard and mouse input for the pause menu.
        self.keys = pygame.key.get_pressed()
        if self.keys == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)  # Cycle up through options
        elif self.keys == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)  # Cycle down through options

        if self.keys == pygame.K_RETURN:
            self.select_option()

        # Handle mouse input
        self.mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(self.mouse_pos):
                self.selected_option = i
                if pygame.mouse.get_pressed()[0]:
                    self.select_option()

    def select_option(self):
        #Perform action based on the selected option.
        if self.menu_options[self.selected_option] == "Resume":
            self.toggle_menu()  # Close the pause menu and resume the game
        elif self.menu_options[self.selected_option] == "Restart":
            self.toggle_menu()  # Close the pause menu
            self.gameworld.reset()
            self.gameworld.run()  # Restart the game loop
        elif self.menu_options[self.selected_option] == "Options":
            # add a new options page instead
            self.gameworld.curr_menu = self.gameworld.game.options
            self.toggle_menu()
        elif self.menu_options[self.selected_option] == "Quit":
            pygame.quit()
            sys.exit()
