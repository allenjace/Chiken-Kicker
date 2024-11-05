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
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
        #self.screen.fill((0, 205, 255))
        # Set up font and its path
        cwd = os.getcwd()
        self.fontpath = os.path.join(cwd, 'Commodore Pixelized v1.2.ttf')
        self.font = pygame.font.Font(self.fontpath, 40)
        
        # set up main gameplay
        self.main_game = Main(self.DISPLAY_W, self.DISPLAY_H)
        self.stage_surface = None
        self.card_surface = None
        self.stage_initialized = False
        self.card_display_times = {}  # Store when each card was placed
        #self.card_display_duration = 3000  # 3 seconds in milliseconds

        # Timer variables (in seconds)
        self.clock = pygame.time.Clock()
        self.start_time = 5 * 60  # 5 minutes in seconds
        
        # Set up deck
        self.carddeck = Deck(self)
        self.current_card_id = None # current card id
        self.card_images = {} # to store card images
        self.card_rects = {} # to store card rect/outline
        #self.hand_cards = []  # To store cards in the player's hand
        self.running_cards = [] # place the cards u have at the moment
        self.max_hand_cards = 5  # Limit to 5 cards in the player's hand

        self.common_cards = [] # for the 5 movement cards the player will be able to use often
        self.addcommon_cards()
        # Load the first card into the deck area
        self.load_next_card()

         # Add source tracking for dragged cards
        self.dragged_from_hand = False
        self.card_positions = {}  # Store positions of cards on head {card_id: (x, y)}
        
        # State management for dragging cards
        self.moving = False
        self.selected_card_id = None

        # Store the card being right-clicked to show info
        self.display_cardinfo = None

    def run(self): # game loop
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        
        while self.running:
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            
            # If the pause menu is active, stop game logic and show the menu
            if self.pause_menu.menu_active:
                self.pause_menu.draw_menu()
                self.pause_menu.handle_input(events)      
                pygame.display.update()
                continue  # Skip the rest of the game logic when paused
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                        self.game.playing = False
                        self.game.curr_menu = self.game.main_menu
                        self.running = False
                    if event.key == pygame.K_ESCAPE:  # Toggle pause menu
                        self.pause_menu.toggle_menu()
                # Handle mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # LMB for dragging the card from deck
                        if  self.current_card_id and len(self.running_cards) < 3: 
                            rect = self.card_rects[self.current_card_id]
                            if rect.collidepoint(event.pos):
                                self.moving = True
                                self.selected_card_id = self.current_card_id
                                self.offset_x = rect.x - event.pos[0]
                                self.offset_y = rect.y - event.pos[1]
                                self.dragged_from_hand = False
                        # Check common cards in hand
                        for card_id in self.common_cards:
                            rect = self.card_rects[card_id]
                            if rect.collidepoint(event.pos):
                                if len(self.running_cards) < 3:
                                    self.moving = True
                                    self.selected_card_id = card_id
                                    self.offset_x = rect.x - event.pos[0]
                                    self.offset_y = rect.y - event.pos[1]
                                    self.dragged_from_hand = True
                                break
                    elif event.button == 3:  # RMB for showing description
                        for card_id, rect in self.card_rects.items():
                            if rect.collidepoint(event.pos):
                                self.display_cardinfo = card_id  # Store the card id to display info
                                break
                elif event.type == MOUSEMOTION and self.moving:
                    if self.selected_card_id is not None and self.selected_card_id in self.card_rects:
                        self.card_rects[self.selected_card_id].x = event.pos[0] + self.offset_x
                        self.card_rects[self.selected_card_id].y = event.pos[1] + self.offset_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.moving:
                        self.moving = False
                        # Different handling based on card source
                        if self.dragged_from_hand:
                            if self.selected_card_id not in self.running_cards and len(self.running_cards) < 3:
                                self.running_cards.append(self.selected_card_id)
                                self.card_display_times[self.selected_card_id] = pygame.time.get_ticks()
                            else:
                                if self.selected_card_id in self.card_positions:
                                    original_pos = self.card_positions[self.selected_card_id]
                                    self.card_rects[self.selected_card_id].topleft = original_pos
                        else:
                            if self.selected_card_id not in self.running_cards and len(self.running_cards) < 3:
                                self.running_cards.append(self.selected_card_id)
                                self.card_display_times[self.selected_card_id] = pygame.time.get_ticks()
                                self.load_next_card() # load next card from deck
                            self.selected_card_id = None
                            self.dragged_from_hand = False
                    elif event.button == 3:
                        self.display_cardinfo = None  # Hide card info on RMB release
            
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

             # Draw card being dragged last so it appears on top
            if self.moving and self.selected_card_id is not None:
                self.screen.blit(self.card_images[self.selected_card_id], self.card_rects[self.selected_card_id])
            # Draw card description if right-clicked
            if pygame.mouse.get_pressed()[2] and self.display_cardinfo is not None:
                card_name = self.carddeck.get_card_name(self.display_cardinfo)
                card_description = self.carddeck.get_card_description(self.display_cardinfo)
                self.card_info(card_name, card_description, self.card_rects[self.display_cardinfo])


            # Draw other UI elements
            self.createArena()
            self.createPlayerHand()
            self.createStage()

            # Update display
            pygame.display.flip()
    def addcommon_cards(self):
        # initalize the 5 common cards that will always be in the player hand
        self.commoncard_names = ["Move Left", "Move Right", "Move Up", "Move Down", "Kick"]

        # locate and store the IDs of the common cards
        for card_id, card_data in self.carddeck.deck.items():
            if card_data[0] in self.commoncard_names and len(self.common_cards) < 5:
                # Load the card image
                image_path = self.carddeck.get_card_img(card_id)
                self.card_images[card_id] = pygame.image.load(image_path).convert_alpha()
                self.common_cards.append(card_id)
                
        # Remove these cards from the shuffled deck
        for card_id in self.common_cards:
            if card_id in self.carddeck.shuffled_deck:
                self.carddeck.shuffled_deck.remove(card_id)
    def load_next_card(self):
        #Load the next card from the deck into the deck area.
        if self.carddeck.shuffled_deck:
            self.current_card_id = self.carddeck.shuffled_deck.pop(0)  # Get the next card
            image_path = self.carddeck.get_card_img(self.current_card_id)
            self.card_images[self.current_card_id] = pygame.image.load(image_path).convert_alpha()
            # Position card within the deck area
            self.card_width, self.card_height = self.card_images[self.current_card_id].get_size()
            self.card_x = int(self.DISPLAY_W * 0.86)  # Assuming 1920x1080 as base resolution
            self.card_y = int(self.DISPLAY_H* 0.825)
            self.card_x = min(self.card_x, self.DISPLAY_W - self.card_width)
            self.card_y = min(self.card_y, self.DISPLAY_H - self.card_height)
            self.card_rects[self.current_card_id] = self.card_images[self.current_card_id].get_rect(topleft=(self.card_x, self.card_y))
        else:
            self.current_card_id = None  # No more cards in the deck

    def countdown_timer(self, elapsed_time): # create a countdown timer of 5 minutes
        remaining_time = self.start_time - elapsed_time
        remaining_time = max(0, remaining_time)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.font.render(time_text, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=(self.DISPLAY_W // 2, 30))
        return timer_surface, timer_rect
    
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
        self.common_cards = []
        self.addcommon_cards()
        self.load_next_card()
        self.game.sound.music.play(1)
        self.start_ticks = pygame.time.get_ticks()
        self.running_cards.clear()
        self.card_positions.clear()
        self.moving = False
        self.selected_card_id = None
        self.dragged_from_hand = False
        
# def createQueue(self):
    #  self.queue = pygame.draw.rect(self.screen, ((255,255,255)), pygame.Rect((25, 50), (200, 700)), 2)

    def createPlayerHand(self):
        # Define the player hand area and return it for collision detection
        width = self.DISPLAY_W * 0.8
        height = self.DISPLAY_H * 0.15
        x = self.DISPLAY_W * 0.02
        y = self.DISPLAY_H * 0.82
        self.playerhand = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((x, y), (width, height)), 2)
        
        # Calculate card positions
        card_spacing = width / 9  # Divide by 6 to leave some margin
        
        # Draw the common cards
        for i, card_id in enumerate(self.common_cards):
            # Calculate card position
            card_width, card_height = self.card_images[card_id].get_size()
            card_x = x + (i + 0.5) * card_spacing - card_width/2
            card_y = y + height/2 - card_height/2
             # Store the position for collision detection
            self.card_positions[card_id] = (card_x, card_y)
            
            # Draw the card if it's not being dragged and it exists
            if not (self.moving and self.selected_card_id == card_id) and card_id in self.card_images:
                self.screen.blit(self.card_images[card_id], (card_x, card_y))
                
            # Update card rect
            if not self.moving or self.selected_card_id != card_id:
                self.card_rects[card_id] = self.card_images[card_id].get_rect(topleft=(card_x, card_y))  
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
        width = self.DISPLAY_W * 0.8
        height = self.DISPLAY_H * 0.625
        x = self.DISPLAY_W * 0.10
        y = self.DISPLAY_H * 0.11
        
        # Initialize surfaces once
        if not self.stage_initialized:
            self.stage_surface = pygame.Surface((width, height))
            self.card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            self.stage_rect = pygame.Rect(x, y, width, height)
            self.main_game.set_screen(self.stage_surface, width, height)
            if not hasattr(self, 'running_cards'):
                self.running_cards = []
            self.stage_initialized = True
        
        # Draw stage content first
        self.screen.blit(self.stage_surface, (x, y))
          
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(self.running_cards) == 3:
            # Clear all cards
            self.running_cards.clear()
            self.card_display_times.clear()
            self.card_positions.clear()

        # Draw remaining active cards
        if self.running_cards:
            fighter_pos = self.main_game.fighter_1.rect
            card_spacing = 100
            base_x = fighter_pos.centerx - (len(self.running_cards) * card_spacing) // 2
            
            for i, card_id in enumerate(self.running_cards): # place above the player head
                card_x = base_x + (i * card_spacing) + 100
                card_y = fighter_pos.top - self.card_height  + 50
                
                # Store the position for collision detection
                self.card_positions[card_id] = (card_x, card_y)
                
                # Draw directly to screen instead of card_surface
                # Draw the card
                if card_id in self.card_images:
                    self.screen.blit(self.card_images[card_id], (card_x, card_y))
        
        # Update game state
        self.main_game.game_loop()
        # Draw stage border
        #self.stage = pygame.draw.rect(self.screen, (255, 255, 255), self.stage_rect, 2)
        
class Deck(): # placeholder deck, will remove 
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
        "legendary": os.path.join(cwd, 'legendary_card.png')}
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
    

