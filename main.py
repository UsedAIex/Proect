import os
import sys
import time

import pygame

from bd_file import Help_db

pygame.init()
hits = None
FPS = 10
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# helper = None
helper = Help_db()

all_sprites = pygame.sprite.Group()
green_tank = pygame.sprite.Group()
blue_tank = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()


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
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    # вернем игрока, а также размер поля в клетках
    return x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            super().__init__(wall_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, lastMove, color="green"):
        if color == "green":
            super().__init__(all_sprites, green_tank)
            self.group = green_tank
        else:
            super().__init__(all_sprites, blue_tank)
            self.group = blue_tank
        super().__init__(tiles_group, all_sprites)
        self.tiles_group = tiles_group
        self.speed = 5
        self.lastMove = lastMove
        self.set_images(color)
        self.set_image()
        self.update_image()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(x, y)
        self.rect.centerx = self.rect.x
        self.rect.bottom = self.rect.y
        self.next_wall = None

    def set_images(self, color):
        if color == "green":
            self.images_up = [
                load_image("tank1.png", -1), load_image("tank2.png", -1), load_image("tank3.png", -1),
                load_image("tank4.png", -1), load_image("tank5.png", -1), load_image("tank6.png", -1),
                load_image("tank7.png", -1), load_image("tank8.png", -1),
            ]
            self.images_right = [
                load_image('tank_right1.png', -1), load_image('tank_right2.png', -1), load_image('tank_right3.png', -1),
                load_image('tank_right4.png', -1), load_image('tank_right5.png', -1),
                load_image('tank_right6.png', -1), load_image('tank_right7.png', -1), load_image('tank_right8.png', -1)]
            self.images_left = [load_image('tank_laft1.png', -1), load_image('tank_laft2.png', -1),
                                load_image('tank_laft3.png', -1),
                                load_image('tank_laft4.png', -1), load_image('tank_laft5.png', -1),
                                load_image('tank_laft6.png', -1),
                                load_image('tank_laft7.png', -1), load_image('tank_laft8.png', -1)]
            self.images_down = [load_image('tank_back1.png', -1), load_image('tank_back2.png', -1),
                                load_image('tank_back3.png', -1),
                                load_image('tank_back4.png', -1), load_image('tank_back5.png', -1),
                                load_image('tank_back6.png', -1),
                                load_image('tank_back7.png', -1), load_image('tank_back8.png', -1)]
        else:
            self.images_down = [load_image('tank_blue1.png', -1), load_image('tank_blue2.png', -1),
                                load_image('tank_blue3.png', -1),
                                load_image('tank_blue4.png', -1), load_image('tank_blue5.png', -1),
                                load_image('tank_blue6.png', -1),
                                load_image('tank_blue7.png', -1), load_image('tank_blue8.png', -1)]
            self.images_up = [load_image('tank_blue_back1.png', -1), load_image('tank_blue_back2.png', -1),
                              load_image('tank_blue_back3.png', -1),
                              load_image('tank_blue_back4.png', -1), load_image('tank_blue_back5.png'),
                              load_image('tank_blue_back6.png', -1),
                              load_image('tank_blue_back7.png', -1), load_image('tank_blue_back8.png', -1)]
            self.images_left = [load_image('tank_blue_laft1.png', -1), load_image('tank_blue_laft2.png', -1),
                                load_image('tank_blue_laft3.png', -1), load_image('tank_blue_laft4.png', -1),
                                load_image('tank_blue_laft5.png', -1), load_image('tank_blue_laft6.png', -1),
                                load_image('tank_blue_laft7.png', -1), load_image('tank_blue_laft8.png', -1)]
            self.images_right = [load_image('tank_blue_right1.png', -1), load_image('tank_blue_right2.png', -1),
                                 load_image('tank_blue_right3.png', -1), load_image('tank_blue_right4.png', -1),
                                 load_image('tank_blue_right5.png', -1), load_image('tank_blue_right6.png', -1),
                                 load_image('tank_blue_right7.png', -1), load_image('tank_blue_right8.png', -1)]

    def set_image(self):
        self.count = 0
        self.image = self.images_up[self.count % len(self.images_up)]
        self.direction = "up"

    def update_image(self):
        if self.direction == "up":
            self.image = self.images_up[self.count % len(self.images_up)]
        elif self.direction == "down":
            self.image = self.images_down[self.count % len(self.images_down)]
        elif self.direction == "left":
            self.image = self.images_left[self.count % len(self.images_left)]
        elif self.direction == "right":
            self.image = self.images_right[self.count % len(self.images_right)]
        elif self.direction == "stop":
            if self.lastMove == 'up':
                self.image = self.images_up[0]

            elif self.lastMove == 'left':
                self.image = self.images_left[0]

            elif self.lastMove == 'right':
                self.image = self.images_right[0]
            elif self.lastMove == 'down':
                self.image = self.images_down[0]
        self.count += 1

    def update(self):
        self.update_image()

    def move(self, direction, lastMove):
        self.direction = direction
        self.lastMove = lastMove
        if not self.next_wall:
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "stop":
                self.rect.x += 0
                self.rect.y += 0
            self.colision()

    def shot(self, color='green'):
        if self.lastMove == 'up':
            bullet = Bullet(self.rect.centerx, self.rect.top, self.lastMove, color)
        elif self.lastMove == 'down':
            bullet = Bullet(self.rect.centerx, self.rect.bottom + 10, self.lastMove, color)
        elif self.lastMove == 'left':
            bullet = Bullet(self.rect.topleft[0] - 10, self.rect.topleft[1] + 35, self.lastMove, color)
        elif self.lastMove == 'right':
            bullet = Bullet(self.rect.topright[0] + 15, self.rect.topright[1] + 35, self.lastMove, color)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def colision(self):
        another_tank = pygame.sprite.spritecollideany(self,
                                                      blue_tank if self.group == green_tank else green_tank)
        wall = pygame.sprite.spritecollideany(self, wall_group)
        if another_tank or wall:
            if self.direction == "up":
                self.rect.y += self.speed
            elif self.direction == "down":
                self.rect.y -= self.speed
            elif self.direction == "left":
                self.rect.x += self.speed
            elif self.direction == "right":
                self.rect.x -= self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, lastMove, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill('YELLOW')
        self.color = color
        self.rect = self.image.get_rect()
        self.lastMove = lastMove
        self.rect.bottom = y
        self.rect.centerx = x
        if lastMove == 'up':
            self.speedx = 0
            self.speedy = -10
        elif lastMove == 'down':
            self.speedx = 0
            self.speedy = 10
        elif lastMove == 'left':
            self.speedx = -10
            self.speedy = 0
        elif lastMove == 'right':
            self.speedx = 10
            self.speedy = 0

    def update(self):
        global blue_bulletss
        global green_bulletss
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.color == 'green':
            if pygame.sprite.spritecollideany(self, wall_group):
                self.kill()
                green_bulletss += 1
            if self.rect.bottom < 0:
                self.kill()
                green_bulletss += 1
            if self.rect.bottom > 800:
                self.kill()
                green_bulletss += 1
            if self.rect.left > 800:
                self.kill()
                green_bulletss += 1
            if self.rect.left < 0:
                self.kill()
                green_bulletss += 1
        elif self.color == 'blue':
            if pygame.sprite.spritecollideany(self, wall_group):
                self.kill()
                blue_bulletss += 1
            if self.rect.bottom < 0:
                self.kill()
                blue_bulletss += 1
            if self.rect.bottom > 800:
                self.kill()
                blue_bulletss += 1
            if self.rect.left > 800:
                self.kill()
                blue_bulletss += 1
            if self.rect.left < 0:
                self.kill()
                blue_bulletss += 1


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png')
}

