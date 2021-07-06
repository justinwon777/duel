import pygame as pg
import os

pg.font.init()
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)
WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First")

SHIP_WIDTH = 55
SHIP_HEIGHT = 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
BORDER = pg.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)


def main():
    pg.init()
    clock = pg.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()

    main()


if __name__ == "__main__":
    main()
