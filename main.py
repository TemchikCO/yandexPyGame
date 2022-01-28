import random

import pygame
import data
from pygame.sprite import Sprite

from classes.Avatar import Avatar
from classes.Bowled import Bowled, control
from classes.Health_count import Health_count
from classes.Particle import Particle
from classes.AnimatedSprite import AnimatedSprite
from classes.Cloud import Cloud
from classes.Count import Count
from classes.Finish_window import Finish_window
from classes.RanHero import RanHero
from classes.Tree import Tree
from classes.Imovablet import ImmovableLet
from data import all_sprites, trees, clouds, start_sprites, play_sprites, final_sprites, \
    lets, ground, upgrade_buttons, bowleds
from classes.StartButton import start_button
from classes.FinishButton import finish_button
from classes.bird_let import Bird
from classes.upgrade_window import upgrade_button, upgrade_window, cancel_upgrade_button, money_count
from classes.Button_for_upgrade import Health_button, Reload_time_button, Bowled_count_button, Damage_button, \
    Count_upgrade_button


def create_particles(position):
    particle_count = 20
    numbers = range(-15, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Generate:
    def __init__(self):
        self.total_ms = 0

    def do(self, ms, speed, score):
        self.total_ms += ms
        if self.total_ms >= 100000 / speed * 4:
            self.total_ms = 0
            if random.choice([True, True, False]):
                lets.add(ImmovableLet(speed, random.choice(data.immovablelets)))
            elif score > 10 and random.choice([True, False]):
                data.birds.add(Bird(random.choice([340, 249, ]), speed))


def chek(i, player, finish):
    if pygame.sprite.collide_mask(i, player):
        finish.finish = True
        data.sounds[0].play()
        pygame.mixer.music.stop()


def chek_lets(player, finish):
    for i in lets:
        chek(i, player, finish)
    for i in data.birds:
        chek(i, player, finish)
    to_kill = []
    for bullet in bowleds:
        for j in data.birds:
            if pygame.sprite.collide_mask(bullet, j):
                to_kill.append(j)
                to_kill.append(bullet)
                data.sounds[4].play()

        for i in lets:
            if bullet.rect.colliderect(i.rect):
                to_kill.append(bullet)
    for i in to_kill:
        i.kill()


def main():
    game_speed = 500
    clock = pygame.time.Clock()
    FPS = 120
    pygame.display.set_caption('Добро пожаловать в игру')
    time = clock.tick(FPS)

    count = Count(all_sprites)
    health_count = Health_count(all_sprites)

    final_image1 = data.load_image("final_image.jpg")
    final_image = pygame.transform.scale(final_image1, (1200, 700))
    final = Finish_window(all_sprites, final_image, 0, -700)
    final.add(final_sprites)

    cloud_image1 = data.load_image("clouds/1.png", -1)
    cloud_image = pygame.transform.scale(cloud_image1, (200, 150))

    Cloud(all_sprites, cloud_image, 0, 100)
    Cloud(all_sprites, cloud_image, 150, 50)
    Cloud(all_sprites, cloud_image, 340, 0)
    Cloud(all_sprites, cloud_image, 660, 0)
    Cloud(all_sprites, cloud_image, 850, 50)
    Cloud(all_sprites, cloud_image, 1000, 100)

    tree_image1 = data.load_image("tree_gif/1.png", -1)
    tree_image = pygame.transform.scale(tree_image1, (200, 150))

    tree = Tree(all_sprites, tree_image, 0, 252)
    Tree(all_sprites, tree_image, 300, 252)
    Tree(all_sprites, tree_image, 600, 252)
    Tree(all_sprites, tree_image, 900, 252)
    Tree(all_sprites, tree_image, 1200, 252)

    avatar_image1 = data.load_image("avatar.png", -1)
    avatar_image = pygame.transform.scale(avatar_image1, (400, 400))
    avatar = Avatar(all_sprites, avatar_image, 390, -70)
    avatar.add(start_sprites)

    image1 = data.load_image("first_hero_animation/1.png", -1)
    image = pygame.transform.scale(image1, (32, 37))
    spining_hero = AnimatedSprite(all_sprites, image, 0, 370, 'first_hero_animation')
    spining_hero.add(start_sprites)

    image1 = data.load_image("raning_hero/1.png", -1)
    image = pygame.transform.scale(image1, (100, 100))
    ran_hero = RanHero(all_sprites, image, 0, 370, 'raning_hero')
    ran_hero.add(play_sprites)

    sky_image1 = data.load_image("sky.jpg")
    sky_image = pygame.transform.scale(sky_image1, (1200, 700))

    cursor_image = data.load_image("arrow.png", -1)
    cursor = Sprite(all_sprites)
    cursor.image = cursor_image
    cursor.rect = cursor_image.get_rect()

    generate = Generate()
    data.load_music(data.game_music[2])

    def take_info():
        file = open('information')
        record = int(file.readline()[7:])

        heapify_line = file.readline()[8:].split('..')
        heapify = int(heapify_line[0])
        heapify_level = int(heapify_line[1][:-1])

        damage_line = file.readline()[7:].split('..')
        damage = int(damage_line[0])
        damage_level = int(damage_line[1][:-1])

        count_koef_line = file.readline()[11:].split('..')
        count_koef = float(count_koef_line[0])
        count_koef_level = int(count_koef_line[1][:-1])

        max_bullet_count_line = file.readline()[17:].split('..')
        max_bullet_count = int(max_bullet_count_line[0])
        max_bullet_count_level = int(max_bullet_count_line[1][:-1])

        speed_of_reloading_line = file.readline()[19:].split('..')
        speed_of_reloading = int(speed_of_reloading_line[0])
        speed_of_reloading_level = int(speed_of_reloading_line[1][:-1])

        money = int(file.readline()[6:])
        if finish_button.finish and count.money_update < 1:
            money += round(count.count // 100)
            count.money_update += 1
        with open('information', 'w') as info_file:
            if round(count.count) > record:
                info_file.write(f'record={round(count.count)}')
            else:
                info_file.write(f'record={round(record)}')
            if Health_button.upgrade_smth:
                heapify += 1
                heapify_level += 1
                money -= Health_button.cost - 1000
                Health_button.upgrade_smth = False
            info_file.write('\n')
            info_file.write(f'heapify={heapify}..{heapify_level}')
            if Damage_button.upgrade_smth:
                damage += 1
                damage_level += 1
                money -= Damage_button.cost - 1000
                Damage_button.upgrade_smth = False
            info_file.write('\n')
            info_file.write(f'damage={str(damage)}..{damage_level}')
            if Count_upgrade_button.upgrade_smth:
                count_koef += 0.5
                count_koef_level += 1
                money -= Count_upgrade_button.cost - 1000
                Count_upgrade_button.upgrade_smth = False
            info_file.write('\n')
            info_file.write(f'count_koef={str(count_koef)}..{count_koef_level}')
            if Bowled_count_button.upgrade_smth:
                max_bullet_count += 1
                max_bullet_count_level += 1
                money -= Bowled_count_button.cost - 1000
                Bowled_count_button.upgrade_smth = False
            info_file.write('\n')
            info_file.write(f'max_bullet_count={str(max_bullet_count)}..{max_bullet_count_level}')
            if Reload_time_button.upgrade_smth:
                speed_of_reloading -= 1
                speed_of_reloading_level += 1
                money -= Reload_time_button.cost - 1000
                Reload_time_button.upgrade_smth = False
            info_file.write('\n')
            info_file.write(f'speed_of_reloading={str(speed_of_reloading)}..{speed_of_reloading_level}')
            info_file.write('\n')
            info_file.write(f'money={str(money)}')
        return [record, money, heapify_line, damage_line, count_koef_line, max_bullet_count_line,
                speed_of_reloading_line]

    upgrade = 1
    running = True
    while running:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                take_info()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                create_particles(pygame.mouse.get_pos())
                if cancel_upgrade_button.cancel_count == upgrade_button.update_count:
                    start_button.check_click(event.pos)
                    upgrade_button.check_click(event.pos)
                cancel_upgrade_button.check_click(event.pos)
                Health_button.check_click(event.pos)
                Reload_time_button.check_click(event.pos)
                Bowled_count_button.check_click(event.pos)
                Damage_button.check_click(event.pos)
                Count_upgrade_button.check_click(event.pos)
                if start_button.button_pressed:
                    spining_hero.kill()
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            if event.type == pygame.KEYDOWN:
                if start_button.button_pressed:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        ran_hero.jump()
                        if ran_hero.is_grounded():
                            data.sounds[3].play()
                    if event.key == pygame.K_SPACE:
                        if control.acept_fire:
                            Bowled(bowleds, data.image_bowled, ran_hero.rect.topleft[0], ran_hero.rect.topleft[1],
                                   ran_hero)
                            data.sounds[1].play()
                            control.bowlet_count += 1
                if event.key == pygame.K_ESCAPE:
                    running = False
            if pygame.mouse.get_focused():
                cursor.add(all_sprites)
                all_sprites.draw(data.screen)
            else:
                cursor.remove(all_sprites)
        data.screen.blit(sky_image, (0, 0))
        for start_sprite in start_sprites:
            start_sprite.draw(data.screen)
        all_sprites.draw(data.screen)
        spining_hero.update()
        avatar.update(time)
        start_button.update(time)
        finish_button.update(time)
        clouds.update()
        horizontal = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
        if avatar.rect.topleft[1] <= -300:
            avatar.kill()
        if start_button.rect.topleft[1] >= 1200:
            start_button.kill()
        if start_button.button_pressed:
            game_speed += 20 * time / 1000
            Health_button.kill()
            Reload_time_button.kill()
            Bowled_count_button.kill()
            Damage_button.kill()
            koef = Count_upgrade_button.smth
            Count_upgrade_button.kill()
            cancel_upgrade_button.kill()
            upgrade_window.kill()
            money_count.kill()
            upgrade_button.update(time)
            play_sprites.update(time, tree.speed)
            for play_sprite in play_sprites:
                play_sprite.draw(data.screen)
            bowleds.update(time)
            for bowled in bowleds:
                bowled.draw(data.screen)
            control.update(take_info(), time)
            control.draw(data.screen)
            trees.update(time, horizontal, ran_hero.down_flag)
            if pressed[pygame.K_s]:
                ran_hero.down_flag = True
            elif not pressed[pygame.K_s]:
                ran_hero.down_flag = False
            count.update(time, koef)
            count.draw(data.screen)
            health_count.update(time, take_info())
            health_count.draw(data.screen)
            ran_hero.set_move(horizontal)
            generate.do(time, game_speed, count.count)
            lets.update(time, game_speed)
            data.birds.update(time, game_speed)
            for i in data.birds:
                i.draw(data.screen)
            for i in lets:
                i.draw(data.screen)
            ground.update(time, horizontal, ran_hero.down_flag)
            chek_lets(ran_hero, finish_button)
        if finish_button.finish:
            ran_hero.speed = 0
            for sprite in start_sprites:
                sprite.speed = 0
                if upgrade >= 2:
                    if sprite.rect.bottomleft[1] <= final.rect.bottomleft[1]:
                        sprite.kill()
            for let in lets:
                let.speed = 0
                if upgrade >= 2:
                    if let.rect.bottomleft[1] <= final.rect.bottomleft[1]:
                        let.kill()
            upgrade += 1
            final.draw(data.screen, take_info(), count.count)
            final.update(time)
        if upgrade_button.upgrade_flag:
            upgrade_window.update(time)
            upgrade_window.draw(data.screen)
            cancel_upgrade_button.draw(data.screen)
            money_count.draw(data.screen, take_info())
            upgrade_buttons.update(take_info())
            for i in upgrade_buttons:
                i.draw(data.screen)
        all_sprites.update()
        all_sprites.draw(data.screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
