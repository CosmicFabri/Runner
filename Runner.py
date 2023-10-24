import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = int(current_time / 1500)
    # if current_time % 2300 == 0: score += 1
    score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

def get_last_score():
    current_time = pygame.time.get_ticks() - start_time
    last_score = int(current_time / 1500)
    return last_score

# Display highscore on screen
def display_last_score(last_score):
    last_score_font = pygame.font.Font('Font/Pixeltype.ttf', 60)
    last_score_surf = last_score_font.render(f'Last score: {last_score}', False, "Black")
    last_score_rect = last_score_surf.get_rect(center = (400, 330))
    screen.blit(last_score_surf, last_score_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            screen.blit(snail_surf, obstacle_rect)
        return obstacle_list
    else:
        return []
    
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
last_score = 0

sky_surf = pygame.image.load('Graphics/Sky.png').convert()
ground_surf = pygame.image.load('Graphics/ground.png').convert()

# score_surf = test_font.render('My game', False, (64, 64, 64))
# score_rect = score_surf.get_rect(center = (400, 70))

# Obstacles (enemies)
snail_surf = pygame.image.load('Graphics/Snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

obstacle_rect_list = []

player_surf = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stant_rect = player_stand.get_rect(center = (400, 200))
title_font = pygame.font.Font('Font/Pixeltype.ttf', 70)
title_surf = title_font.render("Runner game!", False, "Blue")
title_rect = title_surf.get_rect(center = (400, 70))
instruc_font = pygame.font.Font('Font/pixeltype.ttf', 60)
instruc_surf = instruc_font.render("Press space to jump!", False, "Black")
instruc_rect = instruc_surf.get_rect(center = (400, 330))

# Timer. Create custom user event: always add a '+1' to evade conflicts with PyGame's user events
obstacle_timer = pygame.USEREVENT + 1
# Trigger the custom event in certain intervals
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()

    if game_active:
        # block image transfer. Basically put a surface on another surface
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        display_score() 

        # snail_rect.x -= 6
        # if snail_rect.right < 0: snail_rect.x = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
            last_score = get_last_score()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stant_rect)
        screen.blit(title_surf, title_rect)
        if last_score == 0: screen.blit(instruc_surf, instruc_rect)
        else: display_last_score(last_score)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]: print("Jump!")

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed()) # Checking which of the mouse buttons is being pressed
    
    # draw all our elements, update everything
    pygame.display.update()
    clock.tick(60) # this game shouldn't run faster than 60fps