from posixpath import relpath
import pygame
import random
import decimal
import math
import time
import os

from pygame import mixer
abs_path = os.path.dirname(os.path.realpath('__file__'))
rel_path = "pygame_IA"
abs_path = os.path.join(abs_path, rel_path)
os.chdir(abs_path)

score = 0
sound_volume = 0
music_volume = 0
# initialize pygame
pygame.init()
clock = pygame.time.Clock()

# defining display
W, H = 800, 600
HW, HH = W/2, H/2
AREA = W * H
screen = pygame.display.set_mode((W, H))

# Title and Icon Window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# score
score_val = 0
score_font = pygame.font.Font('XXIX.otf', 32)
scoreX = 10
scoreY = 10

# Game Over Text
over_font = pygame.font.Font('XXIX.otf', 64)

# Player
playerImg = pygame.image.load('player\player4.png').convert_alpha()
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyhp = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_rects = []
num_enemies = 2
enemies = {
    1: 'enemies\enemy1.png',
    2: 'enemies\enemy2.png',
    3: 'enemies\enemy3.png',
    4: 'enemies\enemy4.png'
}
for i in range(num_enemies):
    num = random.randint(1, 4)
    enemyImg.append(pygame.image.load(enemies[num]).convert_alpha())
    enemyhp.append(100)
    enemyX.append(random.randint(20, 700))
    enemyY.append(random.randint(10, 70))
    enemyX_change.append(5)
    enemyY_change.append(0)

boomImg = []
for i in range(9):
    boomImg.append(pygame.image.load('explosion/boom0000'+str(i)+'.png'))
print(boomImg)

# Bullet
bulletImg = pygame.image.load('player/bullet1.png').convert_alpha()
bulletX = 0
bulletY = 500
bulletY_change = 5
bullet_state = 'ready'  # ready - can't see/ fire - bullet is currently moving
bullet_sound = mixer.Sound('laser.wav')
bullet_sound.set_volume(sound_volume)

# hit sound
explosion_sound = mixer.Sound('explosion.wav')
explosion_sound.set_volume(sound_volume/3)

# Image_background
bg = pygame.image.load('bg4.png').convert()

# background music
mixer.music.load('background.wav')
pygame.mixer.music.set_volume(music_volume)
mixer.music.play(loops=-1)

# Stars_background
stars = pygame.image.load('stars4.png').convert_alpha()
starsX = 0
starsY = -2000


def show_score(x, y):
    score = score_font.render(str(score_val), True, (255, 255, 255, 10))
    screen.blit(score, (x, y))


def gameover_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255, 10))
    screen.blit(over_text, (x, y))


def stars_background(x, y):
    screen.blit(stars, (x, y))


def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+15, y+30))


def explode(i, x, y):
    screen.blit(boomImg[i], (x, y))

# border wrap for entities


def ent_wrap(ent_x):
    if ent_x > 810:
        ent_x = -64
    elif ent_x < -64:
        ent_x = 810
    return ent_x

# bounce wrap for entities


def ent_bounce(ent_x, ent_changeX):
    ent_changeY = 0
    if ent_x > 736:
        ent_changeX = -1
        ent_changeY = 32
    elif ent_x < 0:
        ent_changeX = 1
        ent_changeY = 32
    return ent_changeX, ent_changeY


# Game Loop
running = True
while running:
    test = clock.tick()

    # update bullet rect position
    bullet_rect = bulletImg.get_rect().move(bulletX, bulletY)

    # print(playerX_change)
    # RGB
    screen.fill((120, 67, 101))

    # Background Image
    screen.blit(bg, (0, 0))

    # stars backgroundd
    starsY += 0.1
    rel_sY = starsY % stars.get_rect().height
    if rel_sY < H:
        stars_background(0, rel_sY)

    # Make sure player wraps around
    playerX = ent_wrap(playerX)

    for i in range(num_enemies):
        enemy_rect = enemyImg[i].get_rect().move(enemyX[i], enemyY[i])
        enemy_rects.append(enemyImg[i].get_rect().move(enemyX[i], enemyY[i]))

        enemyX_change[i], enemyY_change[i] = ent_bounce(
            enemyX[i], enemyX_change[i])

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        # Game Over
        if enemyY[i] > 400:
            for j in range(num_enemies):
                enemyY[j] = 2000

            gameover_text(200, 250)
            break

        if enemy_rect.colliderect(bullet_rect):
            test_time = pygame.time.get_ticks()
            print(test_time)
            explosion_sound.play()
            enemyhp[i] -= 5
            for j in range(9):
                explode(j, enemyX[i], enemyY[i])

            if enemyhp[i] < 1:
                score_val += 1
                new = random.randint(1, 4)
                enemyhp[i] = 100
                enemyImg[i] = pygame.image.load(enemies[new])
                enemyX[i] = random.randint(20, 700)
                enemyY[i] = random.randint(10, 70)

        enemy(i, enemyX[i], enemyY[i])

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke check
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and bullet_state == "ready":
            bullet_sound.play()
            pygame.key.set_repeat(1, 10)
            bulletX = playerX
            fire_bullet(bulletX, bulletY)
        if keys[pygame.K_a]:
            pygame.key.set_repeat(1, 10)
            playerX_change += -0.02
            if playerX_change >= 0:
                playerX_change = -(playerX_change)

            if playerX_change <= -(1.5):
                playerX_change = -1.5

        elif keys[pygame.K_d]:
            pygame.key.set_repeat(1, 10)
            playerX_change += 0.02
            if playerX_change <= 0:
                playerX_change = -(playerX_change)

            if playerX_change >= abs(1.5):
                playerX_change = 1.5

    if not keys[pygame.K_d] and not keys[pygame.K_a]:
        if playerX_change > 0:
            playerX_change -= 0.001
        elif playerX_change < 0:
            playerX_change += 0.001

    # bullet_movement
    if bulletY < -50:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # display layers
    stars_background(0, rel_sY - stars.get_rect().height)
    playerX += playerX_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()
