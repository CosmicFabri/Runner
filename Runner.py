import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Runner/Font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('Runner/Graphics/Sky.png').convert()
ground_surf = pygame.image.load('Runner/Graphics/ground.png').convert()

score_surf = test_font.render('My game', False, (64, 64, 64))
score_rect = score_surf.get_rect(center = (400, 70))

snail_surf = pygame.image.load('Runner/Graphics/Snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('Runner/Graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20

    # block image transfer. Basically put a surface on another surface
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect.inflate(10, 10), 5, 8)
    # pygame.draw.ellipse(screen, "Brown", pygame.Rect(300, 200, 100, 100))
    screen.blit(score_surf, score_rect)
    screen.blit(snail_surf, snail_rect)

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    screen.blit(player_surf, player_rect)
    # print(player_rect.left)
    snail_rect.x -= 4
    if snail_rect.x < -70: snail_rect.x = 800

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]: print("Jump!")

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed()) # Checking which of the mouse buttons is being pressed
    
    # draw all our elements
    # update everything
    pygame.display.update()
    clock.tick(60) # this game shouldn't run faster than 60fps