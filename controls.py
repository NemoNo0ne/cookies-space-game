import time

import pygame, sys
from aliens import Alien
from bullet import Bullet
import pygame.time

# Добавьте задержку для стрельбы
shoot_delay = 200  # Задержка между выстрелами в миллисекундах
last_shot_time = 0  # Время последнего выстрела
def events(screen, gun, bullets):
    """обработка событий"""
    global last_shot_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                gun.mright = True
            elif event.key == pygame.K_a:
                gun.mleft = True
            elif event.key == pygame.K_SPACE:
                gun.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                gun.mright = False
            elif event.key == pygame.K_a:
                gun.mleft = False
            elif event.key == pygame.K_SPACE:
                gun.shooting = False


    # В игровом цикле
    if gun.shooting:
        current_time = pygame.time.get_ticks()  # Текущее время
        if current_time - last_shot_time > shoot_delay:
            new_bullet = Bullet(screen, gun)
            bullets.add(new_bullet)
            last_shot_time = current_time  # Обновляем время последнего выстрела


def update(bg_color, screen, stats, sc, gun, aliens, bullets):
    """Обновление экрана"""
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(screen, stats, sc, aliens, bullets):
    """Обновление поцизии пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += 10 * len(aliens)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(aliens) == 0:
        bullets.empty()
        create_army(screen, aliens)



def gun_kill(stats, screen, sc, gun, aliens, bullets):
    """Столкновение пушки и армии"""
    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens)
        gun.creat_gun()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_aliens(stats, screen, sc, gun, aliens, bullets):
    """Обновление позиции пришельцев"""
    aliens.update()
    if pygame.sprite.spritecollideany(gun, aliens):
        gun_kill(stats, screen, sc,  gun, aliens, bullets)
    aliens_check(stats, screen, sc, gun, aliens, bullets)



def aliens_check(stats, screen, sc, gun, aliens, bullets):
    """Добралась ли армия до края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, aliens, bullets)
            break


def create_army(screen, aliens):
    """Создагние армии пришельцев"""
    alien = Alien(screen)
    alien_width = alien.rect.width
    number_aliens_x = int(((650 - 2 * alien_width) // alien_width))
    alien_height = alien.rect.height
    number_alien_y = int(((650 - 100 - 2 * alien_height) // alien_height))


    for row_number in range(number_alien_y - 1):
        for aliens_number in range(number_aliens_x):
            alien = Alien(screen)
            alien.x = alien_width + alien_width * aliens_number
            alien.y = alien_height + alien_height * row_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + alien.rect.height * row_number
            aliens.add(alien)


def check_high_score(stats, sc):
    """Проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write((str(stats.high_score)))


def show_game_over(screen, stats):
    """Показывает сообщение о проигрыше и изображение"""
    font = pygame.font.SysFont(None, 55)

    # Загружаем изображение
    image = pygame.image.load('img/pixil-frame.png')  # Укажите путь к изображению
    image_rect = image.get_rect()

    # Размещаем изображение над текстом
    image_rect.centerx = screen.get_width() // 2
    image_rect.bottom = screen.get_height() // 2 - 80  # Немного выше текста

    # Выводим изображение
    screen.blit(image, image_rect)

    # Создаем текст "Вы проиграли!"
    text = font.render("Вы проиграли!", True, (255, 0, 0))  # Красный цвет
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_width() // 2
    text_rect.top = image_rect.bottom - 20  # Немного ниже изображения

    # Выводим текст на экран
    screen.blit(text, text_rect)

    pygame.display.flip()

