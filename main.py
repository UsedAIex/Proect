import os
import sys

import pygame

pygame.init()

choose_map = None
sprite = pygame.sprite.Sprite()


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


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
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
            elif level[y][x] == '@':
                Tile('empty', x, y)
                players.append((x, y))
    new_player1 = players[0]
    new_player2 = players[1]
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
        pygame.display.set_caption("Тесты")
        self.choose_map = choose_map
        self.map_1_size = None
        self.map_2_size = None
        self.back_work = None

        # Start screen
        self.draw_menu(width, height)
        self.game(screen, width, height)

    def game(self, screen, width, height):
        game_start = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_work:
                        if (self.list_fight[0] < event.pos[0] < self.list_fight[2] + self.list_fight[0] and
                                self.list_fight[1] < event.pos[1] < self.list_fight[3] + self.list_fight[1]):
                            self.draw_menu(width, height)
                            draw_lvl(screen, self.choose_map, self.map_1_size, self.map_2_size)
                            self.back_work = None
                    else:
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
                        if (self.list_fight[0] < event.pos[0] < self.list_fight[2] + self.list_fight[0] and
                                self.list_fight[1] < event.pos[1] < self.list_fight[3] + self.list_fight[1]):
                            self.draw_list(width, height)

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


    def draw_list(self, width, height):
        screen.blit(background, (0, 0))
        font_txt = pygame.font.Font(None, 35)
        screen.blit(background, (0, 0))
        txt_back = font_txt.render('Назад', True, (255, 255, 100))
        screen.blit(txt_back, (25, 50))
        self.list_fight = (txt_back.get_width() - 60, txt_back.get_height() + 15,
                           txt_back.get_width() + 20, txt_back.get_height() + 20)
        pygame.draw.rect(screen, (255, 255, 0), self.list_fight, 1)
        self.back_work = True


        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,

    def error(self, screen, width, height):
        font = pygame.font.Font(None, 50)
        text = font.render("Вы не выбрали карту", True, (255, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        screen.blit(text, (text_x, height - 230))

    def draw_menu(self, width, height):
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 50)
        font_txt = pygame.font.Font(None, 35)
        text = font.render("Танчики", True, (255, 255, 100))
        text_start = font.render("Играть", True, (255, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_x_start = width // 2 - text_start.get_width() // 2
        text_y = height - 155 - text_start.get_height() // 2
        text_w = text_start.get_width()
        text_h = text_start.get_height()
        screen.blit(text, (text_x, 100))
        screen.blit(text_start, (text_x_start, screen.get_height() - 170))
        self.start_game_btn_coords = (text_x_start - 10, text_y - 10,
                                      text_w + 20, text_h + 20)
        pygame.draw.rect(screen, (255, 255, 0), self.start_game_btn_coords, 1)
        self.map_1_size = (width - 731, height - 600, 303, 300)
        pygame.draw.rect(screen, (0, 0, 0), self.map_1_size, 0)
        screen.blit(map_1_ig, (width - 727, height - 596))
        self.map_2_size = (width - 351, height - 600, 303, 300)
        pygame.draw.rect(screen, (0, 0, 0), self.map_2_size, 0)
        screen.blit(map_2_ig, (width - 347, height - 596))
        txt_fight = font_txt.render('Данные боя', True, (255, 255, 100))
        screen.blit(txt_fight, (width // 2 - txt_fight.get_width() // 2, height - 100))
        self.list_fight = (width // 2 - txt_fight.get_width() // 2 - 10, height - 110,
                           txt_fight.get_width() + 20, txt_fight.get_height() + 20)
        pygame.draw.rect(screen, (255, 255, 0), self.list_fight, 1)


def draw_lvl(screen, choose_maps, maps_1, maps_2):
    if choose_maps:
        if choose_maps == 'map_1':
            pygame.draw.rect(screen, (255, 0, 0), maps_1, 0)
            pygame.draw.rect(screen, (0, 0, 0), maps_2, 0)
            pygame.draw.rect(screen, (0, 0, 0), maps_2, 0)
            screen.blit(map_1_ig, (800 - 727, 800 - 596))
            screen.blit(map_2_ig, (800 - 347, 800 - 596))
        if choose_maps == 'map_2':
            pygame.draw.rect(screen, (0, 0, 0), maps_1, 0)
            pygame.draw.rect(screen, (0, 0, 0), maps_1, 1)
            pygame.draw.rect(screen, (255, 0, 0), maps_2, 0)
            screen.blit(map_1_ig, (800 - 727, 800 - 596))
            screen.blit(map_2_ig, (800 - 347, 800 - 596))
        pygame.display.flip()


def main(screen, maps):
    clock = pygame.time.Clock()
    if maps == 'map_1':
        player1, player2, level_x, level_y = generate_level(load_level('map.txt'))
    else:
        player1, player2, level_x, level_y = generate_level(load_level('map2.txt'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        # изменяем ракурс камеры
        # обновляем положение всех спрайтов
        all_sprites.draw(screen)
        screen.blit(player_1, (player1[0] * 50, player1[1] * 50))
        screen.blit(player_2, (player2[0] * 50, player2[1] * 50 - 10))
        clock.tick(FPS)
        pygame.display.flip()


FPS = 50
screen = pygame.display.set_mode((800, 800))
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png')
}
player_1 = load_image('blue_tank.png', -1)
player_2 = load_image('green_tank.png', -1)

tile_width = tile_height = 50
background = load_image('menu.png')
map_1_ig = load_image('map_one_image.png')
map_2_ig = load_image('map_two_image.png')
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

if __name__ == '__main__':
    Otobraz()
