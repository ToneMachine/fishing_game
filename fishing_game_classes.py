import pygame
from sys import exit
import math

import pygame.mouse

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('fishing_game/graphic/npc/fisherman.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(400, 90))
        self.player_x_move = 0

    def player_input(self):
        #player inputs
        keys = pygame.key.get_pressed()
        self.player_x_move = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x_move -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x_move += 5

    def update(self):
        self.player_input()
        self.rect.x += self.player_x_move
        # boundries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800   

        # fishing line
        pygame.draw.line(screen,'black',(self.rect.topright),pygame.mouse.get_pos(), 2)
        pygame.mouse.set_visible(False)

class Lobster(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('fishing_game/graphic/npc/lobster.png')
        self.rect = self.image.get_rect(topleft=(750, 350))
        self.movement = 3
        self.caught = 2
        self.player = player
        self.is_caught = False

    def update(self):
        if not self.is_caught:
            # Lobster movement
            self.rect.x -= self.movement
            if self.rect.right < 0:
                self.rect.left = 800

            # Check for mouse button hold and collision with the Lobster
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
                self.is_caught = True
        
        elif self.is_caught:
            # Move towards the player
            self.move_towards_player()
            pygame.mouse.set_pos(self.rect.topright)

    def move_towards_player(self):
        player_pos = self.player.rect.midbottom
        direction = (player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        distance = math.hypot(*direction)
        if distance != 0:
            direction = (direction[0] / distance, direction[1] / distance)
            self.rect.x += direction[0] * self.caught
            self.rect.y += direction[1] * self.caught

        if self.rect.y < 75:
            self.movement = 0
            self.caught = 0
        
class Nemo(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('fishing_game/graphic/npc/nemo.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 200))
        self.movement = 3
        self.caught = 2
        self.player = player
        self.is_caught = False

    def update(self):
        if not self.is_caught:
            # Fish movement 
            self.rect.x += self.movement
            if self.rect.left > 800:
                self.rect.right = 0

            # Check for mouse button hold and collision with the Nemo
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
                self.is_caught = True
        else:
            # Move towards the player
            self.move_towards_player()
            pygame.mouse.set_pos(self.rect.topright)



    def move_towards_player(self):
        player_pos = self.player.rect.midbottom
        direction = (player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        distance = math.hypot(*direction)
        if distance != 0:
            direction = (direction[0] / distance, direction[1] / distance)
            self.rect.x += direction[0] * self.caught
            self.rect.y += direction[1] * self.caught

        if self.rect.y < 75:
            self.movement = 0
            self.caught = 0

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Fishing")
clock = pygame.time.Clock()

# Background
ocean_surface = pygame.image.load('fishing_game/graphic/surface/background1.png').convert()

# Player
player = Player()
player_single = pygame.sprite.GroupSingle()
player_single.add(player)

#fishes
nemo = Nemo(player)
lobster = Lobster(player)
fish_group = pygame.sprite.Group()
fish_group.add(nemo, lobster)

# Scoreboard
score = 0
score_font = pygame.font.Font(None, 30)

def update_scoreboard():
    global score_surf, score_rect
    score_surf = score_font.render(f'Score: {score}', True, 'White')
    score_rect = score_surf.get_rect(topleft=(20, 10))

update_scoreboard()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Background
    screen.blit(ocean_surface, (0, 0))

    # score board
    pygame.draw.rect(screen,'Black',score_rect)
    screen.blit(score_surf,(score_rect))

    # Update and draw player
    player_single.update()
    player_single.draw(screen)

    # fish
    fish_group.update()
    fish_group.draw(screen)

    # lobster collide
    if pygame.sprite.collide_rect(player, lobster):
        lobster.rect.left = 0
        lobster.rect.y = 350
        pygame.mouse.set_pos(player.rect.topright)
        lobster.is_caught = False
        score += 10
        update_scoreboard()

    # nemo collide
    elif pygame.sprite.collide_rect(player, nemo):
        nemo.rect.right = 0
        nemo.rect.y = 200
        pygame.mouse.set_pos(player.rect.topright)
        nemo.is_caught = False
        score += 5
        update_scoreboard()

    # Tick rate
    pygame.display.update()
    clock.tick(60)