# This file was created by: Miguel Zalapa
'''
I want to make a game like agar.io or slither.io
I want my main player to kill mobs with a sword
Add a sword
Mobs that attack my player
My player dies when the mobs run into him
My player wins when he reaches 30 points
Sources: 
https://www.youtube.com/@procrastinationnation77
Chat.gpt
Chris Cozort
'''
import pygame, sys, random, math, time
from pygame.locals import*
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
FPS = 30
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Agar.io")

cell_count = 2000
bot_count = 30
map_size = 2000
spawn_size = 25
bots_min_size = 15
bots_max_size = 25
respawn_cells = True
respawn_bots = False
player_color = (255, 0, 0)
background_color = (0, 0, 0)
text_color = (255, 255, 255)

FONT = pygame.font.Font("freesansbold.ttf", 32)
BIGFONT = pygame.font.Font("freesansbold.ttf", 72)
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
        randomize = random.randint(1, round(self.radius))
        if randomize == 1:
            self.status = random.randint(1,8)
        
        if self.status == 1:
            self.y_pos += 300 / self.radius
        elif self.status == 2:
            self.x_pos += 150 / self.radius
            self.y_pos += 150 / self.radius
        elif self.status == 3:
            self.x_pos += 300 / self.radius
        elif self.status == 4:
            self.x_pos += 150 / self.radius
            self.y_pos -= 150 / self.radius
        elif self.status == 5:
            self.y_pos -= 300 / self.radius
        elif self.status == 6:
            self.x_pos -= 150 / self.radius
            self.y_pos -= 150 / self.radius
        elif self.status == 7:
            self.x_pos -= 300 / self.radius
        elif self.status == 8:
            self.x_pos -= 150 / self.radius
            self.y_pos += 150 / self.radius
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
        if self.name == "Bot" or self.name == "Player" or self.name == "cell":
            text = FONT.render(str(round(self.radius)), False, text_color)
# New class for horizontally moving mobs
class HorizontalMob(Cell):
    def __init__(self, y, color, speed, name):
        x = random.randint(-map_size, map_size)
        super().__init__(x, y, color, 10, name)  # Adjust the radius and other parameters as needed
        self.speed = speed
    def move(self):
        self.x_pos += self.speed
# Create a list to store horizontal mobs
horizontal_mobs = [HorizontalMob(random.randint(-map_size, map_size), (0, 0, 255), 2, "HorizontalMob") for _ in range(45)]

class Bot(Cell):
    def __init__(self, x, y, radius, name):
        super().__init__(x, y, (0, 255, 0), radius, name)

    def wander(self, player_cell):
        direction_x = player_cell.x_pos - self.x_pos
        direction_y = player_cell.y_pos - self.y_pos
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance != 0:
            normalized_direction_x = direction_x / distance
            normalized_direction_y = direction_y / distance

            # Adjust the bot's position based on the normalized direction vector
            self.x_pos += normalized_direction_x * 3  # Adjust the factor for speed
            self.y_pos += normalized_direction_y * 3  # Adjust the factor for speed
# class to add mobs
for i in range(cell_count):
    new_cell = Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "cell")
    cells.append(new_cell)

player_cell = Cell(0, 0, player_color, spawn_size, "Player")
cells = [Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "cell") for _ in range(cell_count)]
bots = [Bot(random.randint(-map_size, map_size), random.randint(-map_size, map_size), random.randint(bots_min_size, bots_max_size), "Bot") for _ in range(bot_count)]
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and game_over == False:
            mouse_x, mouse_y = event.pos
        else:
            mouse_x = WIDTH/2
            mouse_y = HEIGHT/2
    
    if not game_over:
        # Check for collisions with cells
        player_cell.collide_check(player_cell)

        # Check for collisions with horizontally moving mobs
        for mob in horizontal_mobs:
            distance = math.sqrt((player_cell.x_pos - mob.x_pos)**2 + (player_cell.y_pos - mob.y_pos)**2)
            if distance < player_cell.radius + mob.radius:
                game_over = True

        # Update player position
        player_cell.x_pos += round(-((mouse_x - (WIDTH/2)) / player_cell.radius/2))
        player_cell.y_pos += round(-((mouse_y - (HEIGHT/2)) / player_cell.radius/2))

        # Check if the player's score has reached 50 points
        if player_cell.radius >= 30:
            game_over = True

        # Update and draw horizontally moving mobs
        for mob in horizontal_mobs:
            mob.move()
            mob.wander()
            
            # Check for collisions with the player
            distance = math.sqrt((player_cell.x_pos - mob.x_pos)**2 + (player_cell.y_pos - mob.y_pos)**2)
            if distance < player_cell.radius + mob.radius:
                game_over = True

            mob.draw(SCREEN, mob.x_pos + player_cell.x_pos, mob.y_pos + player_cell.y_pos)

    for cell in cells:
        cell.draw(SCREEN, cell.x_pos + player_cell.x_pos, cell.y_pos + player_cell.y_pos)

    if game_over:
        if player_cell.radius >= 30:
            text = BIGFONT.render("You Win!", True, text_color)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            SCREEN.blit(text, text_rect)
        else:
            text = BIGFONT.render("You Suck", True, text_color)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            SCREEN.blit(text, text_rect)

    else:
        player_cell.draw(SCREEN, (WIDTH/2), (HEIGHT/2))
    
    text = FONT.render("Score: " + str(round(player_cell.radius)), False, text_color)
    SCREEN.blit(text, (20, 20))
    counter += 1
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.update()
    CLOCK.tick(FPS)
    SCREEN.fill(background_color)