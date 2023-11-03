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
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]

        return obstacle_list
    else:
        return []
    
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True
    
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
last_score = 0

# Environment
sky_surf = pygame.image.load('Graphics/Sky.png').convert()
ground_surf = pygame.image.load('Graphics/ground.png').convert()

# Snail
snail_frame_1 = pygame.image.load('Graphics/Snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Graphics/Snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]

# Fly
fly_frame_1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

# List of enemies that are on screen
obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = player_walk_1 = pygame.image.load('Graphics/Player/jump.png').convert_alpha()

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

# Timer. Create custom user event: always sum 1 to evade conflicts with PyGame's user events
obstacle_timer = pygame.USEREVENT + 1
# Trigger the custom event in certain intervals
pygame.time.set_timer(obstacle_timer, 1500)

# Snail's animation timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

# Fly's animation timer
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_animation_timer == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly_frames[fly_index]
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        # block image transfer. Basically put a surface on another surface
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        display_score()
        last_score = get_last_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stant_rect)
        screen.blit(title_surf, title_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)

        if last_score == 0: screen.blit(instruc_surf, instruc_rect)
        else: display_last_score(last_score)

    mouse_pos = pygame.mouse.get_pos()

    # draw all our elements, update everything
    pygame.display.update()
    clock.tick(60) # this game shouldn't run faster than 60fps