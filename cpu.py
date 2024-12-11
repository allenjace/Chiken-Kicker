import pygame
from deck import *
import math
import random
from fighter import *

SCREEN_WIDTH = SCREENHEIGHT = 0
GRAVITY =2
SPEED = 10

class CPU():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, width, height):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect((x, y, 120, 180))
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0: idle 1: run 2: jump 3: attack1 4:attack2 5: hit 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.health = 100
        self.previous_health = 100  # Add this to track health changes
        self.attack_cool = 0
        self.attack_type = 0
        self.health_thresholds = [90, 60, 30]  # Health points where cards should appear
        SCREEN_WIDTH = width
        SCREENHEIGHT = height
        
        self.hits = 0  # hit counter
        self.display_card = None  # Store the currently displayed card
        self.card_display_time = 0  # Timer for how long to show the card
        self.deck = Deck(None)  # Create deck instance

    def load_images(self, sprite_sheet, animation_steps):
        # extract images
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0 , 0), self.rect) # this is the hitbox
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        
        # Draw card if one is being displayed
        if self.display_card and self.card_display_time > 0:
            # Load and scale the card image
            card_img = pygame.image.load(self.display_card[4])  # Get image path from card data
            card_img = pygame.transform.scale(card_img, (100, 100))  # Scale card to reasonable size
            
            # Position card above CPU's head
            card_x = self.rect.centerx - 30  # Center card horizontally
            card_y = self.rect.top - 100  # Position above head
            
            surface.blit(card_img, (card_x, card_y))
            
            # Update card display timer
            self.card_display_time -= 1
            if self.card_display_time <= 0:
                self.display_card = None

    def update_mvmt(self, screen_width,screen_height,target,surface):
        if not self.rect.colliderect(target.rect):
            dx = dy = 0
            dx, temp = target.rect.x - self.rect.x, target.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            
            if dist != 0: # if distance is not zero because float division by zero error
                dx = dx / dist  # Normalize.
                self.rect.x += dx * SPEED
            
            # Check if player is jumping and respond with 30% chance
            if self.rect.bottom >= screen_height - 10:  # Only jump if on ground
                if target.jump and random.random() <= 0.30:  # 30% chance to mirror player jump
                    self.vel_y = -30
                    self.jump = True   

            
            self.vel_y += GRAVITY
            dy += self.vel_y
        
            # asure player stays on screen
            # player won't go past the screen display
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 10: # defining the ground
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 10 - self.rect.bottom

            # ensure players face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else: 
                self.flip = True
            if self.attack_cool == 0:
                self.counter_attack(surface, target)
            elif self.attack_cool > 0:
                self.attack_cool -= 1
                
            # update cpu position
            self.rect.x += dx
            self.rect.y += dy
            
        # else:
        #     # attack
        #     self.rect.y += GRAVITY
        #     pass

    def update(self):
        # check what action player is performing
        if self.attacking == True:
            if self.attack_type == 1:
                self.update_action(4) # 3: attack1
            elif self.attack_type == 2:
                self.update_action(5) # 4: attack2    
        elif self.jump == True:
            self.update_action(2) # 2: jump
        elif self.running == True:
            self.update_action(1) # 1: run
        else:
            self.update_action(0) # 0: idle
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update 
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            # check if an attack was executed
            if self.action == 3 or self.action == 4:
                self.attacking = False
                self.attack_cool = 20
            if self.action == 5:
                self.hit = False
                self.attacking = False
                
    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    def counter_attack(self, surface, target):
        if not self.attacking and self.attack_cool == 0:
            self.attacking = True
            self.attack_type = random.choice([1, 2])  # Randomly choose attack type
            self.attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if self.attacking_rect.colliderect(target.rect):
                target.health -= 10
            
            pygame.draw.rect(surface, (255, 0, 0), self.attacking_rect)  # Red color for CPU attack
            self.attack_cool = 45
            
    def take_hits(self): # cpu takes 3 hits
         # Check if we've crossed any health thresholds
        current_health = self.health
        
        # If health decreased
        if current_health < self.previous_health:
            # Check each 30-health interval
            for threshold in [90, 60, 30]:
                # If we crossed this threshold in this hit
                if current_health == threshold:
                        bucket_choice = random.randrange(1, 100)
                        if bucket_choice:
                            self.display_card = self.deck.draw_card(1, 18)
                            self.card_display_time = 60
                
   
    
