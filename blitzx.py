import random
import pygame
from pygame.locals import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("plane_s.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT-25
        self.rect.center = (self.x, self.y)
        self.speed = 7

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
            self.y -= self.speed

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
            self.y += self.speed

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.x -= self.speed

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH),0))
        self.speed = random.randint(5, 7)
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.speed = 20

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()

def main():
    pygame.mixer.init()
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 500)

    player = Player()
    missiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w:
                    new_missile = Missile(player.x, player.rect.top)
                    missiles.add(new_missile)
                    all_sprites.add(new_missile)

            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        missiles.update()
        enemies.update()

        screen.fill((135, 206, 250))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            running = False

        if pygame.sprite.groupcollide(missiles, enemies, True, True):
            explosion_sound.play()

        pygame.display.flip()

if __name__=='__main__':
    main()
