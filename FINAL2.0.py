import pygame
import button
from pyvidplayer import Video
import random
import csv
pygame.init()

WIDTH = 1280
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer')

# some game variables
ROWS = 23
COLS = 40
tile_size = 32
game_over = 0
tile_types = 7
clock = pygame.time.Clock()
fps = 60
level = 0

# load images
flyer_img = pygame.image.load("assets//Terrain//Terrain2.png").convert_alpha()
ground_img = pygame.image.load("assets//Terrain//Ground.png").convert_alpha()
grass_img = pygame.image.load("assets//Terrain//Grass.png").convert_alpha()
resume_img = pygame.image.load("assets//Menu//Buttons//Resume_final.png").convert_alpha()
quit_img = pygame.image.load("assets//Menu//Buttons//quit_final.png").convert_alpha()
settings_img = pygame.image.load("assets//Menu//Buttons//settings_final.png").convert_alpha()
button_gr_img = pygame.image.load("assets//Menu//Buttons//Button_blank_green.png").convert_alpha()
main_menu_bg = pygame.image.load("assets//Menu//forest_bg.png").convert_alpha()
new_game_img = pygame.image.load("assets//Menu//Buttons//new_game_final.png").convert_alpha()
skip_intro = pygame.image.load("assets//Other//skip_intro.png").convert_alpha()
spike1_img = pygame.image.load("assets//Enemies//spike1.png").convert_alpha()
spike2_img = pygame.image.load("assets//Enemies//spike2.png").convert_alpha()
spike3_img = pygame.image.load("assets//Enemies//spike3.png").convert_alpha()
spike4_img = pygame.image.load("assets//Enemies//spike4.png").convert_alpha()

