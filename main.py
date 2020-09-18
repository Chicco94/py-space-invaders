import pygame
import random

#%%
# Inizializzazione schermata
pygame.init()

screen_width  = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
backgroud = pygame.image.load("resources/background.png")

# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("resources/logo.jpg")
pygame.display.set_icon(icon)

#%% Player
playerImg = pygame.image.load("resources/spaceship.png")
playerImg_size = 64
playerX = 400
playerY = screen_height - 2*playerImg_size
playerX_change = 0

def player(x,y):
	screen.blit(playerImg, (x, y))


#%% Score
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

def show_score(x,y):
	text = font.render("Score: {}".format(score), True, (255,255,255))
	screen.blit(text,(x,y))

game_over_font = pygame.font.Font("freesansbold.ttf",64)
def game_over():
	text = game_over_font.render("GAME OVER", True, (255,255,255))
	screen.blit(text,(200,200))


#%% Enemies
num_of_enemies = 10
enemies = range(0,num_of_enemies)
enemyImg = pygame.image.load("resources/enemy.png")
enemyImg_size = 64
enemyX 			= [random.randint(0+enemyImg_size,screen_width-enemyImg_size)		for enemy in enemies]
enemyY 			= [random.randint(0+enemyImg_size,screen_height//2-enemyImg_size)	for enemy in enemies]
enemyX_change 	= [5																for enemy in enemies]
enemyY_change 	= [10																for enemy in enemies]
enemy_state 	= ["active"															for enemy in enemies]

def enemy(x,y):
	screen.blit(enemyImg, (x, y))


#%% Bullet
bulletImg = pygame.image.load("resources/bullet.png")
bulletImg_size = 32
bulletX = random.randint(0+bulletImg_size,screen_width-bulletImg_size)
bulletY = random.randint(0+bulletImg_size,screen_height//2-bulletImg_size)
bulletX_change = 0
bulletY_change = -10
bullet_state = "ready"

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x, y))


#%% Collisions
explosionImg = pygame.image.load("resources/explosion.png")
explosionImg_size = 64

def show_collision(x,y):
	screen.blit(explosionImg, (x, y))

def isCollision(x_1,y_1,x_2,y_2):
	return distance(x_1,y_1,x_2,y_2) < enemyImg_size//2

def distance(x_1,y_1,x_2,y_2):
	return ( (x_1 - x_2)**2 +(y_1-y_2)**2 )**(1/2)


#%% Game
keep_going = True
while keep_going:
	screen.fill((255,255,255))
	screen.blit(backgroud,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			keep_going = False
	
		# player movement
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -5
			if event.key == pygame.K_RIGHT:
				playerX_change =  5
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bulletX = playerX+playerImg_size/2
					fire_bullet(playerX,playerY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				playerX_change =  0

	# apply movement to player
	if 0 < playerX + playerX_change < screen_width - playerImg_size:
		playerX += playerX_change

	# apply movement to enemy
	for i in enemies:

		# game over
		if enemyY[i] > 400:
			for j in enemies:
				enemy_state[j] = "hidden"
			game_over()
			break

		enemyX[i] += enemyX_change[i]
		if 0 >= enemyX[i]:
			enemyX_change[i] = - enemyX_change[i]
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= screen_width - enemyImg_size:
			enemyX_change[i] = - enemyX_change[i]
			enemyY[i] += enemyY_change[i]
		
		# collisions
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			# reset the bullet
			bullet_state = "ready"
			bulletY = playerY
			score += 1
			# respawn enemy
			enemy_state[i] = "dead"
			# show explosion
			show_collision(enemyX[i],enemyY[i])
			

	# bullet movement
	if bulletY <= 0:
		bulletY = playerY
		bullet_state = "ready"
	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY += bulletY_change

	# update the screen
	player(playerX,playerY)
	for i in enemies:
		if enemy_state[i] is "active":
			enemy(enemyX[i],enemyY[i])
		if enemy_state[i] is "dead":
			enemy_state[i] = "respawning"
		if enemy_state[i] is "respawning":
			enemy_state[i] = "active"
			enemyX[i] = random.randint(0+enemyImg_size,screen_width-enemyImg_size)
			enemyY[i] = random.randint(0+enemyImg_size,screen_height//2-enemyImg_size)

	show_score(textX,textY)
	pygame.display.update()