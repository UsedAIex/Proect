import pygame
import sys
import os

choose_map = None
map_1 = None
map_2 = None
pygame.init()

def terminate():
    pygame.quit()
    sys.exit()

def load_level(filename):
    fullname = os.path.join(filename)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с картой '{fullname}' не найден")
        terminate()
    # читаем уровень, убирая символы перевода строки
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    return image

def generate_level(level):
    new_player1, new_player2, x, y = None, None, None, None
    players = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player1, new_player2, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Otobraz:
    def __init__(self):

        size = width, height = 800, 800
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")
        self.choose_map = choose_map
        self.map_1_size = None
        self.map_2_size = None


        # Start screen
        self.draw_menu(screen, width, height)
        self.game(screen, width, height)

    def game(self, screen, width, height):
        game_start = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = self.start_game_btn_coords[0]
                    y = self.start_game_btn_coords[1]
                    x1 = x + self.start_game_btn_coords[2]
                    y1 = y + self.start_game_btn_coords[3]
                    if self.map_1_size:
                        x_map_1 = self.map_1_size[0]
                        y_map_1 = self.map_1_size[1]
                        x1_map_1 = x_map_1 + self.map_1_size[2]
                        y1_map_1 = y_map_1 + self.map_1_size[3]
                        if x_map_1 < event.pos[0] < x1_map_1 and y_map_1 < event.pos[1] < y1_map_1:
                            self.choose_map = 'map_1'
                            draw_lvl(screen, self.choose_map, self.map_1_size, self.map_2_size)
                    if self.map_2_size:
                        x_map_2 = self.map_2_size[0]
                        y_map_2 = self.map_2_size[1]
                        x2_map_2 = x_map_2 + self.map_2_size[2]
                        y2_map_2 = y_map_2 + self.map_2_size[3]
                        if x_map_2 < event.pos[0] < x2_map_2 and y_map_2 < event.pos[1] < y2_map_2:
                            self.choose_map = 'map_2'
                            draw_lvl(screen, self.choose_map, self.map_1_size, self.map_2_size)
                    if x < event.pos[0] < x1 and y < event.pos[1] < y1:
                        if not self.choose_map:
                            self.error(screen, width, height)
                        else:
                            main(screen, self.choose_map)
                            game_start = True
                            break

            pygame.display.flip()
            if game_start:
                break


        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,

    def error(self, screen, width, height):
        font = pygame.font.Font(None, 50)
        text = font.render("Вы не выбрали карту", True, (255, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_x = width // 2 - text.get_width() // 2
        screen.blit(text, (text_x, height - 180))

    def draw_menu(self, screen, width, height):
        print(234)
        font = pygame.font.Font(None, 50)
        text = font.render("Танчики", True, (100, 255, 100))
        text_start = font.render("Играть", True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_x_start = width // 2 - text_start.get_width() // 2
        text_y = height - 105 - text_start.get_height() // 2
        text_w = text_start.get_width()
        text_h = text_start.get_height()
        screen.blit(text, (text_x, 100))
        screen.blit(text_start, (text_x_start, screen.get_height() - 120))
        self.start_game_btn_coords = (text_x_start - 10, text_y - 10,
                                      text_w + 20, text_h + 20)
        pygame.draw.rect(screen, (0, 255, 0), self.start_game_btn_coords, 1)
        self.map_1_size = (width - 730, height - 500, 300, 300)
        pygame.draw.rect(screen, (0, 255, 0), self.map_1_size, 1)
        self.map_2_size = (width - 350, height - 500, 300, 300)
        pygame.draw.rect(screen, (0, 255, 0), self.map_2_size, 1)


def draw_lvl(screen, choose_maps, maps_1, maps_2):
    if choose_maps == 'map_1':
        print(maps_1, map_1)
        pygame.draw.rect(screen, (0, 255, 0), maps_1, 0)
        pygame.draw.rect(screen, (0, 0, 0), maps_2, 0)
        pygame.draw.rect(screen, (0, 255, 0), maps_2, 1)
    if choose_maps == 'map_2':
        pygame.draw.rect(screen, (0, 0, 0), maps_1, 0)
        pygame.draw.rect(screen, (0, 255, 0), maps_1, 1)
        pygame.draw.rect(screen, (0, 255, 0), maps_2, 0)
    pygame.display.flip()


def main(screen, maps):
    clock = pygame.time.Clock()
    if maps == 'map_1':
        player1, player2, level_x, level_y = generate_level(load_level('map.txt'))
    else:
        player1, player2, level_x, level_y = generate_level(load_level('map2.txt'))
    while True:
        screen.fill(pygame.Color("green"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        # изменяем ракурс камеры
        # обновляем положение всех спрайтов
        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


FPS = 50
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png')
}

tile_width = tile_height = 50

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

if __name__ == '__main__':
    Otobraz()