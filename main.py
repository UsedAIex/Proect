import pygame

# Задача лучше проработать классы, исправит баги в коде для стрельбы, приделать пуле картинку и добавить взрывы.


class Level:
    def __init__(self):
        self.sten = pygame.image.load('стенки.png')
        self.sten2 = pygame.image.load('стенки2.png')
        self.running = True
        self.graniz = True
        self.clock = pygame.time.Clock()
        self.x = 600
        self.y = 700
        self.speed = 0.07

    def sickl(self):
        global lastMove
        pygame.init()
        pygame.display.set_caption('Танки')
        size = width, height = 800, 800
        self.screen = pygame.display.set_mode(size)
        self.sten_verh = self.sten.get_rect(center=(332, -15))
        self.sten_niz = self.sten.get_rect(center=(332, 815))
        self.sten_left = self.sten2.get_rect(center=(-15, 355))
        self.sten_right = self.sten2.get_rect(center=(815, 355))
        self.sten_verh_dal = self.sten.get_rect(center=(532, -15))
        self.sten_niz_dal = self.sten.get_rect(center=(532, 815))
        self.sten_left_dal = self.sten2.get_rect(center=(-15, 555))
        self.sten_right_dal = self.sten2.get_rect(center=(815, 555))
        bullets = []
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.x > 20:
                self.x -= self.speed
                lastMove = 'left'
            if keys[pygame.K_RIGHT] and self.x < 731:
                self.x += self.speed
                lastMove = 'right'
            if keys[pygame.K_UP] and self.y > 20:
                self.y -= self.speed
                lastMove = 'up'
            if keys[pygame.K_DOWN] and self.y < 740:
                self.y += self.speed
                lastMove = 'down'
            self.screen.fill('white')
            pygame.draw.rect(self.screen, 'blue', (self.x, self.y, 40, 40))
            self.screen.blit(self.sten, self.sten_verh)
            self.screen.blit(self.sten, self.sten_niz)
            self.screen.blit(self.sten2, self.sten_left)
            self.screen.blit(self.sten2, self.sten_right)
            self.screen.blit(self.sten, self.sten_verh_dal)
            self.screen.blit(self.sten, self.sten_niz_dal)
            self.screen.blit(self.sten2, self.sten_left_dal)
            self.screen.blit(self.sten2, self.sten_right_dal)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    lv = Level()
    lv.sickl()
