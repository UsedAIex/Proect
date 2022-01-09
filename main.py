import pygame


class Otobraz:
    def __init__(self):
        pygame.init()
        size = width, height = 800, 700
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")

        running = True
        # Start screen
        self.draw_to_level_1(screen, width, height)
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = self.start_game_btn_coords[0]
                    y = self.start_game_btn_coords[1]
                    x1 = x + self.start_game_btn_coords[2]
                    y1 = y + self.start_game_btn_coords[3]
                    if x < event.pos[0] < x1 and y < event.pos[1] < y1:
                        self.start(screen)



        # First level screen
        # обновляешь экран, формируешь новую картинку, новый игровой цикл,
        pygame.quit()

    def start(self, screen):
        screen.fill((0, 0, 0))

    def draw_to_level_1(self, screen, width, height):
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


if __name__ == '__main__':
    Otobraz()
