import pygame
import random
import math
from pygame import  mixer
# initalize the pygame
pygame.init()

#background
background = pygame.image.load('asgard.png')

#backround music
mixer.music.load('background_new.wav')
mixer.music.play(-1)

#set icon
icon = pygame.image.load('skull.png')
pygame.display.set_icon(icon)

#screen set
screen = pygame.display.set_mode((800,600))

#title of the window
pygame.display.set_caption("Thor Smash")

#player image loading
playerimg = pygame.image.load('thor.png')
playerx = 370
playery = 480
playerx_change = 0

#enemy image loading
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 800))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.3)
    enemyy_change.append(40)

#Bullet image loading
bulletimg = pygame.image.load('thors.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 1
bullet_state = "ready"
#score
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
textx = 10
texty = 10

#game over function
over_text = pygame.font.Font("freesansbold.ttf",64)


def show_score(x,y):
    scores = font.render("Score : " + str(score),True, (225,225,225))
    screen.blit(scores, (x,y))

def game_over():
    game_over_text = over_text.render("GAME OVER" ,True, (225,225,225))
    screen.blit(game_over_text, (200,250))


def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x,y))


def collition(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("hammer.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx,bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

#enemy movement
    for i in range(num_of_enemy):

        #game over
        if enemyy[i] > 440:
            for j in range(num_of_enemy):
                enemyy[j] = 2000
            game_over()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i]  <= 0:
            enemyx_change[i]  = 0.3
            enemyy[i]  += enemyy_change[i]
        elif enemyx[i]  >= 736 :
            enemyx_change[i]  = -0.3
            enemyy[i]  += enemyy_change[i]
        # collition
        collition_v = collition(enemyx[i], enemyy[i], bulletx, bullety)
        if collition_v:
            bullet_sound = mixer.Sound("explosion.wav")
            bullet_sound.play()
            bullety = 480
            bullet_state = "ready"
            score = score + 1
            enemyx[i] = random.randint(0, 800)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i],i)

    #bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change
    # #collition
    # collition_v = collition (enemyx,enemyy,bulletx,bullety)
    # if collition_v:
    #     bullety = 480
    #     bullet_state = "ready"
    #     score = score+1
    #     print(score)
    #     enemyx = random.randint(0, 800)
    #     enemyy = random.randint(50, 150)

    player(playerx, playery)
    show_score(textx,texty)
    pygame.display.update()
