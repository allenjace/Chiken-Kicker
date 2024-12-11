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
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        #self.screen.fill((0, 205, 255))
        
        # Set up font and its path
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
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
        self.max_hand_cards = 10  # Limit to 5 cards in the player's hand

        self.common_cards = [] # for the 5 movement cards the player will be able to use often
        self.random_cards = [] # 5 random cards
        self.addcommon_cards()
        # Load the first card into the deck area
        self.load_next_card()
        self.first_spacebarpress = True
         # Add source tracking for dragged cards
        self.dragged_from_hand = False
        self.card_positions = {}  # Store positions of cards on head {card_id: (x, y)}
        
        # State management for dragging cards
        self.moving = False
        self.selected_card_id = None

        # Store the card being right-clicked to show info
        self.display_cardinfo = None
        
        # death
        self.winlose = WinLose(self)
        self.game_ended = False 

    def run(self):
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        
        while self.running:
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            
            # If the pause menu is active, stop game logic and show the menu
            if self.pause_menu.menu_active:
                self.pause_menu.handle_input(events)   
                self.pause_menu.draw_menu()   
                pygame.display.update()
                continue  # Skip the rest of the game logic when paused
                
            self.handle_events(events)
            self.update()
            self.draw()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event, pressed=True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse(event, pressed=False)

    def handle_input(self, event):
        # Return to main menu
        if event.key in (pygame.K_BACKSPACE, pygame.K_RETURN):
            self.game.playing = False
            self.game.curr_menu = self.game.main_menu
            self.running = False
            return
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                    self.game.playing = False
                    self.game.curr_menu = self.game.main_menu
                    self.running = False
                if event.key == pygame.K_ESCAPE:  # Toggle pause menu
                    self.pause_menu.toggle_menu()
                if (event.key == pygame.K_1 or event.key == pygame.K_KP_1) and len(self.running_cards) < 3:
                    card = self.common_cards[0]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP_2) and len(self.running_cards) < 3:
                    card = self.common_cards[1]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_3 or event.key == pygame.K_KP_3) and len(self.running_cards) < 3:
                    card = self.common_cards[2]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_4 or event.key == pygame.K_KP_4) and len(self.running_cards) < 3:
                    card = self.common_cards[3]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_5 or event.key == pygame.K_KP_5) and len(self.running_cards) < 3:
                    card = self.common_cards[4]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_6 or event.key == pygame.K_KP_6) and len(self.running_cards) < 3:
                    card = self.random_cards[0]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_7 or event.key == pygame.K_KP_7) and len(self.running_cards) < 3:
                    card = self.random_cards[1]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_8 or event.key == pygame.K_KP_8) and len(self.running_cards) < 3:
                    card = self.random_cards[2]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_9 or event.key == pygame.K_KP_9) and len(self.running_cards) < 3:
                    card = self.random_cards[3]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()
                elif (event.key == pygame.K_0 or event.key == pygame.K_KP_0) and len(self.running_cards) < 3:
                    card = self.random_cards[4]
                    self.running_cards.append(card)
                    self.card_display_times[card] = pygame.time.get_ticks()

        # Toggle pause menu
        if event.key == pygame.K_ESCAPE:
            self.pause_menu.toggle_menu()
            return


            # Clear running cards and display times
            self.running_cards.clear()
            self.card_display_times.clear()
            return

            

    def handle_mouse(self, event, pressed):
        # Handle left click (card selection)
        if pressed and event.button == 1 and len(self.running_cards) < 3:
            # Try to select current card from deck
            if self.current_card_id:
                rect = self.card_rects[self.current_card_id]
                if rect.collidepoint(event.pos):
                    self.running_cards.append(self.current_card_id)
                    self.card_display_times[self.current_card_id] = pygame.time.get_ticks()
                    if len(self.carddeck.shuffled_deck) == 0:
                        self.carddeck.reset_deck()
                    self.load_next_card()
                    return

            # Try to select card from hand
            for card_id in self.common_cards + self.random_cards:
                if card_id in self.card_rects and self.card_rects[card_id].collidepoint(event.pos):
                    if card_id not in self.running_cards:
                        self.running_cards.append(card_id)
                        self.card_display_times[card_id] = pygame.time.get_ticks()
                        break

        # Handle right click (card info display)
        elif event.button == 3:
            if pressed:
                for card_id, rect in self.card_rects.items():
                    if rect.collidepoint(event.pos):
                        self.display_cardinfo = card_id
                        break
            else:
                self.display_cardinfo = None

    def update(self):
        if not self.current_card_id:
            if len(self.carddeck.shuffled_deck) == 0:
                self.carddeck.reset_deck()
            self.load_next_card()

    def draw(self):
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
            self.screen.blit(self.card_images[self.current_card_id], 
                            self.card_rects[self.current_card_id])

        # Draw card being dragged last so it appears on top
        if self.moving and self.selected_card_id is not None:
            self.screen.blit(self.card_images[self.selected_card_id], 
                            self.card_rects[self.selected_card_id])

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
        pygame.display.update()
            
    def addcommon_cards(self):
        # Get all common movement cards from the deck
        common_movement_cards = []
        
        # First, find all common movement cards in the deck
        for card_id, card_data in self.carddeck.deck.items():
            if card_data[3] == "common" and "Move" in card_data[1]:
                common_movement_cards.append(card_id)
        
        # Also add the Kick card
        for card_id, card_data in self.carddeck.deck.items():
            if card_data[1] == "Kick":
                common_movement_cards.append(card_id)
                break
        
        # Randomly select 5 cards if we have more than 5
        if len(common_movement_cards) > 5:
            common_movement_cards = random.sample(common_movement_cards, 5)
        
        # Process the selected cards
        for card_id in common_movement_cards:
            # Load base card image
            image_path = self.carddeck.get_card_img(card_id)
            base_card = pygame.image.load(image_path).convert_alpha()
            
            # Create a copy to draw on
            card_with_text = base_card.copy()
            
            # Get card name
            card_name = self.carddeck.get_card_name(card_id)
            
            # Render card name
            font = pygame.font.Font(self.fontpath, 15)
            self.draw_text_on_card(card_with_text, card_name, font, (255, 255, 255))
            
            self.card_images[card_id] = card_with_text
            self.common_cards.append(card_id)
        
        # Remove these cards from the shuffled deck
        for card_id in self.common_cards:
            if card_id in self.carddeck.shuffled_deck:
                self.carddeck.shuffled_deck.remove(card_id)
                
    def fill_random_cards(self):
         # Only fill up to 5 random cards
        while len(self.random_cards) < 5:
            # Check if deck needs reset
            if len(self.carddeck.shuffled_deck) == 0:
                self.carddeck.reset_deck()
        
            newcard_id = self.carddeck.get_next_card()
            if newcard_id:
                image_path = self.carddeck.get_card_img(newcard_id)
                
                # Load base card image
                base_card = pygame.image.load(image_path).convert_alpha()
                card_with_text = base_card.copy()
                
                # Get and render card name
                card_name = self.carddeck.get_card_name(newcard_id)
                font = pygame.font.Font(self.fontpath, 15)
                self.draw_text_on_card(card_with_text, card_name, font, (255, 255, 255))
                
                self.card_images[newcard_id] = card_with_text
                self.random_cards.append(newcard_id)
                # Break if we hit 5 cards
                if len(self.random_cards) >= 5:
                    break            
    def load_next_card(self):
        # Check if deck needs reset
        if len(self.carddeck.shuffled_deck) == 0:
            self.carddeck.reset_deck()
        
        # Get the next card
        self.current_card_id = self.carddeck.get_next_card()
        
        # Load card image
        image_path = self.carddeck.get_card_img(self.current_card_id)
        base_card = pygame.image.load(image_path).convert_alpha()
        card_with_text = base_card.copy()
        
        # Get card name and render it
        card_name = self.carddeck.get_card_name(self.current_card_id)
        font = pygame.font.Font(self.fontpath, 15)
        self.draw_text_on_card(card_with_text, card_name, font, (255, 255, 255))
        
        # Store the card image
        self.card_images[self.current_card_id] = card_with_text
        
        # Position card within the deck area
        self.card_width, self.card_height = self.card_images[self.current_card_id].get_size()
        self.card_x = int(self.DISPLAY_W * 0.86)
        self.card_y = int(self.DISPLAY_H * 0.825)
        self.card_x = min(self.card_x, self.DISPLAY_W - self.card_width)
        self.card_y = min(self.card_y, self.DISPLAY_H - self.card_height)
        
        # Create the rect for the card
        self.card_rects[self.current_card_id] = self.card_images[self.current_card_id].get_rect(topleft=(self.card_x, self.card_y))
            
    def wrap_text_to_card(self, text, font, max_width): # text wrapping for the text inside the card
        words = text.split(' ')
        lines = []
        current_line = words[0]
        
        for word in words[1:]:
            test_line = current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)
        return lines

    def draw_text_on_card(self, card_surface, text, font, color): # draw text on the card
        max_width = int(card_surface.get_width() * 0.60)  # 70% of card width
        lines = self.wrap_text_to_card(text, font, max_width)
        
        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        y = 20  # Starting y position
        
        for line in lines:
            text_surface = font.render(line, True, color)
            x = (card_surface.get_width() - text_surface.get_width()) // 2
            card_surface.blit(text_surface, (x, y))
            y += line_height
        
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
        description_text = font.render(card_description, True, (255, 255, 255))
        
        # Get text dimensions
        text_width = description_text.get_width()
        text_height = description_text.get_height()
        
        # Add padding to box dimensions
        box_width = text_width + 20  # 10px padding on each side
        box_height = text_height + 30  # 10px padding on top and bottom
        
        # Calculate positions
        info_x = rect.x
        info_y = rect.top - 80
        
        # Draw box and text
        pygame.draw.rect(self.screen, (0, 0, 0), (info_x, info_y, box_width, box_height))
        self.screen.blit(description_text, (info_x + 10, info_y + 20))
    
    def reset(self):
        self.game_ended = False
        self.stage_initialized = False
        # Set up deck again
        self.carddeck = Deck(self)
        self.current_card_id = None 
        self.common_cards = []
        self.random_cards = []
        self.addcommon_cards()
        self.first_spacebarpress = True
        self.load_next_card()
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
        card_spacing = width / 12  # Divide by 6 to leave some margin
        
        all_cards = self.common_cards + self.random_cards

        # Draw all cards
        for i, card_id in enumerate(all_cards):
            if card_id in self.card_images:
                # Calculate card position
                card_width, card_height = self.card_images[card_id].get_size()
                card_x = x + (i + 0.5) * card_spacing - card_width/2
                card_y = y + height/2 - card_height/2
                # Store the position for collision detection
                self.card_positions[card_id] = (card_x, card_y)
                
                # Draw the card if it's not being dragged and it exists
                if not (self.moving and self.selected_card_id == card_id):
                    self.card_rects[card_id] = self.card_images[card_id].get_rect(topleft=(card_x, card_y))
                    self.screen.blit(self.card_images[card_id], (card_x, card_y))
                
                #Update card rect
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
    # draw the stage area 
        width = self.DISPLAY_W * 0.8 # 80 percent of the display's width
        height = self.DISPLAY_H * 0.625 # 62.5 percent of the displays height
        x = self.DISPLAY_W * 0.10 # 10 percent of the display's width
        y = self.DISPLAY_H * 0.11 # 11 percent of the display's height
        
        # Initialize surfaces if not already done
        if not self.stage_initialized:
            self.stage_surface = pygame.Surface((width, height)) # create the surface for the game stage
            self.stage_rect = pygame.Rect(x, y, width, height) # creates a rectangle that defines the stage boundaries
            self.main_game.set_screen(self.stage_surface, width, height)
            self.stage_initialized = True # true when the stage is initialized
        
        # Draw stage and process cards first
        self.screen.blit(self.stage_surface, (x, y))
        # Draw active cards before game loop
        if self.running_cards:
            fighter_pos = self.main_game.fighter_1.rect
            card_spacing = 100
            base_x = fighter_pos.centerx - (len(self.running_cards) * card_spacing) // 2
            
            for i, card_id in enumerate(self.running_cards):
                card_x = base_x + (i * card_spacing) + 100
                card_y = fighter_pos.top - self.card_height + 50
                self.card_positions[card_id] = (card_x, card_y)
                if card_id in self.card_images:
                    self.screen.blit(self.card_images[card_id], (card_x, card_y))
        keys = pygame.key.get_pressed()
        self.fill_random_cards()
        
        # Handle spacebar after cards are drawn
        if keys[pygame.K_SPACE]:
            if self.first_spacebarpress:
                if len(self.carddeck.shuffled_deck) < 5:
                    self.carddeck.reset_deck()
                self.first_spacebarpress = False
            else:
                used_random_cards = []
                if len(self.running_cards) > 0:  # Only proceed if we have cards to process
                    combo_id = check_combo_l(self.running_cards)
                    if combo_id in self.carddeck.combos.keys():
                        print(f"Executing combo: {combo_id}")  # Debug print
                        self.main_game.fighter_1.play_combo_card(combo_id, self.carddeck, self.main_game.fighter_2)
                    elif len(self.running_cards) == 1:
                        print(f"Executing single card: {self.running_cards[0]}")  # Debug print
                        self.main_game.fighter_1.play_normal_card(self.running_cards[0], self.carddeck, self.main_game.fighter_2)
                
                for card_id in self.running_cards:
                    if card_id in self.random_cards:
                        used_random_cards.append(card_id)
                
                for card_id in used_random_cards:
                    if card_id in self.random_cards:
                        self.random_cards.remove(card_id)
                        
                # Only replace up to remaining space until 5 cards
                remaining_slots = max(0, 5 - len(self.random_cards))
                cards_to_replace = min(len(used_random_cards), remaining_slots)
                
                if cards_to_replace > 0:
                    existing_card_names = {self.carddeck.get_card_name(card_id) for card_id in self.random_cards}
                    
                    for _ in range(cards_to_replace):
                        attempts = 0
                        while attempts < 20:
                            if len(self.carddeck.shuffled_deck) == 0:
                                self.carddeck.reset_deck()
                                
                            new_card_id = self.carddeck.get_next_card()
                            card_name = self.carddeck.get_card_name(new_card_id)
                            
                            if card_name not in existing_card_names:
                                image_path = self.carddeck.get_card_img(new_card_id)
                                base_card = pygame.image.load(image_path).convert_alpha()
                                card_with_text = base_card.copy()
                                font = pygame.font.Font(self.fontpath, 15)
                                self.draw_text_on_card(card_with_text, card_name, font, (255, 255, 255))
                                self.card_images[new_card_id] = card_with_text
                                self.random_cards.append(new_card_id)
                                existing_card_names.add(card_name)
                                break
                            else:
                                self.carddeck.shuffled_deck.append(new_card_id)
                                random.shuffle(self.carddeck.shuffled_deck)
                            
                            attempts += 1
                        
            self.running_cards.clear()
            self.card_display_times.clear()
            self.card_positions.clear()
        
        # Update game state last
        self.main_game.game_loop()
        
        if not self.game_ended:  # Only check if game hasn't ended yet
            if self.main_game.fighter_2.health <= 0 or self.main_game.fighter_1.health <= 0:
                self.game_ended = True
                self.winlose.trigger_gameover(self.main_game.fighter_2.health, self.main_game.fighter_1.health)

