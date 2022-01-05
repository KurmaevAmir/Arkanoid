import pygame
from game.constants import Constants

bricks = [
    'assets/blue.png',
    'assets/green.png',
    'assets/grey.png',
    'assets/purple.png',
    'assets/red.png',
    'assets/yellow.png'
]


class Bricks:
    def __init__(self, all_sprites):
        self.score = 0
        self.all_sprites = all_sprites
        self.all_bricks = pygame.sprite.Group()

        for r in range(Constants.brick_rows):
            for c in range(Constants.brick_cols):
                brick = Brick(r, c)
                self.all_sprites.add(brick)
                self.all_bricks.add(brick)

    def check_collisions(self, ball):
        hits = pygame.sprite.spritecollide(ball, self.all_bricks, False)
        if hits:
            hit_rect = hits[0].rect
            if hit_rect.left < ball.rect.right or ball.rect.left < hit_rect.right:
                ball.bounce_y()
            if hit_rect.bottom > ball.rect.top or hit_rect.top < ball.rect.bottom:
                ball.bounce_x()

            self.score += 1
            hits[0].kill()


class Brick(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.x_pos = 1.2 * (Constants.brick_start + (col * 64) + 32)
        self.y_pos = 1.4 * (Constants.brick_start + (row * 32) + 16)
        self.image = pygame.image.load(bricks[row])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)
