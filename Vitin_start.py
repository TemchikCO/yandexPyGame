import random

import pygame
import data
from pygame.sprite import Sprite

from classes.Avatar import Avatar
from classes.Health_count import Health_count
from classes.Particle import Particle
from classes.AnimatedSprite import AnimatedSprite
from classes.Cloud import Cloud
from classes.Count import Count
from classes.Finish_window import Finish_window
from classes.RanHero import RanHero
from classes.StartSprite import StartSprite
from classes.Tree import Tree
from data import all_sprites, trees, clouds, start_sprites, play_sprites, final_sprites, immovablelet,\
    lets, ground
from classes.StartButton import start_button
from classes.FinishButton import finish_button
from classes.upgrade_window import upgrade_button, upgrade_window, cancel_upgrade_button, money_count


def create_particles(position):
    particle_count = 20
    numbers = range(-15, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class ImmovableLet(StartSprite):
    def __init__(self):
        super().__init__(None, immovablelet, 1000, 307)
        self.speed = 100

    def update(self, ms):
        self.speed += ms // 1000
        self.x -= self.speed * ms / 1000
        self.speed *= 1.0000000001

    def draw(self, screen):
        self.rect.topleft = self.x, self.y
        screen.blit(self.image, self.rect)


class Generate:
    def __init__(self):
        self.total_ms = 0

    def do(self, ms):
        self.total_ms += ms
        if self.total_ms >= 400:
            lets.add(ImmovableLet())
            self.total_ms = 0


def main():
    clock = pygame.time.Clock()
    FPS = 120
    pygame.display.set_caption('Добро пожаловать в игру')

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

    cursor_image = data.load_image("arrow.png", -1)
    cursor = Sprite(all_sprites)
    cursor.image = cursor_image
    cursor.rect = cursor_image.get_rect()

    generate = Generate()

    def take_info():
        file = open('information')
        record = int(file.readline()[7:])
        heapify = int(file.readline()[8:])
        money = int(file.readline()[6:])
        damage = int(file.readline()[7:])
        count_koef = int(file.readline()[11:])
        max_bullet_count = int(file.readline()[17:])
        speed_of_reloading = int(file.readline()[19:])
        if finish_button.finish:
            money += round(count.count // 100)
        with open('information', 'w') as info_file:
            if round(count.count) > record:
                info_file.write(f'record={round(count.count)}')
            else:
                info_file.write(f'record={round(record)}')
            info_file.write('\n')
            info_file.write(f'heapify={str(heapify)}')
            info_file.write('\n')
            info_file.write(f'money={str(money)}')
            info_file.write('\n')
            info_file.write(f'damage={str(damage)}')
            info_file.write('\n')
            info_file.write(f'count_koef={str(count_koef)}')
            info_file.write('\n')
            info_file.write(f'max_bullet_count={str(max_bullet_count)}')
            info_file.write('\n')
            info_file.write(f'speed_of_reloading={str(speed_of_reloading)}')
        return [record, money, heapify, damage, count_koef, max_bullet_count, speed_of_reloading]

    def chek_lets(player):
        return pygame.sprite.spritecollide(player, lets, True)

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
                start_button.check_click(event.pos)
                finish_button.check_click(event.pos)
                upgrade_button.check_click(event.pos)
                cancel_upgrade_button.check_click(event.pos)
                if start_button.button_pressed:
                    spining_hero.kill()
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            if event.type == pygame.KEYDOWN:
                if start_button.button_pressed:
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        ran_hero.jump()
            if pygame.mouse.get_focused():
                cursor.add(all_sprites)
                all_sprites.draw(data.screen)
            else:
                cursor.remove(all_sprites)
        data.screen.fill((0, 255, 255))
        for start_sprite in start_sprites:
            start_sprite.draw(data.screen)
        all_sprites.draw(data.screen)
        spining_hero.update()
        avatar.update(clock.tick(FPS))
        start_button.update(clock.tick(FPS))
        finish_button.update(clock.tick(FPS))
        clouds.update()
        horizontal = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
        if avatar.rect.topleft[1] <= -300:
            avatar.kill()
        if start_button.rect.topleft[1] >= 1200:
            start_button.kill()
        if start_button.button_pressed:
            upgrade_button.update(clock.tick(FPS))
            for play_sprite in play_sprites:
                play_sprite.draw(data.screen)
                play_sprite.update(clock.tick(FPS), tree.speed)
            trees.update(clock.tick(FPS), horizontal, ran_hero.down_flag)
            if pressed[pygame.K_s]:
                ran_hero.down_flag = True
            elif not pressed[pygame.K_s]:
                ran_hero.down_flag = False
            count.update(clock.tick(FPS))
            count.draw(data.screen)
            health_count.update(clock.tick(FPS), take_info())
            health_count.draw(data.screen)
            ran_hero.set_move(horizontal)
            chek_lets(ran_hero)
            generate.do(clock.tick(FPS))
            lets.update(clock.tick(FPS))
            for i in lets:
                i.draw(data.screen)
            ground.update(clock.tick(FPS), horizontal, ran_hero.down_flag)
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
            final.update(clock.tick(FPS))
        if upgrade_button.upgrade_flag:
            upgrade_window.update(clock.tick(FPS))
            upgrade_window.draw(data.screen)
            cancel_upgrade_button.draw(data.screen)
            cancel_upgrade_button.update(clock.tick(FPS))
            money_count.draw(data.screen, take_info())
        all_sprites.update()
        all_sprites.draw(data.screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
