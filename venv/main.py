import os
import sys

import pygame

global exit_code
exit_code = ""


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
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

def write_text(text, font, indent_list, text_coord, k, screen):
    for n, line in enumerate(text):
        string_rendered = font.render(line, 1,
                                      pygame.Color('white'))
        text_rect = string_rendered.get_rect()
        text_rect.top = text_coord
        text_coord += k
        text_rect.x = indent_list[n]
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)


class StartGame:
    def __init__(self, screen):
        self.screen = screen
        self.fon = pygame.transform.scale((load_image("fon.jpg")),
                                          (WIDTH, HEIGHT))
        self.intro_text = ["Добро пожаловать!"]
        self.welcome()

    def render(self):
        self.width = 1
        self.height = 3
        self.len_width = 190
        self.len_height = 65
        self.board = ["Играть", "Правила", "Рекорд"]
        self.left = 200
        self.top = 150
        self.cell_size = 50
        text_rect_list = [238, 225, 234]
        text_coord = 165
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 30)
        self.coords = []
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (self.left,
                                  self.top + i * (self.cell_size
                                                  + self.len_height),
                                  self.len_width, self.len_height),
                                 1, border_radius=50)
                write_text(self.board, font, text_rect_list,
                           text_coord, 78, screen)
                self.coords.append([self.left,
                                    self.top + i * (self.cell_size +
                                                    self.len_height),
                                    self.left + self.len_width,
                                    self.len_height + self.top + i
                                    * (self.cell_size +
                                       self.len_height)])
        string_rendered = font.render(self.board[0], 1,
                                      pygame.Color("white"))

    def welcome(self):
        text_coord = 50
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 18)
        self.screen.blit(self.fon, (0, 0))
        indent_list = [200]
        write_text(self.intro_text, font, indent_list, text_coord,
                   10, screen)
        print("Добро пожаловать!")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    total = self.get_click(event.pos)
                    if self.cond:
                        return
            pygame.display.flip()
            clock.tick(FPS)

            self.render()
            pygame.display.flip()
            clock.tick(FPS)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cond = True
        for i in range(3):
            if cond is False:
                break
            if x > self.coords[i][0] and x < self.coords[i][2]:
                if y > self.coords[i][1] and y < self.coords[i][3]:
                    count = 0
                    cond = True
                    pos = i
                    while cond:
                        if pos < self.width:
                            return (count)
                        elif pos - self.width >= 0:
                            count += 1
                            pos -= self.width
                        else:
                            cond = False

    def game(self):
        pass

    def on_click(self, cell_coords):
        global exit_code
        if cell_coords == 0:
            exit_code = "start1"
        elif cell_coords == 1:
            exit_code = "start2"
        elif cell_coords == 2:
            exit_code = "start3"

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.cond = True
            self.on_click(cell)
        else:
            self.cond = False
        print(cell)


class Rules:
    def __init__(self, screen):
        self.rules_text = ["Цель игры",
                           "Очистить игровое поле от блоков, попадая "
                           "по ним",
                           "шариком", "",
                           "Шарик отскакивает от ракетки, которую вы",
                           'можете передвигать с помощью клавишь'
                           ' "A" и "D"']
        font = pygame.font.Font(None, 30)
        indent_list = [10] * 6
        text_coord = 50
        fon = pygame.transform.scale(load_image('fon.jpg'),
                                     (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        write_text(self.rules_text, font, indent_list,
                   text_coord, 10, screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)


class Record:
    def __init__(self, screen, session, time):
        self.screen = screen
        best_session, best_time = self.retrievingData()
        session
        time
        self.text = [f"{best_session} \t {best_time}", "",
                     f"{session} \t {time}"]
        text_coord = 50
        font = pygame.font.Font(None, 28)
        indent_list = [208] * 3
        fon = pygame.transform.scale(load_image('fon.jpg'),
                                     (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        write_text(self.text, font, indent_list, text_coord,
                   25, self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    def retrievingData(self):
        return ("0000000000", "0000")



if __name__ == "__main__":
    session = "0000000000"
    time = "0000"
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('main_background.png'),
                                 (WIDTH, HEIGHT))

    StartGame(screen)
    while exit_code != "start1":
        if exit_code == "start2":
            Rules(screen)
        elif exit_code == "start3":
            Record(screen, session, time)
        StartGame(screen)
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.update()
        clock.tick(FPS)
