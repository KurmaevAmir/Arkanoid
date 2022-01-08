import os
import sys
import sqlite3
import random

import pygame

from game import Game
from game.bricks import Bricks
from game.bricks_2 import Bricks2

global exit_code, symbols, exit_code_list_level1, \
    exit_code_list_level2, n, level_list, time_list, session
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
n = 0
level_list = []
time_list = []
session = ''


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


def retrievingData(level, n, record=False):
    con = sqlite3.connect("database/Records.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM RecordList
                                WHERE IdLevel=(
                            SELECT Id FROM ID
                                WHERE Level = ?)""",
                         (level,)).fetchall()
    con.close()
    total_list = []
    if record:
        best_level = [0, 1, "0000", "0000000000"]
        if len(result) == 1:
            best_level = result[0]
        else:
            time = 999999
            for i in result:
                if int(i[2]) < time:
                    time = int(i[2])
                    best_level = i
        return best_level
    elif n == 4:
        return result
    elif n < 4:
        for i in result:
            total_list.append(i[n])
        return total_list
    else:
        print("Ошибка запроса")
        return


def terminate(): #n, level_list, time_list, session
    if session == '' or level_list == []:
        pass
    else:
        # result = cur.execute(f"INSERT INTO RecordList VALUES({}, {}, {}, {})")
        for i in range(len(level_list)):
            if level_list[i] == "level1":
                level_list[i] = 1
            elif level_list[i] == "level2":
                level_list[i] = 2
            con = sqlite3.connect("database/Records.db")
            cur = con.cursor()
            cur.execute("INSERT INTO RecordList(Id, IdLevel, Time,"
                        " Session) VALUES(?, ?, ?,"
                        " ?)", (n, level_list[i],
                                time_list[i], session)).fetchall()
            con.commit()
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


"""def retrievingSessionList():
    con = sqlite3.connect("database/Records.db")
    cur = con.cursor()
    result = cur.execute("SELECT Session FROM ID").fetchall()
    con.close()
    return result"""


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
    def __init__(self, screen, session, time, n):
        self.screen = screen
        best_session1, best_time1, n1, best_session2, best_time2,\
        n2 = self.bestSession()
        self.text = ["Сессия \t Время \t Код сессии", "",
                     f"{best_session1} \t {best_time1} \t {n1}", "",
                     f"{best_session2} \t {best_time2} \t {n2}", "",
                     f"{session} \t {time} \t {n + 1}"]
        text_coord = 50
        font = pygame.font.Font(None, 28)
        indent_list = [208] * 7
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

    """def retrievingData(self):
        best_time = self.best_time
        while len(best_time) != 4:
            best_time = "0" + best_time
        return (self.retrievingSession(self.best_time),
                best_time)"""

    def bestSession(self):
        """data1 = retrievingData("level1", 4)
        data2 = retrievingData("level2", 4)
        level1 = retrievingData("level1", 2)
        level2 = retrievingData("level2", 2)
        level1 = max(level1)
        level2 = max(level2)"""
        """if len(data1) == 1:
            best_level1 = data1
        else:
            for i, j in enumerate(data1):
                if level1 in j[i]:
                    best_level1 = j[i]
        if len(data2) == 1:
            best_level2 = data2
        else:
            for i, j in enumerate(data2):
                if level2 in j[i]:
                    best_level2 = j[i]
        best_level1 = data1.index(max(level1))
        best_level1 = data1[best_level1]
        best_level2 = data2.index(max(level2))
        best_level2 = data2[best_level2]
        return (best_level1[3], best_level1[2], best_level1[0],
                best_level2[3], best_level2[2], best_level2[0],
                max(retrievingData("level1", 1)))"""
        best_level1 = retrievingData("level1", 4, record=True)
        best_level2 = retrievingData("level2", 4, record=True)
        return (best_level1[3], best_level1[2], best_level1[0],
                best_level2[3], best_level2[2], best_level2[0],)


def startMenu():
    global exit_code
    StartGame(screen)
    while exit_code != "start1":
        if exit_code == "start2":
            Rules(screen)
        elif exit_code == "start3":
            Record(screen, session, time, n)
        StartGame(screen)
    exit_code = "level1"


class LevelChange:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = Buttons(2, 1, 190, 65, 0, 535, 220,
                               self.screen)
        self.cycle()

    def text(self):
        text = ["Вернуться", "Следующий"]
        font = pygame.font.Font("font/WellwaitFree Regular.otf", 26)
        text_rect_list = [22, 420]
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
    """print(retrievingData("level1"))
    print(retrievingData("level2"))"""
    game = Game(Bricks)
    f = open("database/BestTime.txt", mode="r", encoding="UTF-8")
    best_time = f.read()
    best_time = best_time
    f.close()
    session_list = []
    session_list.append(retrievingData("level1", 3))
    n = len(session_list) + 1
    """data1 = retrievingData("level1")
    data2 = retrievingData("level2")
    session_list = []
    for i in data1:
        session_list.append(i[3])
    for i in data2:
        session_list.append(i[3])"""
    #session_list = retrievingSessionList()
    session = generationSession(session_list)
    time = "0000"
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('main_background.png'),
                                 (WIDTH, HEIGHT))
    level_list = []
    time_list = []

    startMenu()
    level = Bricks
    level_status = False
    screen.blit(fon, (0, 0))
    """level1 = False"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if exit_code == "inGame":
                    del level_list[-1]
                terminate()
            elif (event.type == pygame.KEYDOWN or
                  event.type == pygame.MOUSEBUTTONDOWN) and \
                  level_status is None:
                game = Game(level)

                """game = Game(Bricks)
                level1 = False"""
        if level_status and level_list[-1] == "level1":
            level_status = False
            time = game.return_time()
            time_list.append(time)
            LevelChange(screen)
        elif level_status and level_list[-1] == "level2":
            level_status = False
            time = game.return_time()
            time_list.append(time)
            startMenu()
        if exit_code == "inGame":
            game.handle_events()
            game.update()
        elif exit_code == "level1":
            exit_code = "inGame"
            level = Bricks
            game = Game(level)
            active_level = 'level1'
            level_list.append(active_level)
        elif exit_code == "level2":
            level = Bricks2
            game = Game(level)
            exit_code = "inGame"
            active_level = 'level2'
            level_list.append(active_level)
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
