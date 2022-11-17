# Import Modules
import pygame
import sys
import math
import random
import datetime

# Constants
# Window Size
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Speeds/Times
SPEED = 6
FRAME_RATE = 60
SPAWN_RATE = 100
WIN_TIME = FRAME_RATE * 60 * 5

# Colour
WHITE = (255, 255, 255)

# Move
UP = pygame.K_w
DOWN = pygame.K_s
LEFT = pygame.K_a
RIGHT = pygame.K_d
SHOOT = pygame.MOUSEBUTTONDOWN

# init
# Pygame Init
pygame.init()
clock = pygame.time.Clock()

# Window set-up
game_window = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Shoot the Things')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('game_assets/character_right.png'), (100, 100)))

# Image Loading
def load_image(path_to_image, dimensions):
    loaded_image = pygame.image.load(path_to_image)
    image_surface = pygame.Surface.convert(loaded_image)
    return pygame.transform.scale(image_surface, dimensions)

def rotate_centre(image, rectangle, angle):
    rotate_image = pygame.transform.rotate(image, angle)
    rotate_rect = rotate_image.get_rect(center = rectangle.center)
    return rotate_image, rotate_rect

# Background
BACKGROUND = load_image('game_assets/background.png', DIMENSIONS)

# Player Images
CHARACTER_RIGHT = load_image('game_assets/character_right.png', (100, 100))
CHARACTER_LEFT = load_image('game_assets/character_left.png' , (100, 100))
BULLET = load_image('game_assets/bullet.png', (50, 25))

# Enemy Images
FLYING_ATTACKING_THING = load_image('game_assets/attack_thing.png',(100, 50))

# Font
MAIN_FONT = pygame.font.Font('game_assets/main_font.ttf', 25)

# Window Set-up

game_window.blit(BACKGROUND, (0, 0))

# Class Definitions
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.moving_right = True
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.is_move = False
        self.health_boost = False
        self.end_main_loop = False
        self.points = 0
        self.jump_up = 1
        self.facing_right = CHARACTER_RIGHT.copy()
        self.facing_left = CHARACTER_LEFT.copy()
        self.health = 20
        self.rect = self.facing_right.get_rect(center = (550, 500)) 
        self.left_rect = self.facing_left.get_rect(center = (550, 500))
        self.speed = SPEED
        self.image = None
        self.points = 0

    # Defines movement
    def update(self, game_window):
        
        if self.health <= 0:
            self.kill()
            self.end_main_loop = True
        else:
            game_window.blit(self.facing_right, (self.rect.x, self.rect.y))
            
            # Move right
            if self.moving_right:
                # game_window.blit(self.facing_right, (self.rect.x, self.rect.y))
                self.image = self.facing_right
                if self.is_move:
                    self.move_right()
                    self.is_move = False
                self.moving_right = False
                
            # Move left
            if self.moving_left:
                # game_window.blit(self.facing_left, (self.rect.x, self.rect.y))
                self.image = self.facing_left
                if self.is_move:
                    self.move_left()
                    self.is_move = False
                self.moving_left = False

            # Move up
            if self.moving_up and self.is_move:
                # game_window.blit(self.facing_right, (self.rect.x, self.rect.y))
                if self.is_move:
                    self.rect.y -= self.speed * 2
                    self.is_move = False
                self.moving_up = False

            # Move Down
            if self.moving_down and self.is_move:
                game_window.blit(self.facing_right, (self.rect.x, self.rect.y))
                if self.is_move:
                    self.rect.y += self.speed * 2
                    self.moving_down = False
                self.is_move = False
                    
            # Get Points
            self.points += 1
            if self.points == 300:
                self.speed *= 3
            elif self.points == 1500:
                self.health = 40
                
        if self.rect.x >= 1120:
            self.rect.x = 10
            
        if self.rect.x <= -60:
            self.rect.x = 1100
            
        if self.rect.y >= 620:
            self.rect.y = 10
            
        if self.rect.y <= -200:
            self.rect.y = 600
  
    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed
        
    def attacked(self):
        self.health -= 1

    def touching_autre(self, autre):
        if self.rect.colliderect(autre):
            self.health -= 1
            autre.kill()

            
