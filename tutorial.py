import pygame as pg
import os

pg.font.init()
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)
WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First")

YELLOW_SHIP = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SHIP = pg.transform.rotate(pg.transform.scale(YELLOW_SHIP, (55, 40)), 90)
RED_SHIP = pg.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SHIP = pg.transform.rotate(pg.transform.scale(RED_SHIP, (55, 40)), 270)
SPACE = pg.transform.scale(pg.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

SHIP_WIDTH = 55
SHIP_HEIGHT = 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

def main():
    pg.init()
    red = pg.Rect(WIDTH - 100 - SHIP_WIDTH, HEIGHT//2 - SHIP_HEIGHT//2, SHIP_HEIGHT, SHIP_WIDTH)
    yellow = pg.Rect(100, HEIGHT//2 - SHIP_HEIGHT//2, SHIP_HEIGHT, SHIP_WIDTH)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 4)
                    yellow_bullets.append(bullet)
                if event.key == pg.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pg.Rect(red.x, red.y + red.height//2 - 2, 10, 4)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        keys_pressed = pg.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

    main()

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill((192, 192, 192))
    pg.draw.rect(WIN, (0, 0, 0), BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255, 255, 255))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))
    for bullet in red_bullets:
        pg.draw.rect(WIN, (255, 0, 0), bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(WIN, (255, 255, 0), bullet)
    pg.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pg.display.update()
    pg.time.delay(3000)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pg.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pg.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pg.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pg.K_LEFT] and red.x - VEL > BORDER.x:
        red.x -= VEL
    if keys_pressed[pg.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pg.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pg.K_DOWN] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)

if __name__ == "__tutorial__":
    main()