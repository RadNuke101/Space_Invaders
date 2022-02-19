#############################################################################################################
#                                              --SPACE_INVADER --                                           #
 
#                                             Author: Pranav Putta                                          #
 
#                                 Description: Defend your planet from the invaders!                        #
 
#                                                                                                           #
 
#                                                                                                           #
 
#                                                                                                           #
 
#                                                                                                           #
#############################################################################################################

#Inspired by: https://github.com/mindninjaX/Space-Invaders-PyGame.git

import math
import random
import pygame

# Intialize pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background_img= pygame.image.load("Images/background.jpg")
background = pygame.transform.scale(background_img, (800, 600))


# Caption
pygame.display.set_caption("Space Invader")

# Player
playerImg_test = pygame.image.load('Images//defender.png')
playerImg = pygame.transform.scale(playerImg_test, (100,100))

playerX = 350
playerY = 490
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 5

for i in range(enemies_num):
    enemyImg.append(pygame.image.load('Images//enemy.png'))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('Images//bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "READY"

# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 70)


def score(x, y):
    score = font.render("SCORE : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "FIRE"
    screen.blit(bulletImg, (x + 5, y + 2))


def Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -2
            if event.key == pygame.K_d:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "READY":
                    # Location of ship
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

    # Enemy Movement
    for i in range(enemies_num):

        # Game Over
        if enemyY[i] > 440:
            for j in range(enemies_num):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "READY"
            score_val += 1
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "READY"

    if bullet_state is "FIRE":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score(textX, testY)
    pygame.display.update()
