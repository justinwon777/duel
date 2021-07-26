import pygame as pg


class Spaceship(pg.sprite.Sprite):
    def __init__(self, path):
        self.image = pg.image.load(path)
        self.health = 10
        self.shots = []
        self.rect = self.image.get_rect()