import pygame
import sys
import os
from game.constants import Constants
from game.player import Player
from game.ball import Ball
from game.bricks import Bricks
import time


class Game:
    def __init__(self, bricks):
        pygame.init()
        self.screen = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))
        self.clock = pygame.time.Clock()

        fullname = os.path.join('data', "main_background.png")
        image = pygame.image.load(fullname)
        self.fon = pygame.transform.scale(image, (600, 600))
        self.start_time = time.time()
        self.finish_time = 0
        self.real_time = 0
        #self.bg_color = pygame.Color('black')

        self.font = pygame.font.Font('font/my_font.otf', 16)
        self.game_over = 0

        self.player = Player()
        self.ball = Ball()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.ball)

        self.level = bricks(self.all_sprites)

        self.bricks = self.level

    def reset(self):
        self.real_time = 0
        self.start_time = time.time()
        self.finish_time = 0
        self.game_over = 0
        self.player = Player()
        self.ball = Ball()
        self.all_sprites.empty()
        self.all_sprites.add(self.player, self.ball)
        self.bricks = self.level

    def handle_events(self):
        self.real_time = "{:.1f}s" \
            .format(time.time() - self.start_time)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()

    def update(self):
        if self.ball.is_off_screen():
            self.player.lose_life()
            if self.player.lives == 0:
                self.game_over = -1
            self.ball.reset()
        self.ball.check_collide_paddle(self.player)
        self.bricks.check_collisions(self.ball)
        self.all_sprites.update()
        pygame.display.update()
        self.clock.tick(120)

    def return_time(self):
        return self.finish_time

    def return_sprites(self):
        return self.all_sprites

    def draw(self):
        #self.screen.fill(self.bg_color)
        self.screen.blit(self.fon, (0, 0))
        if len(self.all_sprites) == 2:
            self.game_over = 1

        if self.game_over != 0:
            if self.finish_time == 0:
                self.finish_time = "time elapsed: {:.1f}s" \
                    .format(time.time() - self.start_time)
            if self.game_over == 1:
                text = self.font.render("", True,
                                        pygame.Color('white'))
                self.screen.blit(text, (Constants.screen_width /
                                        2 - 65,
                                        Constants.screen_height / 2))
                return True
            elif self.game_over == -1:
                text = self.font.render("Вы проиграли!", True,
                                        pygame.Color('white'))
                self.screen.blit(text, (Constants.screen_width /
                                        2 - 65,
                                        Constants.screen_height / 2))
                return None
        else:
            self.all_sprites.draw(self.screen)

            text = self.font.render(f'Жизней: {self.player.lives}',
                                    True, pygame.Color('white'))
            self.screen.blit(text, (15, Constants.screen_height - 30))

            text = self.font.render(f'Время: {self.real_time}', True,
                                    pygame.Color('white'))
            self.screen.blit(text, (Constants.screen_width - 100,
                                    Constants.screen_height - 40))
            return False
