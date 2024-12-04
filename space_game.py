import pygame, controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores

def run():

    pygame.init()
    screen = pygame.display.set_mode((650, 800))
    pygame.display.set_caption('Space battle')
    bg_color = (0, 0, 0)

    clock = pygame.time.Clock()

    gun = Gun(screen)
    bullets = Group()
    aliens = Group()
    controls.create_army(screen, aliens)
    stats = Stats()
    sc = Scores(screen, stats)

    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            bullets.update()
            controls.update(bg_color, screen, stats, sc, gun, aliens, bullets)
            controls.update_bullets(screen, stats, sc, aliens, bullets)
            controls.update_aliens(stats, screen, sc, gun, aliens, bullets)

            if stats.guns_left <= 0:  # Если жизни закончились
                stats.game_over = True
                stats.run_game = False  # Останавливаем игру

        if stats.game_over:
            controls.show_game_over(screen, stats)  # Показываем сообщение

        clock.tick(144)


run()