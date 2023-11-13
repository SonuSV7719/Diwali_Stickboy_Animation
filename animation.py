import pygame
import sys
import random
# Initialize Pygame
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Diwali Stickboy Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
previous_tick = 0
leg_open = True
move_x = 0
legs_movement_allowed = True  

# pygame image load
x_positions = [50, 130, 210, 290, 472, 472 + 80, 472 + 80 + 80, 472 + 80 + 80 + 80] 

diwali_text = pygame.image.load("diwali.png")
# new_width, new_height = 10, 50
# resized_image = pygame.transform.scale(diwali_text, (new_width, new_height))
diwali_rect = diwali_text.get_rect()
diwali_rect.topleft = (180, 0)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.gravity = 0.1
        self.life = 60

    def update(self):
        self.vel.y += self.gravity
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.life -= 1
        if self.life <= 0:
            self.kill()


def get_diya(x_position):
    diya = pygame.image.load("diya.png")
    new_width, new_height = 50, 50
    resized_image = pygame.transform.scale(diya, (new_width, new_height))
    diya_rect = resized_image.get_rect()
    diya_rect.topleft = (x_position, (height * 73) / 100)
    return resized_image, diya_rect


def road(screen, width, height):
    pygame.draw.line(screen, WHITE, (0, (height * 80)/100), (width, (height * 80)/100), 5)

def stickboy(screen, width, height, left_leg_x, right_leg_x, move_x):
    # Head
    pygame.draw.circle(screen, WHITE, (50+move_x, 300), 25)
    # Body
    pygame.draw.line(screen, WHITE, (50+move_x, 325), (50+move_x, 417), 2)
    
    if leg_open and legs_movement_allowed:
        # Legs Open
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (left_leg_x+move_x, 480), 2)  # left
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (right_leg_x+move_x, 480), 2)  # right
    else:
        # Legs Closed
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (47+move_x, 480), 2)  # left
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (53+move_x, 480), 2)  # right

    # Hand
    pygame.draw.line(screen, WHITE, (50+move_x, 350), (18+move_x, 390), 2)  # left
    pygame.draw.line(screen, WHITE, (50+move_x, 350), (82+move_x, 390), 2)  # right

def stickboy_hello_position(screen, width, height):
    # Head
    pygame.draw.circle(screen, WHITE, (50+move_x, 300), 25)
    # Body
    pygame.draw.line(screen, WHITE, (50+move_x, 325), (50+move_x, 417), 2)
    
    if leg_open and legs_movement_allowed:
        # Legs Open
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (25+move_x, 480), 2)  # left
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (75+move_x, 480), 2)  # right
    else:
        # Legs Closed
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (47+move_x, 480), 2)  # left
        pygame.draw.line(screen, WHITE, (50+move_x, 417), (53+move_x, 480), 2)  # right

    # Hand
    pygame.draw.line(screen, WHITE, (50+move_x, 350), (18+move_x, 390), 2)  # left
    pygame.draw.line(screen, WHITE, (50+move_x, 350), (82+move_x, 390), 2)  # right
    
    # hand_bottom
    pygame.draw.line(screen, WHITE, (18+move_x, 390), (18+move_x+20, 390), 2)  # left
    pygame.draw.line(screen, WHITE, (82+move_x, 390), (82+move_x-20, 390), 2)  # right
    
    # hand_closed 
    pygame.draw.line(screen, WHITE, (18+move_x+20, 390), (18+move_x+20+12, 375), 2)  # left
    pygame.draw.line(screen, WHITE, (82+move_x-20, 390), (82+move_x-20-12, 375), 2)  # right
    

all_sprites = pygame.sprite.Group()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y =pygame.mouse.get_pos()
            print(x,", ", y)

    # Draw
    screen.fill(BLACK)
    current_tick = pygame.time.get_ticks()

    if current_tick - previous_tick >= 500 and legs_movement_allowed:
        leg_open = not leg_open
        previous_tick = current_tick

    if move_x < width // 2 - 50:
        stickboy(screen, width, height, 25, 75, move_x)
        move_x += 0.6
    else:
        legs_movement_allowed = False
        stickboy_hello_position(screen, width, height)
        # screen.blit(resized_image, diya_rect)
        for i, x_position in enumerate(x_positions):
            diya_image, diya_rect = get_diya(x_position )
            screen.blit(diya_image, diya_rect)
            
        screen.blit(diwali_text, diwali_rect)
        
        particle = Particle(random.randint(0, width), random.randint(0, height))
        all_sprites.add(particle)
        # Update particles
        all_sprites.update()
        all_sprites.draw(screen)
        
        
    road(screen, width, height) 
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
