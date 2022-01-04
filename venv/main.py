import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey  is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


FPS = 60
WIDTH, HEIGHT = 600, 600


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    print("Добро пожаловать!")
    intro_text = ["Добро пожаловать!", "",
                  "Цель игры",
                  "Очистить игровое поле от блоков, попадая по ним",
                  "шариком", "",
                  "Шарик отскакивает от ракетки, которую вы можете ",
                  'передвигать с помощью клавишь "A" "D"', "", "",
                  "", "", "", "", "", "",
                  "                              "
                  "        1mpr0ve Production"]

    fon = pygame.transform.scale(load_image('fon.jpg'),
                                 (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("font\WellwaitFree Regular.otf", 18)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.update()
        clock.tick(FPS)
