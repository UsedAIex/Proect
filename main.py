import pygame

choose_map = None
map_1 = None
map_2 = None
pygame.init()


class Otobraz:
    def __init__(self):

        size = width, height = 800, 700
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")
        self.choose_map = choose_map
        self.map_1_size = None
        self.map_2_size = None


        # Start screen
        self.draw_menu(screen, width, height)
        self.game(screen)

    def game(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                            print(12345)
                        # self.start(screen, self.choose_map)
            pygame.display.flip()

        pygame.quit()

        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,

    def error(self, screen, width, height):
        font = pygame.font.Font(None, 50)
        text = font.render("Вы не выбрали карту", True, (255, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        screen.blit(text, (text_x, 520))

    def draw_menu(self, screen, width, height):
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

class Play:
    def __init__(self, screen, size_map_1, size_map_2, chosen_map):
        self.size_map_1 = size_map_1
        self.size_map_2 = size_map_2
        self.ch_map = chosen_map

if __name__ == '__main__':
    Otobraz()
