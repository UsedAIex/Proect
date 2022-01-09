import pygame

choose_map = None
map_1 = None
map_2 = None
class Otobraz:
    def __init__(self):
        pygame.init()
        size = width, height = 800, 700
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")
        self.choose_map = choose_map
        self.map_1 = map_1
        self.map_2 = map_2

        running = True
        # Start screen
        self.draw_menu(screen, width, height)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = self.start_game_btn_coords[0]
                    y = self.start_game_btn_coords[1]
                    x1 = x + self.start_game_btn_coords[2]
                    y1 = y + self.start_game_btn_coords[3]
                    if self.map_1:
                        x_map_1 = self.map_1[0]
                        y_map_1 = self.map_1[1]
                        x1_map_1 = x_map_1 + self.map_1[2]
                        y1_map_1 = y_map_1 + self.map_1[3]
                        if x_map_1 < event.pos[0] < x1_map_1 and y_map_1 < event.pos[1] < y1_map_1:
                            self.choose_map = 'map_1'
                            draw_lvl(screen, self.choose_map, self.map_1, self.map_2)
                    if self.map_2:
                        x_map_2 = self.map_2[0]
                        y_map_2 = self.map_2[1]
                        x2_map_2 = x_map_2 + self.map_2[2]
                        y2_map_2 = y_map_2 + self.map_2[3]
                        if x_map_2 < event.pos[0] < x2_map_2 and y_map_2 < event.pos[1] < y2_map_2:
                            self.choose_map = 'map_2'
                            draw_lvl(screen, self.choose_map, self.map_1, self.map_2)
                    if x < event.pos[0] < x1 and y < event.pos[1] < y1:
                        self.start(screen)
            pygame.display.flip()



        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,
        pygame.quit()

    def start(self, screen):
        screen.fill((0, 0, 0))

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
        self.map_1 = (width - 730, height - 500, 300, 300)
        pygame.draw.rect(screen, (0, 255, 0), self.map_1, 1)
        self.map_2 = (width - 350, height - 500, 300, 300)
        pygame.draw.rect(screen, (0, 255, 0), self.map_2, 1)


def draw_lvl(screen, choose_map, map_1, map_2):
    print(map_1, map_2)
    if choose_map == 'map_1':
        pygame.draw.rect(screen, (0, 255, 0), map_1, 0)
        pygame.draw.rect(screen, (0, 255, 0), map_2, 1)
    if choose_map == 'map_2':
        pygame.draw.rect(screen, (0, 255, 0), map_1, 1)
        pygame.draw.rect(screen, (0, 255, 0), map_2, 0)
    pygame.display.flip()


if __name__ == '__main__':
    Otobraz()
