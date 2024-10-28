from random import randint, choice
from turtle import back
import pygame, sys, random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_index = 0
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300
            
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.animation()
        self.destroy()
        self.rect.x -= 5

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        background_music.stop()
        gameOver_sound.play()
        return False
    else:
        return True


#pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Runner")
icon = pygame.image.load('graphics/player/p.ico')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',40)
game_active = False
start_time = 0
score = 0

# sound
gameOver_sound = pygame.mixer.Sound('audio/game over.mp3')
gameOver_sound.set_volume(1)
background_music = pygame.mixer.Sound('audio/Super Mario Bros Theme Song.mp3')
background_music.set_volume(0)

# grup
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))

title_surface = test_font.render('Pixel Runner',False,(111,196,169))
title_rect = title_surface.get_rect(center=(400,70))

gameOver_surface = test_font.render('Game Over!',False,(111,196,169))
gameOver_rect = gameOver_surface.get_rect(center=(400,70))

run_surface = test_font.render('Press enter to run',False,(111,196,169))
run_rect = run_surface.get_rect(center=(400,340))

restart_surface = test_font.render('Press enter to restart',False,(111,196,169))
restart_rect = restart_surface.get_rect(center=(400,340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    background_music.play()
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
        
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        result_surface = test_font.render(f'Your score: {score}',False,(111,196,169))
        result_rect = result_surface.get_rect(center=(100,40))
        if score == 0:
            screen.blit(title_surface,title_rect)
            screen.blit(run_surface,run_rect)
        else:
            screen.blit(gameOver_surface,gameOver_rect)
            screen.blit(restart_surface,restart_rect)
            screen.blit(result_surface,result_rect)
            
    pygame.display.update()
    clock.tick(60)