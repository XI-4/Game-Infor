# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        super().__init__()
        self.image = pygame.transform.rotate(bullet_img, 180)
        self.rect = self.image.get_rect()
        self.rect.midtop = init_pos
        self.speed = -5

    def move(self):
        self.rect.bottom -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos, mapping):
        super().__init__()
        self.image = [plane_img.subsurface(r).convert_alpha() for r in player_rect]
        self.rect = player_rect[0].copy()
        self.rect.topleft = init_pos
        self.base_speed = 8
        self.speed = self.base_speed
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        self.mapping = mapping
        self.boost_mode = False

    def update_speed(self):
        self.speed = self.base_speed * 2 if self.boost_mode else self.base_speed

    def shoot(self, bullet_img, boosted=False):
        bullet = Bullet(bullet_img, self.rect.midtop)
        if boosted:
            bullet.speed = 15
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos, enemy_type):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2 if enemy_type == 'enemy1' else 1.5 if enemy_type == 'enemy2' else 1
        self.down_index = 0
        self.type = enemy_type

    def move(self):
        self.rect.top += self.speed

    def shoot(self, bullet_img, enemy_bullets):
        bullet = EnemyBullet(bullet_img, self.rect.midbottom)
        enemy_bullets.add(bullet)
