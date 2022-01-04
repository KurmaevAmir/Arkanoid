import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


FPS = 30
WIDTH, HEIGHT = 600, 600


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    clock = pygame.time.Clock()
    intro_text = ["Добро пожаловать!", "",
                  "Цель игры",
                  "Очистить игровое поле от блоков, попадая по ним",
                  "шариком", "",
                  "Шарик отскакивает от ракетки, которую вы можете ",
                  'передвигать с помощью клавишь "A" "D"', "", "", "",
                  "", "", "", "", "",
                  "                              "
                  "        1mpr0ve Production"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("font/my_font.otf", 18)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()
            elif i.type == pygame.KEYDOWN or \
                    i.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    terminate()