class DangerousThings(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spawning_positions = [(50, 50),
                                   (700, 100),
                                   (950, 200),
                                   (50, 450),
                                   (550, 300),
                                   (1000, 550)
        ]
        all_bads.add(self)
        self.spawn = random.choice(self.spawning_positions)
        self.image = FLYING_ATTACKING_THING.copy()
        self.rect = self.image.get_rect(center = self.spawn)
        self.health = 1
        self.position = pygame.math.Vector2((self.rect.x, self.rect.y))
        self.speed = SPEED
        

    def update(self, player, game_window):
        player_pos = player.rect.center
        direction = player_pos - self.position
        velocity = direction.normalize() * self.speed
                                        
        # game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        if self.health <= 0:
            self.kill()
        else:
            self.position += velocity
            self.rect.topleft = self.position
            game_window.blit(self.image, (self.rect.x, self.rect.y))

    def touching_bullet(self, bullet, player):
        if self.rect.colliderect(bullet):
            player.points += 50
            bullet.kill()
            self.kill()
            
            

            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        all_bullets.add(self)
        self.spawn = (self.player.rect.x, self.player.rect.y)
        self.image = BULLET.copy()
        self.rect = self.image.get_rect(center = self.spawn)
        self.position = pygame.math.Vector2((self.rect.x, self.rect.y))
        self.speed = SPEED * 2

    def move(self, enemy, game_window):
        enemy_pos = enemy.rect.center
        direction = enemy_pos - self.position
        velocity = direction.normalize() * self.speed
        self.position += velocity
        self.rect.topleft = self.position
       

    def point(self, enemy, game_window):
        enemy_pos = enemy.rect
        angle = math.atan2(-(enemy.rect.y - self.rect.y), (enemy.rect.x - self.rect.x))
        angle = math.degrees(angle)
        rotated = pygame.transform.rotate(self.image, angle)
        game_window.blit(rotated, (self.rect.x, self.rect.y))

    def update(self, enemy, game_window):
        self.move(enemy, game_window)
        self.point(enemy, game_window)
        

        
class Counters(object):
    def __init__(self, player, points, timer):
        self.loop_count = 0
        self.font = MAIN_FONT
        self.player_health = player.health
        self.player_health_rect = None
        self.points = points
        self.points_rect = None
        self.timer = timer
        self.timer_rect = None
        self.player = player
        self.difficulty_level = 1
        self.difficulty_rect = None
        self.difficulty = 1
        
    def draw_player_health(self, game_window):
        self.player_health = self.player.health
        self.player_health_surface = self.font.render(str(self.player_health), True, WHITE)
        self.player_health_rect = self.player_health_surface.get_rect()
        self.player_health_rect.x = 25
        self.player_health_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(self.player_health_surface, self.player_health_rect)

    def draw_points(self, game_window):
        self.points = self.player.points
        self.points_surface = self.font.render(str(self.points), True, WHITE)
        self.points_rect = self.points_surface.get_rect()
        self.points_rect.x = 125
        self.points_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(self.points_surface, self.points_rect)
        
    def draw_timer(self, game_window):
        rendered_time = f'{str(datetime.timedelta(seconds = self.difficulty // 10))}'[2:]
        self.timer_surface = self.font.render(rendered_time, True, WHITE)
        self.timer_rect = self.timer_surface.get_rect()
        self.timer_rect.x = 247
        self.timer_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(self.timer_surface, self.timer_rect)

    def draw_difficulty(self, game_window):
        self.difficulty_surface = self.font.render(str(self.difficulty_level), True, WHITE)
        self.difficulty_rect = self.difficulty_surface.get_rect()
        self.difficulty_rect.x = 395
        self.difficulty_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(self.difficulty_surface, self.difficulty_rect)

    def update(self, game_window):
        self.loop_count += 1
        self.draw_player_health(game_window)
        self.draw_points(game_window)
        self.draw_timer(game_window)
        self.draw_difficulty(game_window)
    


        
all_bads = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

# Main function
def main():
    start_running = True
    click_to_start = MAIN_FONT.render('Click Anywhere to Start', True, WHITE)
    
    while start_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_running = False

        game_window.blit(BACKGROUND, (0, 0))
        game_window.blit(click_to_start, (0, 0))
        pygame.display.update()
    game_running = True
    game_ended = True
    game_can_end = False
    
    player = Player()
    
    counters = Counters(player, player.points, WIN_TIME)
    # Main Game Loop
    while game_running:
        pygame.time.delay(100)
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                Bullet(player)
           
        if pressed_keys[pygame.K_a]:
            player.moving_left = True
            player.is_move = True
            player.image = player.facing_left
            
        if pressed_keys[pygame.K_d]:
            player.moving_right = True
            player.is_move = True
            player.image = player.facing_right                    
        if pressed_keys[pygame.K_w]:
            player.moving_up = True
            player.is_move = True
                                                     
        if pressed_keys[pygame.K_s]:
            player.moving_down = True
            player.is_move = True

        if pressed_keys[pygame.K_w] and pressed_keys[pygame.K_d]:
            player.rect.y -= player.speed
            player.rect.x += player.speed
            
        if pressed_keys[pygame.K_w] and pressed_keys[pygame.K_a]:
            player.rect.y -= player.speed
            player.rect.x -= player.speed
            
        if pressed_keys[pygame.K_s] and pressed_keys[pygame.K_d]:
            player.rect.y += player.speed
            player.rect.x += player.speed
            
        if pressed_keys[pygame.K_s] and pressed_keys[pygame.K_a]:
            player.rect.y += player.speed
            player.rect.x -= player.speed
        ifrand = random.randint(1, int(SPAWN_RATE / counters.difficulty_level))
        
        if ifrand == 1:
            DangerousThings()

        player.update(game_window)
        # win-loss
        if player.points >= 5000:
            game_running = False
            game_can_end = True
        elif player.health <= 0:
            game_running = False
            game_can_end = True

        # game_window.fill((0, 0, 0))
        game_window.blit(BACKGROUND, (0, 0))
        for bad in all_bads:
            bad.update(player, game_window)
            game_window.blit(bad.image, bad.rect)
            player.touching_autre(bad)
            for bullet in all_bullets:
                bullet.update(bad, game_window)
                bad.touching_bullet(bullet, player)
        game_window.blit(player.image, player.rect)
        counters.update(game_window)
        
        pygame.display.update()
        
        counters.difficulty += 1
        if counters.difficulty == 750:
            counters.difficulty_level = 2
        elif counters.difficulty == 1500:
            counters.difficulty_level = 3
        elif counters.difficulty == 2500:
            counters.difficulty_level = 4
        elif counters.difficulty == 3200:
            counters.difficulty_level = 5
        elif counters.difficulty == 4000:
            counters.difficulty_level = 6
            

        clock.tick(FRAME_RATE)
        
    start_game_again = MAIN_FONT.render('Click anywhere to play again', True, WHITE)
    start_game_again_2 = MAIN_FONT.render('Close window to quit', True, WHITE)
    end_font = pygame.font.Font('game_assets/main_font.ttf', 85)
    if game_ended and game_can_end:
        if player.points >= 5000:
            end_surface = end_font.render('won.', True, WHITE)
        else:
            end_surface = end_font.render('lost', True, WHITE)
        game_window.blit(end_surface, (350, 250))
        game_window.blit(start_game_again, (265, 375))
        game_window.blit(start_game_again_2, (315, 415))
        pygame.display.update()

    while game_ended and game_can_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()

        clock.tick(FRAME_RATE)
        
    
# Run
if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
