import sys
from random import randint
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0, 0))
clock = pygame.time.Clock()
score_font = pygame.font.SysFont(None, 40)

apple_image = pygame.image.load("./images/apple.png").convert_alpha()
banana_image = pygame.image.load("./images/banana.png").convert_alpha()
box_image = pygame.image.load("./images/box.png").convert_alpha()

screen_yokohaba = pygame.display.get_surface().get_size()[0]
screen_tatehaba = pygame.display.get_surface().get_size()[1]

fruit_size = apple_image.get_size()
box_size = box_image.get_size()

box_basyo = [screen_yokohaba/2 - box_size[0]/2, screen_tatehaba/2 - box_size[1]/2]

apple_score = 0
banana_score = 0
drop_count = 0

apple_list = []
for i in range(3):
    yoko = randint(0, screen_yokohaba) - fruit_size[0]/2
    tate = -fruit_size[1]/2
    speed = randint(2, 4)
    apple_list.append([yoko, tate, speed])
banana_list = []
for i in range(3):
    yoko = randint(0, screen_yokohaba) - fruit_size[0]/2
    tate = -fruit_size[1]/2
    speed = randint(2, 4)
    banana_list.append([yoko, tate, speed])

tyouten_list = [
    [0, 0],
    [fruit_size[0], 0],
    [0, fruit_size[1]],
    [fruit_size[0], fruit_size[1]],
]

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    box_basyo[0] = pygame.mouse.get_pos()[0] - box_size[0]/2
    box_basyo[1] = pygame.mouse.get_pos()[1] - box_size[1]/2
    screen.blit(box_image, (box_basyo[0], box_basyo[1]))

    for apple in apple_list:
        apple[1] += apple[2]
        screen.blit(apple_image, (apple[0], apple[1]))
        for tyouten in tyouten_list:
            tyouten_yoko = apple[0] + tyouten[0]
            tyouten_tate = apple[1] + tyouten[1]
            if box_basyo[0] <= tyouten_yoko <= box_basyo[0]+box_size[0] and box_basyo[1] <= tyouten_tate <= box_basyo[1]+box_size[1]:
                apple_score += 1
                apple[0] = randint(0, screen_yokohaba) - fruit_size[0]/2
                apple[1] = - fruit_size[1]/2
                pygame.mixer.music.load("./audio/catch.ogg")
                pygame.mixer.music.play(1)
                break
            elif apple[1] >= screen_tatehaba:
                drop_count += 1
                apple[0] = randint(0, screen_yokohaba) - fruit_size[0]/2
                apple[1] = - fruit_size[1]/2
                pygame.mixer.music.load("./audio/drop.ogg")
                pygame.mixer.music.play(1)
                break

    for banana in banana_list:
        banana[1] += banana[2]
        screen.blit(
            banana_image, (banana[0]-fruit_size[0]/2, banana[1]-fruit_size[1]/2))
        for tyouten in tyouten_list:
            tyouten_yoko = banana[0] + tyouten[0]
            tyouten_tate = banana[1] + tyouten[1]
            if box_basyo[0] <= tyouten_yoko <= box_basyo[0]+box_size[0] and box_basyo[1] <= tyouten_tate <= box_basyo[1]+box_size[1]:
                banana_score += 1
                banana[0] = randint(0, screen_yokohaba) - fruit_size[0]/2
                banana[1] = -fruit_size[1]/2
                pygame.mixer.music.load("./audio/catch.ogg")
                pygame.mixer.music.play(1)
                break
            elif banana[1] >= screen_tatehaba:
                drop_count += 1
                banana[0] = randint(0, screen_yokohaba) - fruit_size[0]/2
                banana[1] = -fruit_size[1]/2
                pygame.mixer.music.load("./audio/drop.ogg")
                pygame.mixer.music.play(1)
                break

    score_txt = "drop: " + str(drop_count)
    text = score_font.render(score_txt, True, (0, 0, 0))
    screen.blit(text, (50, 50))

    score_txt = "apple: " + str(apple_score)
    text = score_font.render(score_txt, True, (0, 0, 0))
    screen.blit(text, (50, 90))

    score_txt = "banana: " + str(banana_score)
    text = score_font.render(score_txt, True, (0, 0, 0))
    screen.blit(text, (50, 130))

    if drop_count >= 5:
        break

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

message_font = pygame.font.SysFont(None, 100)
screen.fill((255, 255, 255))
text = message_font.render("Game Over!", True, (0, 0, 0))
screen.blit(text, (screen_yokohaba/2-text.get_size()
            [0]/2, screen_tatehaba/2-text.get_size()[1]/2-80))
score_text = score_font.render(
    "apple: " + str(apple_score) + "  " + "banana: " + str(banana_score), True, (0, 0, 0))
screen.blit(score_text, (screen_yokohaba/2-score_text.get_size()
            [0]/2, screen_tatehaba/2-text.get_size()[1]/2))
pygame.display.update()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
