import pygame 
import math
import random

#Handle music in the game
from pygame import mixer

# Initialize the pygame
pygame.init()

#Initializes screen for display (We put the width and height respectfully))
screen = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load("background.jpg")

#Background Sound
mixer.music.load("background.wav")
# -1 plays the music on loop
mixer.music.play(-1)

# Resize the background image to fit the screen
background = pygame.transform.scale(background, (800, 600))


#Caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0 

#Enemy
#To make multiple enemies, we will save their values in a list
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg .append(pygame.image.load("enemy.png"))
    #Give the enemy a random value
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
#Give the enemy a random value
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.4
bullet_state = "ready"

#Score
score_value = 0
#Style of text to display (Font, Size)
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

#Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    #Instead of blitting the text, we are going to render the text
    #render(text to show, wether to show it or no, color)
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER : " + str(score_value), True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    # blit() -> Draw an image of the player onto the screen, this screen is known as the surface of the screen
    # (image, xy axis)
    screen.blit(playerImg, (x,y))

def enemy(x,y,pos):
    screen.blit(enemyImg[pos], (x,y))

def fire_bullet(x,y):
    #We can access to the bullet_state variable from this function
    global bullet_state
    bullet_state = "fire"
    #We are adding the values to make shure the bullet appears on the center of the space ship
    screen.blit(bulletImg, (x + 16,y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    # Distance between two points D = sqrt*(x2 - x1)^2 + (y2 - y1)^2)
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if (distance < 27):
        return True
    else:
        return False

#The game will be executed inside this loop 
# So, when the variable running changes to False, it will stop
running = True

#We are using the set to store the pressed right arrow and left to avoid stopping the player while one key is still pressed
pressed_keys = set()

while running:
    #RGB -> Red, Green and Blue - 3 values to implement any color and the screen
    screen.fill((0,0,0))

    #Background image
    screen.blit(background, (0,0))

    # We will loop through all of the events that are happening inside the window
    for event in pygame.event.get():
        # If the user press the cross button, the while loop ends
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check wether its right or left 
        #KEYDOWN CHECKS THE KEYS THAT ARE BEING PRESSED
        if event.type == pygame.KEYDOWN:
            #This checks if the key pressed is the left arrow
            if event.key == pygame.K_LEFT:
                pressed_keys.add(event.key)
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                pressed_keys.add(event.key)
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                # Only if bullet state is ready, we can fire a bullet
                if bullet_state == "ready":
                    # In this case it is not mixer.music, it is mixer.Sound as it is one sound only
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        #KEYUP CHECKS THE KEYS THAT ARE BEING PRESSED AND RELEASED
        if event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                pressed_keys.remove(event.key)
            if pygame.K_LEFT not in pressed_keys and pygame.K_RIGHT not in pressed_keys:
                playerX_change = 0

    #Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
        #Subtract 64 to 800 to see the spaceship fit in the window
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for pos in range(num_of_enemies):

        #Game Over
        if enemyY[pos] > 480:
            # Get the enemies out of the screen
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[pos] += enemyX_change[pos]
        if enemyX[pos] <= 0:
            enemyX_change[pos] = 0.2
            enemyY[pos] += enemyY_change[pos]
        elif enemyX[pos] >= 736:
            enemyX_change[pos] = -0.2
            enemyY[pos] += enemyY_change[pos]

        #Collision
        collision = isCollision(enemyX[pos], enemyY[pos], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            #Reset the bullet
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #Respawn the enemy
            enemyX[pos] = random.randint(0, 735)
            enemyY[pos] = random.randint(50, 150)

        enemy(enemyX[pos], enemyY[pos], pos)

    #Bullet Movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    show_score(textX,textY)

    #We need to update the display to show the color
    pygame.display.update() 