import sys
from random import random
from math import floor
import pygame
from pygame.locals import *


score = {}
drop_count = 0


def getRandom(min, max):
    return floor(random() * (max+1 - min)) + min


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
            global score
            score[fruit.type] += 1


class Fruit(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.type = type
        self.image = pygame.image.load(f"./images/{type}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = getRandom(0, pygame.display.get_surface().get_size()[0])
        self.rect.top = 0
        self.speed = getRandom(3, 5)
        self.update = self.fall
    
    def fall(self):
        self.rect.top += self.speed
        if self.rect.top >= pygame.display.get_surface().get_size()[1]:
            global drop_count
            drop_count += 1
            self.kill()
            return
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    pygame.display.set_caption("フルーツバスケット")
    splite_controller = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    fruit_name_list = [
        "apple",
        "banana"
    ]
    global score
    global drop_count
    for fruit_name in fruit_name_list:
        score[fruit_name] = 0

    fruits = pygame.sprite.Group()
    Fruit.containers = splite_controller, fruits

    Box.containers = splite_controller
    Box(fruits)

    sysfont = pygame.font.SysFont(None, 40)

    while True:
        clock.tick(60)

        screen.fill((255, 255, 255))

        if getRandom(1, 30) == 1:
            Fruit(fruit_name_list[getRandom(0, 1)])

        splite_controller.update()
        splite_controller.draw(screen)

        text_pos_y = 50
        score_txt = f"drop: {drop_count}"
        text = sysfont.render(score_txt, True, (0, 0, 0))
        screen.blit(text, (50, text_pos_y))

        for score_key in score.keys():
            score_txt = score_key + ": " + str(score[score_key])
            text_pos_y += 40
            text = sysfont.render(score_txt, True, (0, 0, 0))
            screen.blit(text, (50, text_pos_y))
        
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
