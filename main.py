import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('retro-game-overworld-loop.wav')
mixer.music.play(-1)

# Caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

speed = 2

# Score
score_value = 0
font = pygame.font.Font('ARCADE_I.TTF', 32)

# Game over text
over_font = pygame.font.Font('ARCADE_I.TTF', 64)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Create a list of enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(20, 748))
    enemyY.append(random.randint(40, 180))
    enemyX_change.append(random.randint(8, 15)/10 * speed)
    enemyY_change.append(random.randint(20, 50) * speed)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = -5 * speed
bullet_state = "ready"

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, [255, 255, 255])
    screen.blit(score, [x, y])

def game_over_text():
    over_text = over_font.render("GAME OVER", True, [0, 255, 0])
    screen.blit(over_text, [200, 250])

def player(x, y):
    screen.blit(playerImg, [x, y])

def enemy(x, y, j):
    screen.blit(enemyImg[j], [x, y])

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, [x, y])

def is_collision(xe, ye, xb, yb):
    distance = math.sqrt(math.pow((xb-xe), 2) + math.pow((yb-ye), 2))
    if distance < 21:
        return True
    else:
        return False

def is_contact(xe, ye, xp, yp):
    distance = math.sqrt(math.pow((xp-xe), 2) + math.pow((yp-ye), 2))
    if distance < 21:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill([0, 0, 0])

    # Background image
    screen.blit(background, [0, 0])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Events
        if event.type == pygame.KEYDOWN:
            # Get the current location of the player and shoot
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # shot_Sound = mixer.Sound('laser-shot-silenced.wav')
                    # shot_Sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    print("Shoot")
            # If keystroke is pressed check whether it is right or left and move
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
            if event.key == pygame.K_UP:
                playerY_change = -speed
            if event.key == pygame.K_DOWN:
                playerY_change = speed
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update player's position
    playerX += playerX_change
    playerY += playerY_change

    # Checking boundaries for player's spaceship
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    if playerY < 0:
        playerY = 0
    elif playerY > 536:
        playerY = 536

    # Enemy's movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = -1 * enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 768:
            enemyX_change[i] = -1 * enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosion_sound = mixer.Sound('explosion12.wav')
            # explosion_sound.play()
            score_value += 1
            print("Collision detected. Score:", score_value)
            bullet_state = "ready"
            bulletY = 0
            bulletX = 0
            enemyX[i] = random.randint(20, 748)
            enemyY[i] = random.randint(40, 120)
        # Contact
        contact = is_contact(enemyX[i], enemyY[i], playerX, playerY)
        if contact:
            game_over_text()
            running = False

        enemy(enemyX[i], enemyY[i], i)

    # Bullet's movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    if bulletY <= 0:
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(10, 10)
    pygame.display.update()
