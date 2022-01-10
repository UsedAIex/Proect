import pygame

# Задача лучше проработать классы, исправит баги в коде для стрельбы, приделать пуле картинку и добавить взрывы.
lastMove = 'up'
bullet_img = pygame.image.load('snaryd.png')


class Bullet:
    def __init__(self, x, y):
        self.x_bul = x
        self.y_bul = y
        self.speed_bul = 8

    def move(self):
        global lastMove
        if lastMove == 'up':
            if self.x_bul > 20 and self.y_bul < 740:
                self.y_bul += self.speed_bul
                screen.blit(bullet_img, (self.x_bul, self.y_bul))
                return True


        elif lastMove == 'down':
            if self.y_bul > 20 and self.y_bul < 740:
                self.y_bul -= self.speed_bul
                screen.blit(bullet_img, (self.x_bul, self.y_bul))
                return True

        elif lastMove == 'left':
            if self.x_bul > 20 and self.y_bul < 740:
                self.x_bul -= self.speed_bul
                screen.blit(bullet_img, (self.x_bul, self.y_bul))
                return True

        elif lastMove == 'right':
            if self.x_bul > 20 and self.y_bul < 731:
                self.x_bul += self.speed_bul
                screen.blit(bullet_img, (self.x_bul, self.y_bul))
                return True

        else:
            return False


class Level(Bullet):
    def __init__(self, screen):
        super(Bullet, self).__init__()
        self.sten = pygame.image.load('стенки.png')
        self.sten2 = pygame.image.load('стенки2.png')
        self.running = True
        self.graniz = True
        self.clock = pygame.time.Clock()
        self.x = 500
        self.y = 700
        self.speed = 0.1
        self.screen = screen

    def sickl(self):
        global lastMove
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
            if keys[pygame.K_x]:
                bullets.append(Bullet(self.x, self.y))

            for bullet in bullets:
                if not bullet.move():
                    bullets.remove(bullet)

            if keys[pygame.K_LEFT] and self.x > 20:
                if keys[pygame.K_LEFT] and not keys[pygame.K_UP]:
                    if keys[pygame.K_LEFT] and not keys[pygame.K_UP]:
                        self.x -= self.speed
                        lastMove = 'left'

            if keys[pygame.K_RIGHT] and self.x < 731:
                if keys[pygame.K_RIGHT] and not keys[pygame.K_UP]:
                    if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]:
                        self.x += self.speed
                        lastMove = 'right'

            if keys[pygame.K_UP] and self.y > 20:
                self.y -= self.speed
                lastMove = 'up'

            if keys[pygame.K_DOWN] and self.y < 740:
                if keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:
                    if keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
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
    pygame.init()
    pygame.display.set_caption('Танки')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    lv = Level(screen)
    lv.sickl()
