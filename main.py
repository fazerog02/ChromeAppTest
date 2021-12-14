import sys
from random import randint
import pygame
from pygame.locals import *


apple_score = 0
banana_score = 0
drop_count = 0


class Box(pygame.sprite.Sprite):
    def __init__(self, fruits):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("./images/box.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = pygame.display.get_surface().get_rect().centerx
        self.rect.top = pygame.display.get_surface().get_rect().centery + 200
        self.fruits = fruits
        self.update = self.move
    
    def move(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()
        self.rect.left -= self.rect.width / 2
        self.rect.top -= self.rect.height / 2
        collided_fruits = pygame.sprite.spritecollide(self, self.fruits, True)
        for fruit in collided_fruits:
            if fruit.type == "apple":
                global apple_score
                apple_score += 1
            elif fruit.type == "banana":
                global banana_score
                banana_score += 1
            pygame.mixer.music.load("./audio/catch.ogg")
            pygame.mixer.music.play(1)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.type = type
        self.image = pygame.image.load(f"./images/{type}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, pygame.display.get_surface().get_size()[0])
        self.rect.top = 0
        self.speed = randint(3, 5)
        self.update = self.fall
    
    def fall(self):
        self.rect.top += self.speed
        if self.rect.top >= pygame.display.get_surface().get_size()[1]:
            global drop_count
            drop_count += 1
            pygame.mixer.music.load("./audio/drop.ogg")
            pygame.mixer.music.play(1)
            self.kill()
            return
        

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    splite_controller = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    global apple_score
    global banana_score
    global drop_count

    fruits = pygame.sprite.Group()
    Fruit.containers = splite_controller, fruits

    Box.containers = splite_controller
    Box(fruits)

    sysfont = pygame.font.SysFont(None, 40)

    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))

        if randint(1, 30) == 1:
            if randint(0, 1) == 0:
                Fruit("apple")
            else:
                Fruit("banana")

        splite_controller.update()
        splite_controller.draw(screen)

        score_txt = "drop: " + str(drop_count)
        text = sysfont.render(score_txt, True, (0, 0, 0))
        screen.blit(text, (50, 50))

        score_txt = "apple: " + str(apple_score)
        text = sysfont.render(score_txt, True, (0, 0, 0))
        screen.blit(text, (50, 90))

        score_txt = "banana: " + str(banana_score)
        text = sysfont.render(score_txt, True, (0, 0, 0))
        screen.blit(text, (50, 130))
        
        if drop_count >= 3:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
