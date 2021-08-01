import pygame as pg
import os, sys, random
from spaceship import Spaceship

pg.font.init()
pg.init()
HEALTH_FONT = pg.font.SysFont('arial', 40)
MENU_FONT = pg.font.SysFont('arial', 100)
WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Duel")
clock = pg.time.Clock()
FPS = 60

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

SHIP_WIDTH = 55
SHIP_HEIGHT = 40
VEL = 5
LASER_VEL = 7
MAX_LASERS = 10
MIDLINE = pg.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

PLAYER_HIT = pg.USEREVENT + 1
ENEMY_HIT = pg.USEREVENT + 2

paused = False


def main_menu():
    timer_sec = 0
    click = False
    running = True
    while running:
        mx, my = pg.mouse.get_pos()
        screen.fill((192, 192, 192))
        title = MENU_FONT.render("DUEL", 1, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 10))
        button_1 = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 4, 400, 60)
        button_2 = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 6, 400, 60)
        one_player = HEALTH_FONT.render("1 Player", 1, BLACK)
        one_player_rect = one_player.get_rect(center=(WIDTH // 2, button_1.centery))
        screen.blit(one_player, one_player_rect)
        two_player = HEALTH_FONT.render("2 Players", 1, BLACK)
        two_player_rect = two_player.get_rect(center=(WIDTH // 2, button_2.centery))
        screen.blit(two_player, two_player_rect)
        pg.draw.rect(screen, BLACK, button_1, 5)
        pg.draw.rect(screen, BLACK, button_2, 5)
        clock.tick(FPS)
        if button_1.collidepoint((mx, my)):
            if click:
                duel_1()
        if button_2.collidepoint((mx, my)):
            if click:
                duel_2()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()

    main_menu()


def duel_1():
    ai_move = pg.USEREVENT + 3
    ai_shoot = pg.USEREVENT + 4
    pg.time.set_timer(ai_move, 500)
    pg.time.set_timer(ai_shoot, 400)
    ai = True
    direction = UP
    global paused
    player = Spaceship(os.path.join('Assets', '6b.png'))
    player.image = pg.transform.rotate(player.image, 270)
    player.rect.x, player.rect.y = (100, HEIGHT // 2 - player.rect.width // 2)
    enemy = Spaceship(os.path.join('Assets', '6.png'))
    enemy.image = pg.transform.rotate(enemy.image, 90)
    enemy.rect.x, enemy.rect.y = (WIDTH - 100 - enemy.rect.width, HEIGHT // 2 - player.rect.width // 2)
    countdown(player, enemy)
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((192, 192, 192))
        pg.draw.rect(screen, BLACK, MIDLINE)
        screen.blit(player.image, (player.rect.x, player.rect.y))
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
        keys_pressed = pg.key.get_pressed()
        move_player(player, keys_pressed)
        move_enemy_ai(enemy, direction)
        move_lasers(player.shots, enemy.shots, player, enemy)
        player_health = HEALTH_FONT.render("Health: " + str(player.health), 1, BLACK)
        enemy_health = HEALTH_FONT.render("Health: " + str(enemy.health), 1, BLACK)
        screen.blit(enemy_health, (WIDTH - enemy_health.get_width() - 10, 10))
        screen.blit(player_health, (10, 10))
        for laser in player.shots:
            pg.draw.rect(screen, (0, 0, 255), laser)
        for laser in enemy.shots:
            pg.draw.rect(screen, (255, 0, 0), laser)

        win_text = ''
        if player.health <= 0:
            win_text = 'YOU LOSE'
        if enemy.health <= 0:
            win_text = 'YOU WIN'
        if win_text != '':
            game_over(win_text, ai)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and len(player.shots) < MAX_LASERS:
                    laser = pg.Rect(player.rect.midright[0], player.rect.midright[1], 10, 4)
                    player.shots.append(laser)
                if event.key == pg.K_ESCAPE:
                    paused = True
                    pause()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == ENEMY_HIT:
                enemy.health -= 1
            if event.type == PLAYER_HIT:
                player.health -= 1
            if event.type == ai_move:
                directions = [UP, DOWN, LEFT, RIGHT]
                directions.remove(direction)
                new_dir = random.randint(0, 2)
                direction = directions[new_dir]
            if event.type == ai_shoot:
                if len(enemy.shots) < MAX_LASERS:
                    laser = pg.Rect(enemy.rect.midleft[0] - 10, enemy.rect.midleft[1], 10, 4)
                    enemy.shots.append(laser)
        pg.display.update()


def duel_2():
    global paused
    ai = False
    player = Spaceship(os.path.join('Assets', '6b.png'))
    player.image = pg.transform.rotate(player.image, 270)
    player.rect.x, player.rect.y = (100, HEIGHT // 2 - player.rect.width // 2)
    enemy = Spaceship(os.path.join('Assets', '6.png'))
    enemy.image = pg.transform.rotate(enemy.image, 90)
    enemy.rect.x, enemy.rect.y = (WIDTH - 100 - enemy.rect.width, HEIGHT // 2 - player.rect.width // 2)
    countdown(player, enemy)
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((192, 192, 192))
        pg.draw.rect(screen, BLACK, MIDLINE)
        screen.blit(player.image, (player.rect.x, player.rect.y))
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
        keys_pressed = pg.key.get_pressed()
        move_player(player, keys_pressed)
        move_enemy(enemy, keys_pressed)
        move_lasers(player.shots, enemy.shots, player, enemy)
        player_health = HEALTH_FONT.render("Health: " + str(player.health), 1, BLACK)
        enemy_health = HEALTH_FONT.render("Health: " + str(enemy.health), 1, BLACK)
        screen.blit(enemy_health, (WIDTH - enemy_health.get_width() - 10, 10))
        screen.blit(player_health, (10, 10))
        for laser in player.shots:
            pg.draw.rect(screen, (0, 0, 255), laser)
        for laser in enemy.shots:
            pg.draw.rect(screen, (255, 0, 0), laser)

        win_text = ''
        if player.health <= 0:
            win_text = 'RED WINS'
        if enemy.health <= 0:
            win_text = 'BLUE WINS'
        if win_text != '':
            game_over(win_text, ai)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and len(player.shots) < MAX_LASERS:
                    laser = pg.Rect(player.rect.midright[0], player.rect.midright[1], 10, 4)
                    player.shots.append(laser)
                if event.key == pg.K_RALT and len(enemy.shots) < MAX_LASERS:
                    laser = pg.Rect(enemy.rect.midleft[0], enemy.rect.midleft[1], 10, 4)
                    enemy.shots.append(laser)
                if event.key == pg.K_ESCAPE:
                    paused = True
                    pause()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == ENEMY_HIT:
                enemy.health -= 1
            if event.type == PLAYER_HIT:
                player.health -= 1

        pg.display.update()


def game_over(text, ai):
    click = False
    running = True
    while running:
        mx, my = pg.mouse.get_pos()
        end_screen = pg.Rect(0, 0, 600, 400)
        end_screen.center = (WIDTH // 2, HEIGHT // 2)
        pg.draw.rect(screen, WHITE, end_screen)
        end_text = MENU_FONT.render(text, 1, BLACK)
        end_text_rect = end_text.get_rect(center=(WIDTH // 2, end_screen.y + 80))
        screen.blit(end_text, end_text_rect)
        play_again_button = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 5, 400, 60)
        menu_button = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 7, 400, 60)
        pg.draw.rect(screen, BLACK, play_again_button, 5)
        pg.draw.rect(screen, BLACK, menu_button, 5)
        play_again = HEALTH_FONT.render("Play Again", 1, BLACK)
        play_again_rect = play_again.get_rect(center=(WIDTH // 2, play_again_button.centery))
        screen.blit(play_again, play_again_rect)
        menu = HEALTH_FONT.render("Main Menu", 1, BLACK)
        menu_rect = menu.get_rect(center=(WIDTH // 2, menu_button.centery))
        screen.blit(menu, menu_rect)
        if play_again_button.collidepoint((mx, my)):
            if click:
                if ai:
                    duel_1()
                else:
                    duel_2()
        if menu_button.collidepoint((mx, my)):
            if click:
                main_menu()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()


def pause():
    click = False
    while paused:
        mx, my = pg.mouse.get_pos()
        clock.tick(FPS)
        pause_screen = pg.Rect(0, 0, 600, 400)
        pause_screen.center = (WIDTH // 2, HEIGHT // 2)
        pg.draw.rect(screen, WHITE, pause_screen)
        pause_text = MENU_FONT.render('PAUSED', 1, BLACK)
        pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, pause_screen.y + 100))
        screen.blit(pause_text, pause_text_rect)
        continue_button = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 5, 400, 60)
        menu_button = pg.Rect(WIDTH // 2 - 200, HEIGHT // 10 * 7, 400, 60)
        pg.draw.rect(screen, BLACK, continue_button, 5)
        pg.draw.rect(screen, BLACK, menu_button, 5)
        continue_text = HEALTH_FONT.render("Continue", 1, BLACK)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, continue_button.centery))
        screen.blit(continue_text, continue_rect)
        menu = HEALTH_FONT.render("Main Menu", 1, BLACK)
        menu_rect = menu.get_rect(center=(WIDTH // 2, menu_button.centery))
        screen.blit(menu, menu_rect)
        if continue_button.collidepoint((mx, my)):
            if click:
                unpause()
        if menu_button.collidepoint((mx, my)):
            if click:
                main_menu()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    unpause()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()


def unpause():
    global paused
    paused = False


def move_player(player, keys):
    if keys[pg.K_a] and player.rect.x - VEL > 0:
        player.rect.x -= VEL
    if keys[pg.K_d] and player.rect.x + VEL + player.rect.height < MIDLINE.x:
        player.rect.x += VEL
    if keys[pg.K_w] and player.rect.y - VEL > 0:
        player.rect.y -= VEL
    if keys[pg.K_s] and player.rect.y + VEL + player.rect.width < HEIGHT:
        player.rect.y += VEL


def move_enemy(enemy, keys):
    if keys[pg.K_LEFT] and enemy.rect.x - VEL > MIDLINE.x + MIDLINE.width:
        enemy.rect.x -= VEL
    if keys[pg.K_RIGHT] and enemy.rect.x + VEL + enemy.rect.height < WIDTH:
        enemy.rect.x += VEL
    if keys[pg.K_UP] and enemy.rect.y - VEL > 0:
        enemy.rect.y -= VEL
    if keys[pg.K_DOWN] and enemy.rect.y + VEL + enemy.rect.width < HEIGHT:
        enemy.rect.y += VEL


def move_enemy_ai(enemy, dir):
    if dir == LEFT and enemy.rect.x - VEL > MIDLINE.x + MIDLINE.width:
        enemy.rect.x -= VEL
    if dir == RIGHT and enemy.rect.x + VEL + enemy.rect.height < WIDTH:
        enemy.rect.x += VEL
    if dir == UP and enemy.rect.y - VEL > 0:
        enemy.rect.y -= VEL
    if dir == DOWN and enemy.rect.y + VEL + enemy.rect.width < HEIGHT:
        enemy.rect.y += VEL


def move_lasers(player_shots, enemy_shots, player, enemy):
    for laser in player_shots:
        laser.x += LASER_VEL
        if enemy.rect.colliderect(laser):
            pg.event.post(pg.event.Event(ENEMY_HIT))
            player_shots.remove(laser)
        elif laser.x > WIDTH:
            player_shots.remove(laser)
    for laser in enemy_shots:
        laser.x -= LASER_VEL
        if player.rect.colliderect(laser):
            pg.event.post(pg.event.Event(PLAYER_HIT))
            enemy_shots.remove(laser)
        elif laser.x + laser.width < 0:
            enemy_shots.remove(laser)


def countdown(player, enemy):
    timer = pg.USEREVENT + 5
    pg.time.set_timer(timer, 1000)
    time = 3
    timer_screen = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    timer_screen.fill((0, 0, 0, 150))
    timer_text = MENU_FONT.render(str(time), 1, WHITE)
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((192, 192, 192))
        pg.draw.rect(screen, BLACK, MIDLINE)
        screen.blit(player.image, (player.rect.x, player.rect.y))
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
        timer_text = MENU_FONT.render(str(time), 1, WHITE)
        screen.blit(timer_screen, (0, 0))
        screen.blit(timer_text, timer_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == timer:
                time -= 1
        if time == 0:
            running = False
        pg.display.update()


if __name__ == "__main__":
    main_menu()
