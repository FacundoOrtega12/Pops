import pygame
# hola pops

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_d,
    K_s,
    K_a,
    KEYDOWN,
    QUIT,
)

class Paddle1(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle1, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.res = (1024, 720)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.res[0]:
            self.rect.right = self.res[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.res[1]:
            self.rect.bottom = self.res[1]


class Paddle2(pygame.sprite.Sprite):
    def __init__(self):
        super(Paddle2, self).__init__()
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.res = (1024, 720)

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.res[0]:
            self.rect.right = self.res[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.res[1]:
            self.rect.bottom = self.res[1]


def main():
    pygame.init()
    res_x = 1024
    res_y = 720
    screen = pygame.display.set_mode((res_x, res_y))
    paddle1 = Paddle1()
    paddle2 = Paddle2()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
            elif event.type == QUIT:
                running = False
            
        screen.fill((0,0,0))
        screen.blit(paddle1.surf, paddle1.rect)
        screen.blit(paddle2.surf, paddle2.rect)
        pygame.display.flip()
        pressed_keys = pygame.key.get_pressed()
        paddle1.update(pressed_keys)
        paddle2.update(pressed_keys)
    






if __name__ == "__main__":
    main()