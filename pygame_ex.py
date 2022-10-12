import pygame, random, math

pygame.init()

ancho, alto = 800, 600
negro = (0, 0, 0)
blanco = (255, 255, 255)
FPS = 60
velocidad = 7
velocidadnalguis = velocidad - 2
contadordecolisiones = 1
perseguidores = []

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("un jueguito")
reloj = pygame.time.Clock()


class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Red-Ball-PNG-Image.png").convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.center = (ancho / 2, alto / 2)
        self.speed = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.speedx = -velocidad

        if tecla[pygame.K_RIGHT]:
            self.speedx = velocidad

        if tecla[pygame.K_UP]:
            self.speedy = -velocidad

        if tecla[pygame.K_DOWN]:
            self.speedy = velocidad

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > ancho:
            self.rect.right = ancho

        if self.rect.bottom > alto:
            self.rect.bottom = alto

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0


pelota = Pelota()


class Perseguidor(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = pygame.image.load('Red-Ball-PNG-Image.png').convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.velocidad = velocidadnalguis
        self.radius = self.rect.width / 2
        self.center = self.rect.center
        self.contadordecolisiones = 1
        self.enerandom = random.randint(0, 4)

        if self.enerandom == 0:
            self.rect.center = (random.randrange(-130, -30), random.randrange(-130, alto + 130))
        if self.enerandom == 1:
            self.rect.center = (random.randrange(-130, ancho + 130), random.randrange(-130, -30))
        if self.enerandom == 2:
            self.rect.center = (random.randrange(ancho + 30, ancho + 130), random.randrange(-130, alto + 130))
        if self.enerandom == 3:
            self.rect.center = (random.randrange(-130, ancho + 130), random.randrange(alto + 30, alto + 130))

    def update(self):

        self.pely = pelota.rect.y
        self.pelx = pelota.rect.x
        self.perx = self.rect.x
        self.pery = self.rect.y

        self.dist = math.sqrt(((self.pely - self.pery) ** 2) + ((self.pelx - self.perx) ** 2)) / velocidadnalguis

        self.angulo = math.atan2(self.pely - self.pery, self.pelx - self.perx)

        self.speedx = 0
        self.speedy = 0
        self.speedx = math.cos(self.angulo)
        self.speedy = math.sin(self.angulo)

        old_rect = self.rect.copy()
        if self.dist >= 1:
            self.rect.x += velocidadnalguis * self.speedx
            self.rect.y += velocidadnalguis * self.speedy

        hit = pygame.sprite.spritecollide(self, perseguidor_grupo, False, pygame.sprite.collide_circle)
        if len(hit) > 1:  # at last 1, because the ball hits itself
            if random.randrange(2) == 0:
                self.rect.x = old_rect.x
            else:
                self.rect.y = old_rect.y
            hit = pygame.sprite.spritecollide(self, perseguidor_grupo, False, pygame.sprite.collide_circle)
            if len(hit) > 1:
                self.rect = old_rect


all_sprites = pygame.sprite.Group()
perseguidor_grupo = pygame.sprite.Group()
all_sprites.add(pelota)

terminar = False

requested_balls = 1

while not terminar:
    reloj.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminar = True

    if len(perseguidor_grupo) < 1:
        perseguidor = Perseguidor()
        perseguidor_grupo.add(perseguidor)
        all_sprites.add(perseguidor)

    hit = pygame.sprite.spritecollide(pelota, perseguidor_grupo, True, pygame.sprite.collide_circle)
    if hit:
        requested_balls = min(25, requested_balls + 1)
    if len(perseguidor_grupo) < requested_balls:
        perseguidor = Perseguidor()
        if not pygame.sprite.spritecollide(perseguidor, perseguidor_grupo, True, pygame.sprite.collide_circle):
            all_sprites.add(perseguidor)
            perseguidor_grupo.add(perseguidor)
            perseguidores.append(perseguidor)

    dist = 1

    if len(perseguidores) > len(perseguidor_grupo):
        del perseguidores[0]

    all_sprites.update()
    pantalla.fill(negro)
    all_sprites.draw(pantalla)

    pygame.display.flip()

pygame.quit()
quit()