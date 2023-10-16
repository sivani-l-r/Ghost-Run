import pygame
import sys


def display_score():
    global time
    time = int(pygame.time.get_ticks() / 1000) - START_TIME
    time_surface = font1.render(f'{time}', False, RED)
    screen.blit(time_surface, (80, 0))
    return time

def player_animation():
    global cutie,cutie_index
    if cutie_rect.bottom < SCREEN_HEIGHT - 20:
        cutie = cutie_jump
    else:
        cutie_index += 0.1
        if cutie_index >=len(cutie_walk): cutie_index = 0

        cutie = cutie_walk[int(cutie_index)]



# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GRAVITY_STRENGTH = 1
JUMP_HEIGHT = 20
CUTIE_SIZE = (100, 100)
GHOST_SIZE = (120, 120)
CUTIE_COLLISION_SIZE = (15, 15)
CUTIE_COLLISION_OFFSET = (5, 5)
START_TIME = 0

# Colors
DARK_BLUE = (69, 25, 82)
BROWN = (102, 37, 73)
RED = '#D80032'
DARK_ORANGE = (243, 159, 90)
WHITE = '#F8F0E5'

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ghost Run')
clock = pygame.time.Clock()

# Load Resources
bg_surface = pygame.image.load('landscape/bg.png').convert_alpha()
land_surface = pygame.image.load('landscape/land.png').convert_alpha()
cutie_1 = pygame.transform.scale(pygame.image.load('players/cutie/cutie - 2.gif').convert_alpha(), CUTIE_SIZE)
cutie_2 = pygame.transform.scale(pygame.image.load('players/cutie/cutie - 6.gif').convert_alpha(), CUTIE_SIZE)
cutie_jump = pygame.transform.scale(pygame.image.load('players/cutie/cutie - 1.gif').convert_alpha(), CUTIE_SIZE)

cutie_walk = [cutie_1, cutie_2]
cutie_index = 0
cutie = cutie_walk[cutie_index]

ghost = pygame.transform.scale(pygame.image.load('players/ghost.png').convert_alpha(), GHOST_SIZE)

# Fonts
font1 = pygame.font.Font('font/Spookyman.otf', 30)
font2 = pygame.font.Font('font/SpookyMagic.ttf', 60)
score_surface = font1.render('Score', True, DARK_ORANGE)
gameover_surface = font2.render('GAME OVER', True, DARK_ORANGE)
gamestart_surface = font1.render('Press Space to restart', True, WHITE)

# Initialize Game Variables
cutie_rect = cutie.get_rect(midbottom=(50, SCREEN_HEIGHT - 20))
ghost_rect = ghost.get_rect(midbottom=(SCREEN_WIDTH, SCREEN_HEIGHT - 40))
cutie_collision_rect = pygame.Rect(
    cutie_rect.centerx - CUTIE_COLLISION_SIZE[0] // 2 + CUTIE_COLLISION_OFFSET[0],
    cutie_rect.centery - CUTIE_COLLISION_SIZE[1] // 2 + CUTIE_COLLISION_OFFSET[1],
    CUTIE_COLLISION_SIZE[0],
    CUTIE_COLLISION_SIZE[1]
)
player_gravity = 0
is_jumping = False
collision_detected = False

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if collision_detected == False:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                if cutie_rect.bottom == SCREEN_HEIGHT - 20 and not is_jumping:
                    is_jumping = True
                    player_gravity = -JUMP_HEIGHT
        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                collision_detected = False
                ghost_rect.left = 800

    if collision_detected == False:

        # Surface
        screen.blit(bg_surface, (0, 0))
        screen.blit(land_surface, (0, 50))
        screen.blit(land_surface, (500, 50))

        # Font
        screen.blit(score_surface, (0, 0))
        score = display_score()

        ghost_rect.left -= 5
        if ghost_rect.right <= 0:
            ghost_rect.left = SCREEN_WIDTH

        if is_jumping:
            cutie_rect.y += player_gravity
            player_gravity += GRAVITY_STRENGTH

            if cutie_rect.bottom >= SCREEN_HEIGHT - 20:
                cutie_rect.bottom = SCREEN_HEIGHT - 20
                is_jumping = False
                player_gravity = 0

        cutie_collision_rect.topleft = (
            cutie_rect.left + CUTIE_COLLISION_OFFSET[0],
            cutie_rect.top + CUTIE_COLLISION_OFFSET[1]
        )
        player_animation()
        screen.blit(ghost, ghost_rect)
        screen.blit(cutie, cutie_rect)

        if cutie_collision_rect.colliderect(ghost_rect):
            if not collision_detected:
                collision_detected = True

    else:
        screen.blit(bg_surface, (0, 0))
        screen.blit(gameover_surface, (200, 150))
        screen.blit(gamestart_surface, (250, 250))

        finalscore_surface = font1.render(f'Your Score  {score}', False, RED)
        screen.blit(finalscore_surface, (0, 0))
        START_TIME = int(pygame.time.get_ticks() / 1000)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
