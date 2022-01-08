import os
import sys
import sqlite3
import random

import pygame

from game import Game
from game.bricks import Bricks
from game.bricks_2 import Bricks2

global exit_code, symbols, exit_code_list_level1, \
    exit_code_list_level2
symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
           "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
           "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
           "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
           "Y", "Z"]
exit_code_list_level1 = ["start1", "start2", "start3"]
exit_code_list_level2 = ["level1", "level2"]
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


FPS = 120
WIDTH, HEIGHT = 600, 600


"""def retrievingData():
    con = sqlite3.connect("database/Records.db")
    cur = con.cursor()
    result = cur.execute("""""")"""


def terminate():
    """n = int(n) + 1
    if session_name is None:
    #if game.return_time() == 0:
        pass
    else:
        time_session = "127"
        #time_session = game.return_time()
        con = sqlite3.connect("database/Records.db")
        cur = con.cursor()
        time = cur.execute(f"INSERT INTO RecordList(ID, BestTime) VALUES({n}, {time_session})").fetchall()
        name = cur.execute("INSERT INTO ID(SessionNumber, Session) VALUES(?, ?);", (n, session_name)).fetchall()
        con.commit()
        con.close()
        f = open("database/BestTime.txt", "w", encoding='UTF-8')
        f.write()
        f.close()"""
    pygame.quit()
    sys.exit()

def write_text(text, font, indent_list, text_coord, k, screen, axis):
    if axis == "y":
        for n, line in enumerate(text):
            string_rendered = font.render(line, 1,
                                          pygame.Color('white'))
            text_rect = string_rendered.get_rect()
            text_rect.top = text_coord
            text_coord += k
            text_rect.x = indent_list[n]
            text_coord += text_rect.height
            screen.blit(string_rendered, text_rect)
    else:
        for n, line in enumerate(text):
            string_rendered = font.render(line, 1,
                                          pygame.Color("white"))
            text_rect = string_rendered.get_rect()
            text_rect.top = text_coord
            text_rect.x = indent_list[n]
            screen.blit(string_rendered, text_rect)


def retrievingSessionList():
    con = sqlite3.connect("database/Records.db")
    cur = con.cursor()
    result = cur.execute("""SELECT Session FROM ID""").fetchall()
    con.close()
    return result


def generationSession(session_list):
    session = ""
    for i in range(10):
        session += random.choice(symbols)
    while session in session_list:
        session = generationSession(session_list)
    print(f"Сессия {session} начата!")
    return session


class Buttons:
    def __init__(self, width, height, len_width, len_height, left,
                 top, cell_size, screen):
        self.width = width
        self.height = height
        self.len_width = len_width
        self.len_height = len_height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.screen = screen
        self.render()

    def render(self):
        self.coords = []
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (self.left + j * (self.cell_size
                                                   + self.len_width),
                                  self.top + i * (self.cell_size
                                                  + self.len_height),
                                  self.len_width, self.len_height),
                                 1, border_radius=50),
                self.coords.append([self.left + j * (self.cell_size +
                                                     self.len_width),
                                    self.top + i * (self.cell_size +
                                                    self.len_height),
                                    self.left + self.len_width + j
                                    * (self.cell_size +
                                       self.len_width),
                                    self.len_height + self.top + i
                                    * (self.cell_size +
                                       self.len_height)])

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cond = True
        for i in range(self.width * self.height):
            if cond is False:
                break
            if x > self.coords[i][0] and x < self.coords[i][2]:
                if y > self.coords[i][1] and y < self.coords[i][3]:
                    count = 0
                    cond = True
                    pos = i
                    while cond:
                        if pos < self.width:
                            return (count, pos)
                        elif pos - self.width >= 0:
                            count += 1
                            pos -= self.width
                        else:
                            cond = False


