import pygame
from deck import *
import math

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
        self.attack_cool = 0
        self.attack_type = 0
        self.health = 100
        SCREEN_WIDTH = width
        SCREENHEIGHT = height

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
        # pygame.draw.rect(surface, (255, 0 , 0), self.rect) # this is the hitbox
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update_mvmt(self, screen_width,screen_height,target):
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

            # Move along this normalized vector towards the player at current speed.
            #if temp > 0 and self.jump ==False:
                #self.jump = True
                #self.vel_y -= 30
            
            self.vel_y += GRAVITY
            dy = self.vel_y
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

            if self.attack_cool > 0:
                self.attack_cool -= 1
            self.rect.y += dy
        # else:
        #     # attack
        #     self.rect.y += GRAVITY
        #     pass

    def update(self):
        # check what action player is performing
        if self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) # 3: attack1
            elif self.attack_type == 2:
                self.update_action(4) # 4: attack2    
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
