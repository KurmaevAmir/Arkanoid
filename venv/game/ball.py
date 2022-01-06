import pygame
from random import randint
from game.constants import Constants


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = Constants.screen_width / 2
        self.y_pos = Constants.screen_height - 80
        self.image = pygame.image.load('assets/my_ball.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = [randint(2, 4), randint(-4, 0)]
        self.rect.center = (self.x_pos, self.y_pos)

    def update(self):
        if self.x_pos < 11 or self.x_pos > Constants.screen_width - 11:
            self.velocity[0] = -self.velocity[0]
        if self.y_pos < 11:
            self.velocity[1] = -self.velocity[1]
        if self.velocity[0] == 0:
            self.velocity[0] += 1
        if self.velocity[1] == 0:
            self.velocity[1] += 1
        self.x_pos += self.velocity[0]
        self.y_pos += self.velocity[1]

        self.rect.center = (self.x_pos, self.y_pos)

    def reset(self):
        self.velocity = [randint(2, 4), randint(-4, 0)]
        self.x_pos = Constants.screen_width / 2
        self.y_pos = Constants.screen_height - 80
        self.rect.center = (self.x_pos, self.y_pos)

    def check_collide_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            if abs(self.rect.bottom - paddle.rect.top) < Constants.collision_threshold and self.velocity[1] > 0:
                self.velocity[1] = -self.velocity[1]
                self.velocity[0] += abs(paddle.direction)
                if self.velocity[0] > Constants.max_ball_speed:
                    self.velocity[0] = Constants.max_ball_speed
                if self.velocity[0] < Constants.max_ball_speed:
                    self.velocity[0] = -Constants.max_ball_speed
            else:
                self.velocity[0] *= -1

    def is_off_screen(self):
        return self.y_pos > Constants.screen_height

    def bounce_y(self):
        self.velocity[1] *= -1

    def bounce_x(self):
        self.velocity[0] *= -1

    def bounce_xy(self):
        self.velocity[1] *= -1
        self.velocity[0] *= -1