tile_width = tile_height = 50

# группы спрайтов


blue_bulletss = 4
green_bulletss = 4

pygame.init()
choose_map = None
sprite = pygame.sprite.Sprite()


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
                        if (self.cleat[0] < event.pos[0] < self.cleat[2] + self.cleat[0] and
                                self.cleat[1] < event.pos[1] < self.cleat[3] + self.cleat[1]):
                            helper.delete_db()
                            self.draw_list(width, height)
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
        screen.blit(txt_back, (25, 45))
        self.list_fight = (txt_back.get_width() - 60, txt_back.get_height() + 10,
                           txt_back.get_width() + 20, txt_back.get_height() + 20)
        pygame.draw.rect(screen, (255, 255, 0), self.list_fight, 1)
        x = txt_back.get_width() * 2 - 40
        pygame.draw.rect(screen, (255, 255, 0), (x, 80, width - x * 2, height - 160), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 160), (width - x, 160), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 240), (width - x, 240), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 320), (width - x, 320), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 400), (width - x, 400), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 480), (width - x, 480), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 560), (width - x, 560), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 640), (width - x, 640), 1)
        pygame.draw.line(screen, (255, 255, 0), (x, 720), (width - x, 720), 1)
        pygame.draw.line(screen, (255, 255, 0), (x + 280, 80), (x + 280, 720), 1)
        pygame.draw.line(screen, (255, 255, 0), (x + 280, 80), (x + 280, 720), 1)
        pygame.draw.line(screen, (255, 255, 0), (x + 430, 80), (x + 430, 720), 1)
        txt_1 = font_txt.render('Победитель', True, (255, 255, 100))
        screen.blit(txt_1, (255 - txt_1.get_width() / 2, 110))
        txt_2 = font_txt.render('Время игры', True, (255, 255, 100))
        screen.blit(txt_2, (395, 110))
        txt_3 = font_txt.render('Кол-во', True, (255, 255, 100))
        screen.blit(txt_3, (570, 97))
        txt_4 = font_txt.render('выстрелов', True, (255, 255, 100))
        screen.blit(txt_4, (550, 123))
        self.back_work = True
        data = helper.vivod()
        count = 0
        for i in data[::-1]:
            if count == 7:
                break
            txt = font_txt.render(str(i[3]), True, (255, 255, 100))
            screen.blit(txt, (240, count * 80 + 190))
            txt = font_txt.render(str(i[1]), True, (255, 255, 100))
            screen.blit(txt, (490 - txt.get_width(), count * 80 + 190))
            txt = font_txt.render(str(i[2]), True, (255, 255, 100))
            screen.blit(txt, (620 - txt.get_width(), count * 80 + 190))
            count += 1
        txt_clear = font_txt.render('Очистить историю', True, (255, 255, 100))
        screen.blit(txt_clear, (width - 250, height - 45))
        self.cleat = (800 - txt_clear.get_width() - 35, 800 - txt_clear.get_height() - 30,
                           txt_clear.get_width() + 20, txt_clear.get_height() + 20)
        pygame.draw.rect(screen, (255, 255, 0), self.cleat, 1)
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


