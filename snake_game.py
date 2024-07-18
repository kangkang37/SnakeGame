import os.path
import os
import pygame
import random

# initialize the game
pygame.init()

pygame.mixer.init()

# load music if exists
music_path = './snakeMusic.mp3'
# music_path = './your_music_path.mp3'
bgm = False # whether to play the background music
if os.path.exists(music_path):
    bgm = True
    pygame.mixer.music.load(music_path)


# set the screem size
screen = pygame.display.set_mode((640, 640))

# set the game clock
clock = pygame.time.Clock()

# set the initial direction
direction = 'RIGHT'
change_to = direction

# set the color
snake_color = (0,255,0) # green
food_color = (255,0,0) # red
background_color = (0,0,0) # black
text_color = (255, 255, 255) # white

font = pygame.font.Font(None, 36)

# set "restart" and "exit" button and position
restart_button = pygame.Rect(260, 400, 120, 50)
exit_button = pygame.Rect(260, 500, 120, 50)
start_button = pygame.Rect(260, 300, 120, 50)

# initial score
score = 0

def show_score():
    score_text = font.render(f'Score: {score}', True, text_color)
    screen.blit(score_text, (0, 0))

def game_over():
    global score,direction
    
    # Set the text to be displayed
    text = font.render('Game Over', True, text_color)
    # Set the display position
    screen.blit(text, (250, 300))

    # Draw the "restart" button
    pygame.draw.rect(screen, text_color, restart_button, 2)
    text = font.render('restart', True, text_color)
    screen.blit(text, (restart_button.x + 22, restart_button.y + 14))

    # Draw the "exit" button
    pygame.draw.rect(screen, text_color, exit_button, 2)
    text = font.render('exit', True, text_color)
    screen.blit(text, (exit_button.x + 35, exit_button.y + 14))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                # Reset Direction
                direction = 'RIGHT'
                change_to = direction
                score=0
                return True
    return False



# Display the start interface and wait for the user to click the "start" button
def start_screen():
    screen.fill(background_color)

    text = font.render("Click 'start' to Begin!", True, text_color)
    screen.blit(text, (200, 200))

    pygame.draw.rect(screen, text_color, start_button, 2)
    text = font.render('start', True, text_color)
    screen.blit(text, (start_button.x + 32, start_button.y + 14))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                return

# Display the start screen
start_screen()

# Set the initial positions of the snake and food
snake_pos = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
food_spawn = True

# Play music when the game starts
if bgm:
    pygame.mixer.music.play(-1)


while True:
    # control direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    direction = change_to

    # update the snake position
    if direction == 'UP':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1]-10])
    if direction == 'DOWN':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1]+10])
    if direction == 'LEFT':
        snake_pos.insert(0, [snake_pos[0][0]-10, snake_pos[0][1]])
    if direction == 'RIGHT':
        snake_pos.insert(0, [snake_pos[0][0]+10, snake_pos[0][1]])

    # whether eat the food
    if snake_pos[0] == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_pos.pop()

    # Generate new food
    if not food_spawn:
        food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
    food_spawn = True

    # Refresh the screen
    screen.fill(background_color)
    for pos in snake_pos:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # show score
    show_score()

    # Determine whether you hit the wall or yourself
    if snake_pos[0][0] >= 640 or snake_pos[0][0] < 0 or snake_pos[0][1] >= 640 or snake_pos[0][1] < 0:
        if bgm: pygame.mixer.music.stop()
        if game_over():
            if bgm:
                pygame.mixer.music.play(-1)
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            direction = 'RIGHT'
            change_to=direction
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            if bgm: pygame.mixer.music.stop()
            if game_over():
                if bgm:
                    pygame.mixer.music.play(-1)
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                direction = 'RIGHT'
                change_to=direction

    pygame.display.update()
    # Slow down the snake's movement
    clock.tick(10)
