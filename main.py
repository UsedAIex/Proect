import pygame
from random import randint

class Otobraz:
    def __init__(self):
        pygame.init()
        size = 300, 300
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Тесты")
        rects = []
        running = True
        pygame.draw.rect(screen, (0, 255, 0), (randint(1, 200), randint(1, 200), 100, 100), 0)
        while running:
            a = self.draw(screen)
            if a == False:
                break
        pygame.quit()

    def draw(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                # работает костыльно (если изменится цвет или будет изображение, оно не будет работать)
                if screen.get_at(event.pos) == pygame.Color(0, 255, 0):
                    llist = []
                    screen2 = screen
                    x, y = event.pos
                    minus_x = x - 1
                    minus_y = y - 1
                    plus_x = x + 1
                    plus_y = y + 1
                    for i in range(100):
                        if screen.get_at((minus_x, y)) == pygame.Color(0, 255, 0):
                            minus_x = x - i
                        if screen.get_at((plus_x, y)) == pygame.Color(0, 255, 0):
                            plus_x = x + i
                        if screen.get_at((x, plus_y)) == pygame.Color(0, 255, 0):
                            plus_y = y + i
                        if screen.get_at((x, minus_y)) == pygame.Color(0, 255, 0):
                            minus_y = y - i
                    minus_x -= 1
                    minus_y -= 1
                    llist.append(((minus_x, minus_y), (plus_x, minus_y)))
                    llist.append(((minus_x, minus_y), (minus_x, plus_y)))
                    llist.append(((plus_x, minus_y), (plus_x, plus_y)))
                    llist.append(((minus_x, plus_y), (plus_x, plus_y)))
                    self.draw_line(screen, llist)
                    print(minus_x, minus_y)
                    print(plus_x, minus_y)
                    print(minus_x, plus_y)
                    print(plus_x, plus_y)
                    llist.pop()
                    llist.pop()
                    llist.pop()
                    llist.pop()
            pygame.display.flip()

    def draw_line(self, screen, lst):
        for i, j in lst:
            pygame.draw.line(screen, (255, 0, 0), i, j, width=2)
            pygame.draw.line(screen, (255, 0, 0), i, j, width=2)
            pygame.draw.line(screen, (255, 0, 0), i, j, width=2)
            pygame.draw.line(screen, (255, 0, 0), i, j, width=2)


if __name__ == '__main__':
    Otobraz()

