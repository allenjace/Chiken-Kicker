import pygame
from deck import *

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, hand):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = self.orig_rect = pygame.Rect((x, y, 80, 100))
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
        self.attack_type = 0
        self.health = 100
        self.playerhand = hand
        self.playerqueue = queue.Queue()

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

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get key presses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False:
            # movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
            # jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            # attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                # determine which attack type was used
                if key[pygame.K_r]: # defining if "r" is clicked
                    self.attack_type = 1 
                if key[pygame.K_t]: # defining if "t" is clicked
                    self.attack_type = 2

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # asure player stays on screen
        # player won't go past the screen display
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110: # defining the ground
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else: 
            self.flip = True

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates
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
    # hitbox 
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10 # fighter loses 10 health
        
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (0, 255 , 0), self.rect, 2)
        # surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def add_card(self, card):
        self.playerqueue.put(card)
        # print('placing and removing', card)
        if card[2] != 0:
            self.playerhand.remove(card)

    def card_move(self, mvmt, target):
        if self.flip:
            self.rect.x -= mvmt[0]
        else:
            self.rect.x += mvmt[0]
        self.rect.y += mvmt[1]

        if mvmt[2] != self.image_scale:
            if mvmt[2] < 1:
                self.rect.scale_by(mvmt[2])
                self.image_scale = mvmt[2]
            elif self.image_scale < 1 and mvmt[2] >= 1:
                self.rect.scale_by(1/self.image_scale)
                self.image_scale(mvmt[2])
                self.rect.scale_by(self.image_scale)
        
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else: 
            self.flip = True

    def detect_col(self, opp, move):
        if (self.rect.y + self.rect.h) > opp.rect.y and (opp.rect.y + opp.rect.h) > (self.rect.y + (self.rect.h/2)):
            if (opp.rect.x < self.rect.x + move[0]) and opp.rect.x > self.rect.x + self.rect.w:
                return True
        return False

    def create_hitbox(self, action):
        # creates a hitbox for the related move, will create on the side closest to 
        if self.flip:
            hitbox = pygame.Rect((self.rect.x - self.rect.w * action[5][0], self.rect.y + self.rect.h - self.rect.h * action[5][1],self.rect.w * action[5][0],self.rect.h * action[5][1]))
        else:
            hitbox = pygame.Rect((self.rect.x + self.rect.w, self.rect.y + self.rect.h - self.rect.h * action[5][1],self.rect.w * action[5][0],self.rect.h * action[5][1]))
        return hitbox
