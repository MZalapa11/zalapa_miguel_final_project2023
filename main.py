# This file was created by: Miguel Zalapa
'''
I want to make a game like agar.io or slither.io
I want my main player to kill mobs with a sword
Add a sword
Mobs that attack my player
My player dies when the mobs run into him
'''
import pygame, sys, random, math, time
from pygame.locals import*
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
FPS = 30
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Agar.io")

cell_count = 2000
bot_count = 20
map_size = 2000
spawn_size = 25
bots_min_size = 25
bots_max_size = 250
respawn_cells = True
respawn_bots = False
player_color = (255, 0, 0)
background_color = (0, 0, 0)
text_color = (255, 255, 255)

FONT = pygame.font.Font("freesansbold.ttf", 32)
FONT = pygame.font.Font("freesansbold.ttf", 72)
WIDTH = 1280
HEIGHT = 720
cells = []
bots = []
game_over = False

counter = 0
frame_rate =30
start_time = 0
frame_rate_delay = 0.5

#class to make our cells from
class Cell():
    def __init__(self, x, y, color, radius, name):
        self.name = name
        self.radius = radius
        self.color = color
        self.status = random.randint(1, 8)
        self.x_pos = x
        self.y_pos = y
    def wander(self):
        pass
    def collide_check(self, player):
        global cells, bots, game_over
        for cell in cells:
            if math.sqrt(((player.x_pos - (WIDTH/2) + cell.x_pos) ** 2 + (player.y_pos - (HEIGHT/2) + cell.y_pos) ** 2)) <= cell.radius + player.radius and cell.radius <= player.radius:
                cells.remove(cell)
                player.radius += 0.25
                if respawn_cells:
                    new_cell = Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "cell") 
                    cells.append(new_cell)
    def draw(self, surface, x, y):
        pygame.draw.circle(surface, self.color, (x, y), int(self.radius))
        if self.name == "Bot" or self.name == "Player":
            text = FONT.render(str(round(self.radius)), False, text_color)
for i in range(cell_count):
    new_cell = Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "cell")
    cells.append(new_cell)

player_cell = Cell(0, 0, player_color, spawn_size, "Player")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
        if event.type == MOUSEMOTION and game_over == False:
            mouse_x, mouse_y = event.pos
        else:
            mouse_x = WIDTH/2
            mouse_y = HEIGHT/2
    if not game_over:
        player_cell.collide_check(player_cell)
    player_cell.x_pos += round(-((mouse_x - (WIDTH/2)) / player_cell.radius/2 ))
    player_cell.y_pos += round(-((mouse_y - (HEIGHT/2)) / player_cell.radius/2 ))

    for cell in cells:
        cell.draw(SCREEN, cell.x_pos + player_cell.x_pos, cell.y_pos + player_cell.y_pos)
    if game_over == True:
        text = BIGFONT.render("You lose!", False, text_color)
        SCREEN.blit(text, ((WIDTH/2) - 150, (HEIGHT/2)-40))
    else:
        player_cell.draw(SCREEN, (WIDTH/2), (HEIGHT/2))
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.update()
    CLOCK.tick(FPS)
    SCREEN.fill(background_color)

