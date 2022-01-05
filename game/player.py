import pygame
from game.constants import Constants


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/my_paddle.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.y_pos = Constants.screen_height - 50
        self.x_pos = Constants.screen_width / 2
        self.rect.center = (self.x_pos, self.y_pos)
        self.direction = 0
        self.lives = Constants.starting_lives

    def update(self):
        if self.x_pos < 52:
            self.x_pos = 52
        if self.x_pos > Constants.screen_width - 52:
            self.x_pos = Constants.screen_width - 52
        self.rect.center = (self.x_pos, self.y_pos)

    def lose_life(self):
        self.lives -= 1

    def reset(self):
        self.lives = Constants.starting_lives

    def move_left(self):
        self.x_pos -= Constants.paddle_speed
        self.direction = -1

    def move_right(self):
        self.x_pos += Constants.paddle_speed
        self.direction = 1