class PauseMenu: # class for the pause menu
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.game = self.gameworld.game
        self.mainmenu = self.game.main_menu
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
        self.font = pygame.font.Font(self.fontpath, 40)
        self.menu_options = ["Resume", "Restart", "Options", "Main Menu", "Quit"]
        self.options_menu_options = ["Music: On", "Back"]
        self.selected_option = 0
        self.menu_active = False
        self.options_active = False
        self.menu_rects = []
        
        # Cursor properties
        self.cursor_char = "*"
        self.cursor_offset = 20  # Distance from text
        
        # Cooldown timers
        self.last_key_time = pygame.time.get_ticks()
        self.last_click_time = pygame.time.get_ticks()
        self.last_toggle_time = pygame.time.get_ticks()
        self.key_cooldown = 200  # Milliseconds between key presses
        self.click_cooldown = 200  # Milliseconds between mouse clicks
        self.toggle_cooldown = 300  # Milliseconds between menu toggles

    def toggle_menu(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_toggle_time >= self.toggle_cooldown:
            self.menu_active = not self.menu_active
            self.options_active = False
            # Reset selected option when opening menu
            if self.menu_active:
                self.selected_option = 0
            self.last_toggle_time = current_time

    def draw_menu(self):
        # Draw semi-transparent background
        self.overlay = pygame.Surface((self.gameworld.DISPLAY_W, self.gameworld.DISPLAY_H), pygame.SRCALPHA)
        self.overlay.fill((0, 205, 255, 150))
        self.gameworld.screen.blit(self.overlay, (0, 0))

        # Draw menu background
        self.menu_width, self.menu_height = 450, 350
        self.menu_x = (self.gameworld.DISPLAY_W // 2) - (self.menu_width // 2)
        self.menu_y = (self.gameworld.DISPLAY_H // 2) - (self.menu_height // 2)

        pygame.draw.rect(self.gameworld.screen, (50, 50, 50), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 0)
        pygame.draw.rect(self.gameworld.screen, (255, 255, 255), (self.menu_x, self.menu_y, self.menu_width, self.menu_height), 2)

        if self.options_active:
            self.draw_options_menu()
        else:
            self.draw_main_menu()

    def draw_main_menu(self):
        # Draw menu options and cursor
        self.menu_rects = []
        for i, option in enumerate(self.menu_options):
            # Create text surface for the cursor (asterisk)
            cursor_surface = self.font.render(self.cursor_char, True, (255, 255, 255))
            
            # Create text surface for the menu option
            text_color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text_surface = self.font.render(option, True, text_color)
            
            # Position the text in the center
            text_rect = text_surface.get_rect(center=(self.gameworld.DISPLAY_W // 2, self.menu_y + 50 + i * 60))
            self.menu_rects.append(text_rect)
            
            # Draw the option text
            self.gameworld.screen.blit(text_surface, text_rect)
            
            # Draw cursor next to selected option
            if i == self.selected_option:
                cursor_rect = cursor_surface.get_rect(right=text_rect.left - 10, centery=text_rect.centery)
                self.gameworld.screen.blit(cursor_surface, cursor_rect)

    def draw_options_menu(self):
        # Update music option text based on current state
        self.options_menu_options[0] = f"Music: {'On' if not self.game.sound.music.get_volume() == 0 else 'Off'}"
        
        # Draw options title
        title_surface = self.font.render("Options", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.gameworld.DISPLAY_W // 2, self.menu_y + 40))
        self.gameworld.screen.blit(title_surface, title_rect)

        # Draw options and cursor
        self.menu_rects = []
        for i, option in enumerate(self.options_menu_options):
            cursor_surface = self.font.render(self.cursor_char, True, (255, 255, 255))
            
            text_color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text_surface = self.font.render(option, True, text_color)
            
            text_rect = text_surface.get_rect(center=(self.gameworld.DISPLAY_W // 2, self.menu_y + 120 + i * 60))
            self.menu_rects.append(text_rect)
            
            self.gameworld.screen.blit(text_surface, text_rect)
            
            if i == self.selected_option:
                cursor_rect = cursor_surface.get_rect(right=text_rect.left - 10,centery=text_rect.centery)
                self.gameworld.screen.blit(cursor_surface, cursor_rect)

    def handle_input(self, events):
        current_time = pygame.time.get_ticks()

        # Get keyboard input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if current_time - self.last_key_time >= self.key_cooldown:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % (len(self.options_menu_options) if self.options_active else len(self.menu_options))
                        self.last_key_time = current_time
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % (len(self.options_menu_options) if self.options_active else len(self.menu_options))
                        self.last_key_time = current_time
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if current_time - self.last_key_time >= self.key_cooldown:
                            self.select_option()
                            self.last_key_time = current_time
                    elif event.key == pygame.K_ESCAPE and self.options_active:
                        if current_time - self.last_toggle_time >= self.toggle_cooldown:
                            self.options_active = False
                            self.selected_option = 0
                            self.last_toggle_time = current_time

        # Handle mouse input with cooldown
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Update selection when hovering (no cooldown needed)
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_option = i
                
                # Handle clicks with cooldown
                if mouse_clicked and current_time - self.last_click_time >= self.click_cooldown:
                    self.select_option()
                    self.last_click_time = current_time

    def select_option(self):
        current_time = pygame.time.get_ticks()
        
        if self.options_active:
            if self.selected_option == 0:  # Music toggle
                if current_time - self.last_click_time >= self.click_cooldown:
                    if self.game.sound.music.get_volume() == 0:
                        self.game.sound.music.set_volume(0.5)  # Set to default volume
                    else:
                        self.game.sound.music.set_volume(0)
                    self.last_click_time = current_time
            elif self.selected_option == 1:  # Back
                if current_time - self.last_toggle_time >= self.toggle_cooldown:
                    self.options_active = False
                    self.selected_option = 0
                    self.last_toggle_time = current_time
        else:
            if self.menu_options[self.selected_option] == "Resume":
                self.menu_active = False
            elif self.menu_options[self.selected_option] == "Restart":
                self.menu_active = False
                self.gameworld.reset()
                self.gameworld.run()
            elif self.menu_options[self.selected_option] == "Options":
                if current_time - self.last_toggle_time >= self.toggle_cooldown:
                    self.options_active = True
                    self.selected_option = 0
                    self.last_toggle_time = current_time
            elif self.menu_options[self.selected_option] == "Main Menu":
                self.menu_active = False
                self.game.playing = False
                self.gameworld.reset()
                self.game.curr_menu = self.game.main_menu
                while self.game.running:
                    self.game.curr_menu.displayMenu()
                    if self.game.playing:
                        self.game.game_loop()
            elif self.menu_options[self.selected_option] == "Quit":
                pygame.quit()
                sys.exit()
