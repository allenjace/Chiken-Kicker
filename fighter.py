import pygame

class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))    # Where x,y are and given a width and height
        self.vel_y = 0                              # Starting velocity is 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 2
        GRAVITY = 1
        dx = 0
        dy = 0
        
        # Get Keypresses
        key = pygame.key.get_pressed()
        
        # Can only perform other actions if not currently attacking
        if self.attacking == False:
            # Movement
            if key[pygame.K_a]:     # Checking if key a is being pressed
                dx = -SPEED
            if key[pygame.K_d]:     # Checking if key d is being pressed
                dx = SPEED
            # Jump
            if key[pygame.K_w] and self.jump == False:     # Checking if key w is being pressed
                self.vel_y = -30
                self.jump = True
            # Attacks
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                
                # Determine which attack type was used
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2
        
        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
            
        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx =self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:     # Ensure player doesnt fall down
            self.vel_y = 0
            self.jump = False                               # Ensure player can jump again
            dy = screen_height - 110 - self.rect.bottom
        # Update player position
        self.rect.x += dx
        self.rect.y += dy
        
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            print("Hit")
        
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    def draw(self, surface):                        # Game player window
        pygame.draw.rect(surface, (255, 0, 0), self.rect)   # Color of player background rect