# create buttons
blank_button = button.Button(WIDTH // 2 - 368 // 2, HEIGHT // 2 - 250, button_gr_img, 8)
blank_button2 = button.Button(WIDTH // 2 - 368 // 2, HEIGHT // 2 - 75, button_gr_img, 8)
blank_button3 = button.Button(WIDTH // 2 - 368 // 2, HEIGHT // 2 + 100, button_gr_img, 8)
resume_button = button.Button(WIDTH // 2 - 230 // 2, HEIGHT // 2 - 230, resume_img, 0.2)
quit_button = button.Button(WIDTH // 2 - 125 // 2, HEIGHT // 2 + 117, quit_img, 0.16)
settings_button = button.Button(WIDTH // 2 - 200 // 2, HEIGHT // 2 - 63, settings_img, 0.15)
new_game_button = button.Button(WIDTH // 2 - 253 // 2, HEIGHT // 2 - 230, new_game_img, 0.15)
skip_intro_button = button.Button(774, HEIGHT - 50, skip_intro, 0.25)

# main menu
def main_menu(window):
    while True:
        window.blit(main_menu_bg, (0, 0))
        if blank_button.draw(window):
            intro(window)
        if new_game_button.draw(window):
            intro(window)
        if blank_button2.draw(window):
            settings_menu(window)
        if settings_button.draw(window):
            settings_menu(window)
        if blank_button3.draw(window):
            pygame.quit()
        if quit_button.draw(window):
            pygame.quit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
# settings menu
def settings_menu(window):
    pass
# video intro at the start of the game
def intro(window):
    vid = Video("assets//Other//Intro.mov")
    vid.set_size((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)
        skip_intro_button.draw(window)
        pygame.display.update()
        vid.draw(window, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                main(window, game_over)
            if event.type == pygame.K_RETURN:
                vid.close()
                main(window, game_over)
            if event.type == pygame.K_SPACE:
                vid.close()
                main(window, game_over)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
# main character
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        # player controls
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check head collision
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check feet collision
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            # check for collision with spikes
            if pygame.sprite.spritecollide(self, spike1_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, spike2_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, spike3_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, spike4_group, False):
                game_over = -1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        # draw player onto screen
        window.blit(self.image, self.rect)

        return game_over

    # create player
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'assets//MainCharacters//guy{num}.png')
            img_right = pygame.transform.scale(img_right, (tile_size, tile_size * 2))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
# world
class World():
    # appends blocks to numbers
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    img = pygame.transform.scale(ground_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 1:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(flyer_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    spike1 = Spike_Up(col_count * tile_size, row_count * tile_size)
                    spike1_group.add(spike1)
                if tile == 4:
                    spike2 = Spike_Right(col_count * tile_size, row_count * tile_size)
                    spike2_group.add(spike2)
                if tile == 5:
                    spike3 = Spike_Down(col_count * tile_size, row_count * tile_size)
                    spike3_group.add(spike3)
                if tile == 6:
                    spike4 = Spike_Left(col_count * tile_size, row_count * tile_size)
                    spike4_group.add(spike4)
                if tile == 7:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                col_count += 1
            row_count += 1
    # draw blocks onto screen
    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])
# moving enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets//Enemies//blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
# stationary enemies
class Spike_Up(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spike1_img
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Spike_Right(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spike2_img
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Spike_Down(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spike3_img
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Spike_Left(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = spike4_img
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,5,5,5,5,0,0,0,5,5,5,-1,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,5,5,5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,3,3,1,1,-1,-1,-1,-1,-1,-1,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,3,0,0,0,-1,-1,-1,-1,-1,-1,1,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,-1,3,3,0,0,0,0,-1,-1,-1,-1,1,1,0,0,0],
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,3,3,3,0,0,0,0,-1,-1,-1,-1,-1,1,0,0,0,0,0],
[0,2,2,2,-1,-1,-1,-1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,3,3,0,0,0,0,0,0,-1,-1,-1,-1,-1,1,0,-1,-1,-1,-1,-1],
[0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,3,3,3,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,-1,-1,-1],
[0,0,0,0,3,3,3,3,3,3,3,-1,-1,-1,3,3,3,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,4,-1,-1,-1,-1,-1],
[0,0,0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,0,0,1,-1,-1,-1,2],
[0,0,0,0,0,0,5,5,5,5,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,4,-1,-1,-1,-1,0],
[0,0,0,5,5,5,-1,-1,-1,-1,5,5,5,0,0,0,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,0,0,4,-1,-1,-1,-1,0],
[0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0,1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,0,0,0,4,-1,-1,-1,-1,-1,0],
[0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0,1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,5,0,4,-1,-1,-1,1,1,0],
[0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0,1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0],
[0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0,0,1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0],
[0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0,0,0,1,1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
]

player = Player(tile_size + 15, 7 * tile_size)

blob_group = pygame.sprite.Group()
spike1_group = pygame.sprite.Group()
spike2_group = pygame.sprite.Group()
spike3_group = pygame.sprite.Group()
spike4_group = pygame.sprite.Group()

world = World(world_data)

# create background
scroll = 0
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"assets//Background//plx{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(5):
        speed = 1
        for i in bg_images:
            window.blit(i, ((x * bg_width) - scroll * speed / 5, 0))
            window.blit(i, ((- x * bg_width) - scroll * speed / 5, 0))
            speed += 0.2
# screen shake when player dies
def shake_screen():
    shake_intensity = 2  # The maximum angle of rotation
    shake_duration = 1  # The duration of the shake in milliseconds
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < shake_duration:
        angle = random.randint(-shake_intensity, shake_intensity)
        if angle == 0:
            angle = 1
        rotated_screen = pygame.transform.rotate(window, angle)
        window.blit(rotated_screen, (0, 0))
        pygame.display.flip()
# main game loop
def main(window, game_over):
    fade_alpha = 20
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(fade_alpha)
    fade_surface.fill((0, 0, 0))
    game_on = True
    fade_counter = -WIDTH + 500
    BLACK = (0, 0, 0)
    shake_counter = 0

    run = True
    while run:
        clock.tick(fps)

        if game_on == True:
            fade_alpha /= 100
            draw_bg()
            world.draw()
            blob_group.draw(window)
            spike1_group.draw(window)
            spike2_group.draw(window)
            spike3_group.draw(window)
            spike4_group.draw(window)
            game_over = player.update(game_over)
            blob_group.update()
        else:
            if fade_alpha < 75:
                window.blit(fade_surface, (0, 0))
            if blank_button.draw(window):
                game_on = True
            if resume_button.draw(window):
                game_on = True
            if blank_button2.draw(window):
                pass
            if settings_button.draw(window):
                pass
            if blank_button3.draw(window):
                run = False
                break
            if quit_button.draw(window):
                run = False
                break
            fade_alpha += 5
            pygame.display.update()

        # if player has died
        if game_over == -1:
            if shake_counter < 2:
                shake_screen()
            if fade_counter < WIDTH:
                fade_counter += 50
            pygame.draw.rect(window, BLACK, (fade_counter, 0, WIDTH - 400, HEIGHT))
            player.reset(tile_size, HEIGHT - 14 * tile_size)
            shake_counter += 1
            if fade_counter > WIDTH:
                game_over = 0
                fade_counter = 400 - WIDTH
                shake_counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main_menu(window)