class PauseMenu: # class for the pause menu
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.game = self.gameworld.game
        #self.mainmenu = self.game.main_menu
        cwd = os.getcwd()
        self.fontpath = (os.path.join(cwd, 'Commodore Pixelized v1.2.ttf'))
        self.font = pygame.font.Font(self.fontpath, 40)
        self.menu_options = ["Resume", "Restart", "Options", "Main Menu", "Quit"]
        self.options_menu_options = ["Music coming soon!", "Back"]
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
        self.click_cooldown = 200 # Milliseconds between mouse clicks
        self.toggle_cooldown = 200  # Milliseconds between menu toggles

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
                cursor_rect = cursor_surface.get_rect(right=text_rect.left - 10, centery=text_rect.centery)
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
            if self.selected_option == 0: # Music toggle
                if current_time - self.last_click_time >= self.click_cooldown:
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
                
                
class WinLose:
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.game = self.gameworld.game
        self.screen = self.gameworld.screen
        self.DISPLAY_W = self.gameworld.DISPLAY_W
        self.DISPLAY_H = self.gameworld.DISPLAY_H
        
        # Load images
        cwd = os.getcwd()
        chicken_path = os.path.join(cwd, "chiken_death.png")
        chickfila_path = os.path.join(cwd, "chick fil a.png")
        kfc_path = os.path.join(cwd, "kfc.png")
        costco_path = os.path.join(cwd, "chicken bake.png")
        
        # Load and scale images
        self.images = {
            'chicken': self.load_scale_image(chicken_path),
            'chickfila': self.load_scale_image(chickfila_path),
            'kfc': self.load_scale_image(kfc_path),
            'costco': self.load_scale_image(costco_path)
        }
        
        # Define end screen variations
        self.win_screens = [
            {
                'image': 'chickfila',
                'main_text': "YOU COOKED!",
                'sub_text': '"Only open on sundays"'
            },
            {
                'image': 'kfc',
                'main_text': "YOU COOKED!",
                'sub_text': '"So, you telling me a shrimp fried this chicken?"'
            },
            {
                'image': 'costco',
                'main_text': "YOU COOKED!",
                'sub_text': '"Price of the chicken bake from costco"'
            }
        ]
        
        self.lose_screens = [
            {
                'image': 'chickfila',
                'main_text': "YOU GOT COOKED!",
                'sub_text': '"Only open on sundays"'
            },
            {
                'image': 'kfc',
                'main_text': "YOU GOT COOKED!",
                'sub_text': '"So you tellin me, a shrimp fried this chicken?"'
            },
            {
                'image': 'costco',
                'main_text': "YOU GOT COOKED!",
                'sub_text': '"Price of the chicken bake from Costco"'
            }
        ]
        
        # Create buttons
        btn_w, btn_h = 300, 75
        btn_x = (self.DISPLAY_W - btn_w) // 2
        self.restart_btn = pygame.Rect(btn_x, self.DISPLAY_H//2 + 50, btn_w, btn_h)
        self.menu_btn = pygame.Rect(btn_x, self.DISPLAY_H//2 + 130, btn_w, btn_h)
        self.quit_btn = pygame.Rect(btn_x, self.DISPLAY_H//2 + 210, btn_w, btn_h)
        
        # Track game over state
        self.show_gameover = False

    def load_scale_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (self.DISPLAY_W, self.DISPLAY_H))

    def trigger_gameover(self, cpu_health, fighter_health):
        if cpu_health <= 0:
            self.show_gameover = True
            self.show_end_screen(True)
            self.game.playing = False
            return True
        elif fighter_health <= 0:
            self.show_gameover = True
            self.show_end_screen(False)
            self.game.playing = False
            return True
        return False

    def show_end_screen(self, is_victory):
        # Select random screen content
        screen_content = random.choice(self.win_screens if is_victory else self.lose_screens)
        
        # Draw background
        self.screen.fill((0, 205, 255))
        
        # Calculate vertical spacing
        title_y = self.DISPLAY_H * 0.15  # Title at 15% from top
        image_y = self.DISPLAY_H * 0.3   # Image at 30% from top
        quote_y = self.DISPLAY_H * 0.7   # Quote at 70% from top
        
        # Draw overlay first
        overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        
        # Draw main text at top
        main_text = self.gameworld.font.render(screen_content['main_text'], True, (255, 255, 255))
        main_text_rect = main_text.get_rect(center=(self.DISPLAY_W//2, title_y))
        self.screen.blit(main_text, main_text_rect)
        
        # Draw image in middle (scaled to fit between text and quote)
        if self.images[screen_content['image']]:
            image = self.images[screen_content['image']]
            # Scale image to fit in middle section while maintaining aspect ratio
            image_height = quote_y - image_y - 20  # Leave some padding
            image_width = image_height * (image.get_width() / image.get_height())
            scaled_image = pygame.transform.scale(image, (int(image_width), int(image_height)))
            image_rect = scaled_image.get_rect(center=(self.DISPLAY_W//2, image_y + image_height//2))
            self.screen.blit(scaled_image, image_rect)
        
        # Draw quote below image
        sub_font = pygame.font.Font(self.gameworld.fontpath, 30)
        sub_text = sub_font.render(screen_content['sub_text'], True, (255, 255, 255))
        sub_text_rect = sub_text.get_rect(center=(self.DISPLAY_W//2, quote_y))
        self.screen.blit(sub_text, sub_text_rect)
        
        # Update button positions to be below quote
        btn_w, btn_h = 300, 75
        btn_x = (self.DISPLAY_W - btn_w) // 2
        self.restart_btn = pygame.Rect(btn_x, quote_y + 80, btn_w, btn_h)
        self.menu_btn = pygame.Rect(btn_x, quote_y + 160, btn_w, btn_h)
        self.quit_btn = pygame.Rect(btn_x, quote_y + 240, btn_w, btn_h)
        
        self.button_input()

    def clear_gameover(self):
        self.show_gameover = False
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.event.clear()

    def button_input(self):
        while self.show_gameover:
            mouse = pygame.mouse.get_pos()
            
            # Draw buttons
            for btn, text in [(self.restart_btn, "Restart"), (self.menu_btn, "Main Menu"), (self.quit_btn, "Quit Game")]:
                color = (70, 70, 70) if btn.collidepoint(mouse) else (50, 50, 50)
                pygame.draw.rect(self.screen, color, btn)
                pygame.draw.rect(self.screen, (255, 255, 255), btn, 2)
                
                txt_surf = self.gameworld.font.render(text, True, (255, 255, 255))
                self.screen.blit(txt_surf, txt_surf.get_rect(center=btn.center))
            
            pygame.display.update()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.clear_gameover()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                        self.game.playing = False
                        self.game.curr_menu = self.game.main_menu
                        self.running = False
                    if event.key == pygame.K_ESCAPE:  # Toggle pause menu
                        self.pause_menu.toggle_menu()
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_btn.collidepoint(mouse):
                        self.clear_gameover()
                        self.game.playing = True
                        self.gameworld.reset()
                        return
                    if self.menu_btn.collidepoint(mouse):
                        self.clear_gameover()
                        self.gameworld.reset() 
                        self.game.playing = False
                        self.gameworld.running = False
                        self.game.curr_menu = self.game.main_menu
                        self.game.curr_menu.run_display = True
                        return
                    if self.quit_btn.collidepoint(mouse):
                        pygame.quit()
                        sys.exit()
                        return
