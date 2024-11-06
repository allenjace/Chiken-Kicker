import pygame
import sys
import os
import random
from game import *
from deck import *
from menu import *
from pygame.locals import *
from fighter import *
from main import Main

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
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN | pygame.SCALED)
        #self.screen.fill((0, 205, 255))
        # Set up font and its path
        cwd = os.getcwd()
        self.fontpath = os.path.join(cwd, 'Commodore Pixelized v1.2.ttf')
        self.font = pygame.font.Font(self.fontpath, 40)
        
        # set up main gameplay
        self.main_game = Main(self.DISPLAY_W, self.DISPLAY_H)
        self.stage_surface = None
        self.stage_initialized = False

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
            image_path = self.carddeck.get_card_img(self.current_card_id) # get the card image file path
            # Load base card image
            base_card = pygame.image.load(image_path).convert_alpha()
            
            # Create a copy to draw on
            card_with_text = base_card.copy()
            
            # Get card name 
            card_name = self.carddeck.get_card_name(self.current_card_id)
            
            # Render card name
            font = pygame.font.Font(self.fontpath, 20)  # Smaller font for card name
            self.draw_text_on_card(card_with_text, card_name, font, (0, 0, 0)) # black text on the card

            self.card_images[self.current_card_id] = card_with_text # store completed card into the card image dictionary
            
            # Position card within the deck area
            self.card_width, self.card_height = self.card_images[self.current_card_id].get_size()
            self.card_x = int(self.DISPLAY_W * 0.86)  # Assuming 1920x1080 as base resolution
            self.card_y = int(self.DISPLAY_H* 0.825)
            self.card_x = min(self.card_x, self.DISPLAY_W - self.card_width)
            self.card_y = min(self.card_y, self.DISPLAY_H - self.card_height)
            self.card_rects[self.current_card_id] = self.card_images[self.current_card_id].get_rect(topleft=(self.card_x, self.card_y))
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
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            
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
                # Handle mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.current_card_id:  # LMB for dragging the card from deck
                        rect = self.card_rects[self.current_card_id]
                        if rect.collidepoint(self.mouse_pos):
                            self.moving = True
                            self.selected_card_id = self.current_card_id
                            self.offset_x = rect.x - self.mouse_pos[0]
                            self.offset_y = rect.y - self.mouse_pos[1]
                            #if len(self.hand_cards) < self.max_hand_cards:
                                # Place the card in the player hand
                                # self.hand_cards.append(self.selected_card_id)
                                #hand_x = len(self.hand_cards) * 100  # Position cards in the hand
                                # self.card_rects[self.selected_card_id].topleft = (hand_x - 75, 785)
                                # self.load_next_card()  # Load the next card from the deck
                                #  break
                    elif event.button == 3:  # RMB for showing description
                        for card_id, rect in self.card_rects.items():
                            if rect.collidepoint(self.mouse_pos):
                                self.display_cardinfo = card_id  # Store the card id to display info
                                break
                elif event.type == MOUSEMOTION and self.moving:
                    if self.selected_card_id is not None and self.selected_card_id in self.card_rects:
                        self.card_rects[self.selected_card_id].x = self.mouse_pos[0] + self.offset_x
                        self.card_rects[self.selected_card_id].y = self.mouse_pos[1] + self.offset_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.moving:
                        self.moving = False
                        
                        # Check if the card is placed in the player hand area
                        if self.createPlayerHand().collidepoint(self.mouse_pos):
                            if len(self.hand_cards) < self.max_hand_cards:
                                # Place the card in the player hand
                                self.hand_cards.append(self.selected_card_id)
                                self.hand_x = len(self.hand_cards) * 150  # Position cards in the hand
                                self.card_width, self.card_height = self.card_rects[self.selected_card_id].size
                                self.hand_horizontal_ratio = (self.hand_x - 75) / 1920 
                                self.hand_horizontal = int(self.DISPLAY_W * self.hand_horizontal_ratio)
                                self.hand_vertical = int(self.DISPLAY_H * 0.825)
                                self.hand_horizontal = max(0, min(self.hand_horizontal, self.DISPLAY_W - self.card_width))
                                self.hand_vertical = max(0, min(self.hand_vertical, self.DISPLAY_H - self.card_height))
                                self.card_rects[self.selected_card_id].topleft = (self.hand_horizontal, self.hand_vertical)
                                self.load_next_card()  # Load the next card from the deck
                            else:
                                print("Hand is full. No more cards can be added.")
                        elif self.selected_card_id == self.current_card_id:
                            self.card_rects[self.current_card_id] = self.card_images[self.current_card_id].get_rect(topleft=(self.card_x, self.card_y))
                        self.selected_card_id = None
                    elif event.button == 3:
                        self.display_cardinfo = None  # Hide card info on RMB release
            # If the pause menu is active, stop game logic and show the menu
            if self.pause_menu.menu_active:
                self.pause_menu.draw_menu()
                self.pause_menu.handle_input()      
                pygame.display.update()
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
    
    
    def card_info(self, card_name, card_description, rect):
        font = pygame.font.SysFont(None, 24)
        cardname_text = font.render(card_name, True, (255, 255, 255))
        description_text = font.render(card_description, True, (255, 255, 255))
        info_x = rect.right + 10
        info_y = rect.top + 25
        
        pygame.draw.rect(self.screen, (0, 0, 0), (info_x, info_y, 225, 60))
        self.screen.blit(cardname_text, (info_x + 5, info_y + 5))
        self.screen.blit(description_text, (info_x + 5, info_y + 30))
    
    def reset(self):
        self.stage_initialized = False
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
        width = self.DISPLAY_W * 0.8
        height = self.DISPLAY_H * 0.15
        x = self.DISPLAY_W * 0.02
        y = self.DISPLAY_H * 0.82
        self.playerhand = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((x, y), (width, height)), 2)
        return self.playerhand

    def createDeck(self):
        # Draw the deck area where cards are placed
        width = self.DISPLAY_W * 0.13
        height = self.DISPLAY_H * 0.15
        x = self.DISPLAY_W * 0.84
        y = self.DISPLAY_H * 0.82
        self.createdeck = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((x, y), (width, height)), 2)

    def createArena(self):
        # Draw the arena where you get knocked out
        width = self.DISPLAY_W * 0.95
        height = self.DISPLAY_H * 0.75
        x = self.DISPLAY_W * 0.02
        y = self.DISPLAY_H * 0.05
        self.arena = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((x, y), (width, height)), 2)

    def createStage(self): 
        # draw the stage area 
        width = self.DISPLAY_W * 0.8 # 80 percent of the display's width
        height = self.DISPLAY_H * 0.625 # 62.5 percent of the displays height
        x = self.DISPLAY_W * 0.10 # 10 percent of the display's width
        y = self.DISPLAY_H * 0.11 # 11 percent of the display's height
        
        # Initialize surfaces once
        if not self.stage_initialized:
            self.stage_surface = pygame.Surface((width, height)) # create the surface for the game stage
            self.card_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # create a surface for the cards with transparency (srcalpha)
            self.stage_rect = pygame.Rect(x, y, width, height) # creates a rectangle that defines the stage boundaries and is used for collision detection
            self.main_game.set_screen(self.stage_surface, width, height) # sets up the main game screen using the height and width of the stage
            if not hasattr(self, 'running_cards'): # keeps track of the cards that are currently placed above player
                self.running_cards = []
            self.stage_initialized = True # true when the stage is initialized
        
        # Draw stage content first
        self.screen.blit(self.stage_surface, (x, y))
          
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(self.running_cards) == 3: # when you press space and the active card count is 3
            # Clear all cards
            self.running_cards.clear()
            self.card_display_times.clear()
            self.card_positions.clear()

        # Draw remaining active cards
        if self.running_cards:
            fighter_pos = self.main_game.fighter_1.rect #get the player position to anchor the cards
            card_spacing = 100 # card space
            base_x = fighter_pos.centerx - (len(self.running_cards) * card_spacing) // 2 # calculate starting x to center cards abbove player/centers group of cards by accounting for total width
            
            for i, card_id in enumerate(self.running_cards): # draw each active card 
                card_x = base_x + (i * card_spacing) + 100 # card spacing with an offset from the base position
                card_y = fighter_pos.top - self.card_height  + 50 # place above the player head with an offset
                
                # Store the position for collision detection and management of cards
                self.card_positions[card_id] = (card_x, card_y)
                
                # Draw the card if it is in the card images dictionary
                if card_id in self.card_images:
                    self.screen.blit(self.card_images[card_id], (card_x, card_y))
        
        # Update game state
        self.main_game.game_loop()
        
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
        self.game = self.gameworld.game
        self.mainmenu = self.game.main_menu
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
        self.font = pygame.font.Font(self.fontpath, 40)  # Use the same font as the game
        self.menu_options = ["Resume", "Restart", "Options", "Main Menu", "Quit"]
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

        pygame.draw.rect(self.gameworld.screen, (50, 50, 50), (self.menu_x, self.menu_y, self.menu_width, self.menu_height + 50), 0)  # Menu box
        pygame.draw.rect(self.gameworld.screen, (255, 255, 255), (self.menu_x, self.menu_y, self.menu_width, self.menu_height + 50), 2)  # Menu border

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
        self.last_key_time = 0
        self.keys_cooldown = 150
        self.current_time = pygame.time.get_ticks()
        
        self.keys = pygame.key.get_pressed()
        if self.current_time - self.last_key_time > self.keys_cooldown:
            if self.keys == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)  # Cycle up through options
                self.last_key_time = self.current_time
            elif self.keys == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)  # Cycle down through options
                self.last_key_time = self.current_time

            if self.keys == pygame.K_RETURN:
                self.select_option()
                self.last_key_time = self.current_time

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
            self.menu_active = False
          # Close the pause menu and resume the game
        elif self.menu_options[self.selected_option] == "Restart":
            self.menu_active = False  # Close the pause menu
            self.gameworld.reset()
            self.gameworld.run()  # Restart the game loop
        elif self.menu_options[self.selected_option] == "Options":
            # add a new options page instead
            self.menu_active = False
        elif self.menu_options[self.selected_option] == "Main Menu":
            self.menu_active = False
            self.game.playing = False
            self.gameworld.reset()
            self.mainmenu.displayMenu() # stop game loop
            self.game.game_loop()
            self.gameworld.run()  # Restart the game loop
        elif self.menu_options[self.selected_option] == "Quit":
            pygame.quit()
            sys.exit()