class Final_menu:
    def __init__(self, times, bullet, winner='12'):
        size = width, height = 800, 800
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")
        times = times[:4]
        self.game(screen, width, height, winner, times, bullet)

        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,

    def game(self, screen, width, height, winner, time, bullet):
        self.draw_menu(screen, width, height, winner, time, bullet)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.list_fight[0] < event.pos[0] < self.list_fight[2] + self.list_fight[0] and
                            self.list_fight[1] < event.pos[1] < self.list_fight[3] + self.list_fight[1]):
                        Otobraz()
            pygame.display.flip()

    def draw_menu(self, screen, width, height, winner, time, bullet):
        helper.add_db(time, bullet, winner)
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 50)
        font_text = pygame.font.Font(None, 35)
        text = font.render("Игра окончена", True, (255, 255, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - 280
        text_winner = font_text.render('Выиграл: ' + winner, True, (255, 255, 0))
        x_win = width // 2 - text_winner.get_width() // 2
        y_win = height // 2 - 190
        text_time = font_text.render('Время боя: ' + time, True, (255, 255, 0))
        x_time = width // 2 - text.get_width() // 2 - 200
        y_time = height // 2 - 100
        text_bullet = font_text.render('Количество выстрелов: ' + bullet, True, (255, 255, 0))
        x_bullet = width // 2 - text.get_width() // 2 - 200
        y_bullet = height // 2 - 10
        screen.blit(text, (text_x, text_y))
        screen.blit(text_winner, (x_win, y_win))
        screen.blit(text_time, (x_time, y_time))
        screen.blit(text_bullet, (x_bullet, y_bullet))
        txt_back = font.render('В меню', True, (255, 255, 100))
        screen.blit(txt_back, (57, 60))
        self.list_fight = (txt_back.get_width() - 80, txt_back.get_height() + 15,
                           txt_back.get_width() + 20, txt_back.get_height() + 20)
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
    tit1 = time.time()
    global wall_group
    global blue_bulletss
    global green_bulletss
    clock = pygame.time.Clock()
    lastMove_blue = 'down'
    lastMove_green = 'up'
    running = True
    col_bullets_for_play = 0
    if maps == 'map_1':
        level_x, level_y = generate_level(load_level('../map.txt'))
        dragon = AnimatedSprite(375, 750, lastMove_green)
        dragon2 = AnimatedSprite(425, 108, lastMove_blue, color="blue")
    else:
        level_x, level_y = generate_level(load_level('../map2.txt'))
        dragon = AnimatedSprite(725, 750, lastMove_green)
        dragon2 = AnimatedSprite(75, 108, lastMove_blue, color="blue")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    if green_bulletss > 0:
                        green_bulletss -= 1
                        col_bullets_for_play += 1
                        dragon.shot(color='green')

                elif event.key == pygame.K_m:
                    if blue_bulletss > 0:
                        blue_bulletss -= 1
                        col_bullets_for_play += 1
                        dragon2.shot(color='blue')

        hits = pygame.sprite.groupcollide(blue_tank, bullets, True, True)
        hit = pygame.sprite.groupcollide(green_tank, bullets, True, True)

        if hits or hit:
            blue_bulletss = 4
            green_bulletss = 4
            tit2 = time.time()
            wall_group = pygame.sprite.Group()
            Final_menu(str(tit2 - tit1), str(col_bullets_for_play))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            lastMove_green = 'up'
            dragon.move("up", lastMove_green)

        elif keys[pygame.K_DOWN]:
            lastMove_green = 'down'
            dragon.move("down", lastMove_green)

        elif keys[pygame.K_LEFT]:
            lastMove_green = 'left'
            dragon.move("left", lastMove_green)

        elif keys[pygame.K_RIGHT]:
            lastMove_green = 'right'
            dragon.move("right", lastMove_green)

        elif not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                dragon.move("stop", lastMove_green)

        if keys[pygame.K_w]:
            lastMove_blue = 'up'
            dragon2.move("up", lastMove_blue)

        elif keys[pygame.K_s]:
            lastMove_blue = 'down'
            dragon2.move("down", lastMove_blue)

        elif keys[pygame.K_a]:
            lastMove_blue = 'left'
            dragon2.move("left", lastMove_blue)

        elif keys[pygame.K_d]:
            lastMove_blue = 'right'
            dragon2.move("right", lastMove_blue)

        elif not keys[pygame.K_w] and not keys[pygame.K_s]:
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                dragon2.move("stop", lastMove_blue)

        all_sprites.update()
        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
        # screen.blit(player_1, (player1[0] * 50, player1[1] * 50))
        # screen.blit(player_2, (player2[0] * 50, player2[1] * 50 - 10))


screen = pygame.display.set_mode((800, 800))

background = load_image('menu.png')
map_1_ig = load_image('map_one_image.png')
map_2_ig = load_image('map_two_image.png')

player_group = pygame.sprite.Group()

if __name__ == '__main__':
    Otobraz()
