import pygame
import os
import random

pygame.init()

width = 800
height = 460
screen = pygame.display.set_mode((width, height))

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#constant game variables 
gravity = 0.7
tile_size = 20
ground_level = 409  # Ground level for enemies and player

#define player action variables 
moving_left = False 
moving_right = False
shoot = False
game_over = False  # Track game state

# Camera variables
camera_x_offset = 0
camera_speed = 5

#load images 
bullet_img = pygame.image.load('bullet.PNG').convert_alpha()
points_coin = pygame.image.load('coin.PNG').convert_alpha()
health_coin = pygame.image.load('health.PNG').convert_alpha()

# Load background image and set its width
background_img = pygame.image.load('backround.png').convert()
background_width = background_img.get_width()

items = {
    'Health': health_coin, 
    'Points': points_coin
}

#define colours
BG = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font('font.ttf', 30)

def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))

def draw_bg():
    # Draw two backgrounds to create a continuous scrolling effect
    screen.blit(background_img, (camera_x_offset % background_width, 0))
    screen.blit(background_img, ((camera_x_offset % background_width) - background_width, 0))

def update_camera(player):
    global camera_x_offset
    # Move the camera to follow the player
    if player.rect.centerx > width // 2:
        camera_x_offset = -player.rect.centerx + width // 2
    else:
        camera_x_offset = 0

#CHARACTERS (HEROS AND ENEMYS)
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.points = 0
        self.max_health = self.health
        self.direction = 1
        self.velocity_y = 0
        self.jump = False 
        self.flip = False
        idle = pygame.image.load(f'{self.char_type}.png').convert_alpha()
        self.idle = pygame.transform.scale(idle, (int(idle.get_width() * scale), int(idle.get_height() * scale)))
        self.rect = self.idle.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #reset movement variables 
        dx = 0
        dy = 0

        #assign movement variables for left and right 
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right: 
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True:
            self.velocity_y = -10
            self.jump = False

        #gravity
        self.velocity_y += gravity 
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y

        #check collision with floor
        if self.rect.bottom + dy > ground_level:
            dy = ground_level - self.rect.bottom

        #update rect position
        self.rect.x += dx
        self.rect.y += dy

    #shoot
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            # Spawn bullet at player's gun location (near player's hand)
            bullet_x = self.rect.centerx + (50 * self.direction)
            bullet_y = self.rect.centery - 20  # Adjust bullet height relative to player
            bullet = Bullet(bullet_x - camera_x_offset, bullet_y, self.direction)  # Take camera offset into account
            bullet_group.add(bullet)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0 
            self.speed = 0
            self.alive = False

    def draw(self):
        # Draw player and apply camera offset
        screen.blit(pygame.transform.flip(self.idle, self.flip, False), (self.rect.x + camera_x_offset, self.rect.y))


#ENEMY CLASS
class Enemy(Character):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__(char_type, x, y, scale, speed)
        self.direction = random.choice([-1, 1])  # Random initial direction

    def move(self):
        # Make enemy move randomly
        if self.alive:
            self.rect.x += self.speed * self.direction

            # Change direction if the enemy hits the screen boundaries or randomly
            if self.rect.left < 0 or self.rect.right > 2000:
                self.direction *= -1

    def check_alive(self):
        if self.health <= 0:
            self.kill()

    def draw(self):
        # Draw enemies and apply camera offset
        screen.blit(pygame.transform.flip(self.idle, self.flip, False), (self.rect.x + camera_x_offset, self.rect.y))


#COLLECTABLES
class Collectables(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type 
        self.image = items[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x , y)

    def update(self):
        if pygame.sprite.collide_rect(self, player_idle):  
          if self.item_type == 'Health':
            player_idle.health += 20
            if player_idle.health > player_idle.max_health:
                player_idle.health = player_idle.max_health
          elif self.item_type == 'Points':
            player_idle.points += 100
          self.kill()

    def draw(self):
        # Draw items without applying camera offset (stationary)
        screen.blit(self.image, (self.rect.x, self.rect.y))


#HEALTHBAR
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health      
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health 
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


#BULLETS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > 2000:
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.health -= 20
                self.kill()


# Randomly generate positions for items and enemies
def generate_random_positions(num_items, num_enemies):
    for _ in range(num_items):
        x = random.randint(0, 2000)
        y = ground_level  # Ensure items are on the ground
        item_type = random.choice(['Health', 'Points'])
        item = Collectables(item_type, x, y)
        items_group.add(item)

    for _ in range(num_enemies):
        x = random.randint(0, 2000)
        y = ground_level  # Ensure enemies are on the ground
        enemy = Enemy('enemy', x, y, 1, 2)
        enemy_group.add(enemy)


#sprite groups 
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

# Randomly generate collectable items and enemies
generate_random_positions(num_items=5, num_enemies=3)

#create characters
player_idle = Character('shoot', 60, ground_level, 1, 5)

health_bar = HealthBar(10, 10, player_idle.health, player_idle.health)

backround = Character('backround', 400, 230, 1, 5)

def restart_game():
    global game_over
    player_idle.health = player_idle.max_health
    player_idle.alive = True
    game_over = False
    bullet_group.empty()
    enemy_group.empty()
    items_group.empty()
    generate_random_positions(num_items=5, num_enemies=3)  # Regenerate items and enemies


run = True
while run == True:

    clock.tick(FPS)

    if not game_over:
        draw_bg()
        update_camera(player_idle)  # Update camera position

        backround.draw()
        health_bar.draw(player_idle.health)
        draw_text(f'Points: {player_idle.points}', font, BG, 15, 40)

        for enemy in enemy_group:
            enemy.move()  # Move enemies randomly
            enemy.draw()

            # Check for collision between player and enemies
            if pygame.sprite.collide_rect(player_idle, enemy):
                player_idle.health -= 1  # Player loses health upon collision

        items_group.update()
        items_group.draw(screen)

        player_idle.update()
        player_idle.draw()
        player_idle.move(moving_left, moving_right)

        #update and draw groups 
        bullet_group.update()
        bullet_group.draw(screen)

        #update player actions 
        if player_idle.alive:
            if shoot:
                player_idle.shoot()
        else:
            game_over = True  # Player has died

    else:
        # Game over state
        draw_text('GAME OVER', font, WHITE, width // 2 - 100, height // 2)
        draw_text('Press R to Restart', font, WHITE, width // 2 - 150, height // 2 + 50)

    for event in pygame.event.get():

    #game exit
        if event.type == pygame.QUIT:
            run = False

    #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player_idle.alive:
                moving_left = True
            if event.key == pygame.K_d and player_idle.alive:
                moving_right = True
            if event.key == pygame.K_w and player_idle.alive:
                player_idle.jump = True
            if event.key == pygame.K_SPACE and player_idle.alive:
                shoot = True
            if event.key == pygame.K_r and game_over:  # Restart when game over
                restart_game()

    #keyboard releases 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()