class StartGame:
    def __init__(self, screen):
        self.screen = screen
        self.fon = pygame.transform.scale((load_image("fon.jpg")),
                                          (WIDTH, HEIGHT))
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 30)
        self.intro_text = ["Добро пожаловать!"]
        self.welcome()

    def text(self):
        text = ["Играть", "Правила", "Рекорд"]
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 30)
        text_rect_list = [238, 225, 234]
        text_coord = 165
        k = 78
        write_text(text, font, text_rect_list, text_coord, k,
                   self.screen, "y")

    def welcome(self):
        text_coord = 50
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 18)
        self.screen.blit(self.fon, (0, 0))
        indent_list = [200]
        write_text(self.intro_text, font, indent_list, text_coord,
                   10, self.screen, "y")
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

            self.text()
            self.buttons = Buttons(1, 3, 190, 65, 200, 150, 50,
                                   self.screen)
            pygame.display.flip()
            clock.tick(FPS)

    def on_click(self, cell_coords):
        global exit_code, exit_code_list_level1
        exit_code = exit_code_list_level1[cell_coords]

    def get_click(self, mouse_pos):
        cell = self.buttons.get_cell(mouse_pos)
        if cell is not None:
            self.cond = True
            self.on_click(cell[0])
            print(cell[0])
        else:
            self.cond = False
            print(None)


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
                   text_coord, 10, screen, "y")
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
    def __init__(self, screen, session, time, best_time):
        self.best_time = best_time
        self.screen = screen
        best_session, best_time = self.retrievingData()
        self.text = [f"{best_session} \t {best_time}", "",
                     f"{session} \t {time}"]
        text_coord = 50
        font = pygame.font.Font(None, 28)
        indent_list = [208] * 3
        fon = pygame.transform.scale(load_image('fon.jpg'),
                                     (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        write_text(self.text, font, indent_list, text_coord,
                   25, self.screen, "y")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)

    """def retrievingSession(self, best_time):
        con = sqlite3.connect("database/Records.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT Session FROM ID
                                     WHERE SessionNumber=(
                                 SELECT ID FROM RecordList
                                     WHERE BestTime == {best_time})
                              ").fetchall()
        con.close()
        result = result[0][0]
        return result"""

    def retrievingData(self):
        best_time = self.best_time
        while len(best_time) != 4:
            best_time = "0" + best_time
        return (self.retrievingSession(self.best_time),
                best_time)


class LevelChange:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = Buttons(2, 1, 190, 65, 0, 535, 220,
                               self.screen)
        self.cycle()

    def text(self):
        text = ["Вернутся", "Следующий"]
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 26)
        text_rect_list = [28, 420]
        text_coord = 550
        k = 0
        write_text(text, font, text_rect_list, text_coord, k,
                   self.screen, "x")

        text = ["Поздравляю!", "",
                "Вы прошли первый уровень!", "",
                "Вы можете начать проходить уровень заново",
                "Или перейти к следующему уровню!"]
        font = pygame.font.Font(None, 32)
        indent_list = [10] * 6
        text_coord = 50
        write_text(text, font, indent_list,
                   text_coord, 10, self.screen, "y")

    def on_click(self, cell_coords):
        global exit_code, exit_code_list_level2
        exit_code = exit_code_list_level2[cell_coords]

    def get_click(self, mouse_pos):
        cell = self.buttons.get_cell(mouse_pos)
        if cell is not None:
            self.cond = True
            self.on_click(cell[1])
            print(cell[1])
        else:
            self.cond = False
            print(None)

    def cycle(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    total = self.get_click(event.pos)
                    if self.cond:
                        return
            self.text()
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game(Bricks)
    f = open("database/BestTime.txt", mode="r", encoding="UTF-8")
    best_time = f.read()
    best_time = best_time
    f.close()
    session_list = retrievingSessionList()
    session = generationSession(session_list)
    if game.return_time() == 0:
        time = "0000"
    """else:
        time = game.return_time()"""
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
            Record(screen, session, time, best_time)
        StartGame(screen)
    exit_code = "level1"
    level = Bricks
    level_status = False
    screen.blit(fon, (0, 0))
    """level1 = False"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or
                  event.type == pygame.MOUSEBUTTONDOWN) and \
                  level_status is None:
                game = Game(level)

                """game = Game(Bricks)
                level1 = False"""
        if level_status:
            LevelChange(screen)
            level_status = False
        if exit_code == "inGame":
            game.handle_events()
            game.update()
        elif exit_code == "level1":
            exit_code = "inGame"
            level = Bricks
            game = Game(level)
        elif exit_code == "level2":
            level = Bricks2
            game = Game(level)
            exit_code = "inGame"
        level_status = game.draw()
        """if exit_code == "level1" and level1 is False:
            game.handle_events()
            game.update()
            level1 = game.draw()
        elif exit_code == "level2":
            game = Game(Bricks2)
            exit_code = "inGame"
        if level1:
            LevelChange(screen)
            game = Game(Bricks)
            level1 = False"""
        pygame.display.update()
        clock.tick(FPS)
