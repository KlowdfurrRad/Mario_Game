import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mario Level')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Load images
mario_img = pygame.image.load('mario.png')
block_img = pygame.image.load('block.png')
flag_img = pygame.image.load('flag.png')

# Get flag dimensions
flag_width, flag_height = flag_img.get_size()

# Player settings
player_width = 40
player_height = 60
player_x = 50
player_y = screen_height - player_height - 10
player_speed = 5
player_jump = False
jump_height = 15
gravity = 0.8
player_velocity_y = 0

# Level design (a simple array of blocks)
level = [
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                                                                                    #####                                              ',
    '                                                                                               #######                                                 ',
    '                                                                                          ###########                                                  ',
    '                                                                                                                                                       ',
    '                                                                                                                                                       ',
    '                                           #####                                    #####                                                              ',
    '                                                ##     ##                     #############                                                            ',
    '                                                                                         ###                                                           ',
    '##         ##          #####                       ##          ##    #############                   ########                                          ',
    '                                                                                 ##                                                                    ',
    '                                    ##               ######                                                                                            ',
    '#############################      ######   #########################################################                                                  ',
    '                                                                                                                                         ######         ',
    '                                                                                                                                                       ',
]

# Create block positions based on level design
block_list = []
breakable_blocks = ['@']  # Define characters for breakable blocks
for y, row in enumerate(level):
    for x, block in enumerate(row):
        if block == '#':  # Regular block
            block_rect = pygame.Rect(x * 40, y * 40, 40, 40)
            block_list.append(block_rect)
        elif block in breakable_blocks:  # Breakable block
            block_rect = pygame.Rect(x * 40, y * 40, 40, 40)
            block_list.append(block_rect)

# Flag position
flag_x = len(level[0]) * 40 - 100
flag_y = screen_height - flag_height - 10
flag_rect = pygame.Rect(flag_x, flag_y, flag_width, flag_height)

# Function to handle player collision with blocks
def handle_collision(rect, dx, dy):
    global block_list
    for block in block_list[:]:  # Iterate over a copy to modify original list
        if rect.colliderect(block):
            if dx > 0:  # Moving right
                rect.right = block.left
            if dx < 0:  # Moving left
                rect.left = block.right
            if dy > 0:  # Moving down
                rect.bottom = block.top
                return True
            if dy < 0:  # Moving up
                rect.top = block.bottom
            # Check collision from below to break block
            if dy > 0 and rect.bottom > block.top and rect.bottom - dy < block.top:
                block_list.remove(block)
                return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()
camera_x = 0
win = False
space_pressed = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -player_speed
    if keys[pygame.K_RIGHT]:
        dx = player_speed
    if keys[pygame.K_SPACE] and not player_jump and not space_pressed:
        player_velocity_y = -jump_height
        player_jump = True
        space_pressed = True
    if not keys[pygame.K_SPACE]:
        space_pressed = False

    # Apply gravity
    player_velocity_y += gravity
    if player_velocity_y > 10:  # Terminal velocity
        player_velocity_y = 10

    # Calculate new position
    player_x += dx
    player_y += player_velocity_y

    # Create a rectangle for the player
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Handle collisions
    if handle_collision(player_rect, dx, 0):
        player_x = player_rect.x
    if handle_collision(player_rect, 0, player_velocity_y):
        player_y = player_rect.y
        player_velocity_y = 0
        player_jump = False

    # Check if player is on the ground
    if player_y > screen_height - player_height:
        player_y = screen_height - player_height
        player_velocity_y = 0
        player_jump = False

    # Scroll the screen
    if player_x > screen_width / 2:
        camera_x = player_x - screen_width / 2

    # Check for win condition
    if player_rect.colliderect(flag_rect):
        win = True
        running = False

    # Drawing code
    screen.fill(blue)
    screen.blit(mario_img, (player_x - camera_x, player_y))
    for block in block_list:
        screen.blit(block_img, (block.x - camera_x, block.y))
    screen.blit(flag_img, (flag_x - camera_x, flag_y))

    # Refresh the screen
    pygame.display.flip()
    clock.tick(60)

# Win message
if win:
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", 1, white)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

pygame.quit()
sys.exit()
