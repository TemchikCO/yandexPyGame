import random

import pygame
import data
from pygame.sprite import Sprite
from data import all_sprites

button_pressed = False
GRAVITY = 1


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [data.load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, 1200, 700)):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-15, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class StartSprite(Sprite):
    def __init__(self, group, surface, x, y):
        if group:
            super().__init__(group)
        else:
            super().__init__()
        self.image = surface
        self.rect = surface.get_rect()
        self.x: float = x
        self.y: float = y
        self.speed = 300
        self.dir_y: float = 0

    def draw(self, screen):
        self.rect.topleft = self.x, self.y
        screen.blit(self.image, self.rect)


class StartButton(StartSprite):
    def __init__(self, group, surface, x, y):
        super().__init__(group, surface, x, y)

    def check_click(self, pos):
        if self.rect.topleft[0] <= pos[0] <= self.rect.bottomright[0]:
            if self.rect.topleft[1] <= pos[1] <= self.rect.bottomright[1]:
                global button_pressed
                button_pressed = True

    def update(self, ms):
        self.y += self.dir_y * ms / 1000
        if button_pressed:
            self.dir_y = self.speed


class Avatar(StartSprite):
    def update(self, ms):
        self.y += self.dir_y * ms / 1000
        if button_pressed:
            self.dir_y = -self.speed


class Cloud(StartSprite):
    def __init__(self, group, surface, x, y):
        super().__init__(group, surface, x, y)
        self.frames = []
        for i in range(12):
            animate_cloud_image1 = data.load_image(f'clouds/{i + 1}.png', -1)
            animate_cloud_image = pygame.transform.scale(animate_cloud_image1, (200, 150))
            self.frames.append(animate_cloud_image)
        self.upgrades_count = 1
        self.upgrades_per_frame = 6
        self.cur_frame = 0
        self.image = surface

    def update(self):
        self.upgrades_count += 1
        if self.upgrades_count == self.upgrades_per_frame:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.upgrades_count = 0


class AnimatedSprite(StartSprite):
    def __init__(self, group, surface, x, y, file_name):
        super().__init__(group, surface, x, y)
        self.frames = []
        self.file_name = file_name
        for i in range(15):
            animate_hero_image1 = data.load_image(f'{self.file_name}\{i + 1}.png', -1)
            animate_hero_image = pygame.transform.scale(animate_hero_image1, (96, 111))
            self.frames.append(animate_hero_image)
        self.upgrades_count = 1
        self.upgrades_per_frame = 6
        self.cur_frame = 0
        self.image = surface

    def update(self):
        self.upgrades_count += 1
        if self.upgrades_count == self.upgrades_per_frame:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.upgrades_count = 0


class Raner_hero(StartSprite):
    def __init__(self, group, surface, x, y, filename):
        super().__init__(group, surface, x, y)
        self.dir_x: float = 0
        self.ranning_frames_forward = []
        self.jumping_frames_forward = []
        self.ranning_frames_back = []
        self.jumping_frames_back = []
        self.active_frames = []
        self.frames = []
        self.jump_force = 70
        for i in range(8):
            animate_ran_hero_image1 = data.load_image(f'{filename}/{i + 1}.png', -1)
            animate_ran_hero_image = pygame.transform.scale(animate_ran_hero_image1, (96, 111))
            self.ranning_frames_forward.append(animate_ran_hero_image)
        for i in range(4):
            animate_jump_hero_image1 = data.load_image(f'jumping_hero/{i + 1}.png', -1)
            animate_jump_hero_image = pygame.transform.scale(animate_jump_hero_image1, (96, 111))
            self.jumping_frames_forward.append(animate_jump_hero_image)
        for i in range(8):
            animate_ran_hero_image1 = data.load_image(f'{filename}_mirred/{i + 1}.png', -1)
            animate_ran_hero_image = pygame.transform.scale(animate_ran_hero_image1, (96, 111))
            self.ranning_frames_back.append(animate_ran_hero_image)
        for i in range(4):
            animate_jump_hero_image1 = data.load_image(f'jumping_hero_mirred/{i + 1}.png', -1)
            animate_jump_hero_image = pygame.transform.scale(animate_jump_hero_image1, (96, 111))
            self.jumping_frames_back.append(animate_jump_hero_image)
        self.upgrades_count = 1
        self.upgrades_per_frame = 7
        self.cur_frame = 0
        self.image = surface

    def update(self, ms):
        self.upgrades_count += 1
        if self.upgrades_count == self.upgrades_per_frame:
            if self.is_grounded():
                if self.dir_x >= 0:
                    self.active_frames = self.ranning_frames_forward.copy()
                else:
                    self.active_frames = self.ranning_frames_back.copy()
                self.cur_frame = (self.cur_frame + 1) % len(self.active_frames)
                self.image = self.active_frames[self.cur_frame]
            elif not self.is_grounded():
                if self.dir_x >= 0:
                    self.active_frames = self.jumping_frames_forward.copy()
                else:
                    self.active_frames = self.jumping_frames_back.copy()
                self.cur_frame = (self.cur_frame + 1) % len(self.active_frames)
                self.image = self.active_frames[self.cur_frame]
            self.upgrades_count = 0
        self.x += self.dir_x * ms / 1000
        self.y += self.dir_y * ms / 200
        if self.is_grounded():
            self.dir_y = 0
            self.can_jump = True
        else:
            self.can_jump = False
            self.dir_y += data.gravity * ms / 100

    def is_grounded(self):
        return self.y > 370

    def set_move(self, horizontal):
        self.dir_x = horizontal * self.speed

    def jump(self):
        if self.can_jump:
            self.dir_y = -self.jump_force

#
# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y):
#         super().__init__(spriteGroup)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)
#         self.upgrades_per_frame = 10
#         self.upgrades_count = 0
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(-60, 350, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.upgrades_count += 1
#         if self.upgrades_count == self.upgrades_per_frame:
#             self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#             self.image = self.frames[self.cur_frame]
#             self.upgrades_count = 0


def main():
    clock = pygame.time.Clock()
    FPS = 120
    pygame.display.set_caption('Добро пожаловать в игру')
    clouds = pygame.sprite.Group()
    start_sprites = pygame.sprite.Group()
    play_sprites = pygame.sprite.Group()

    ground_image1 = data.load_image("Ground.jpg")
    ground_image = pygame.transform.scale(ground_image1, (1200, 700))
    ground = StartSprite(all_sprites, ground_image, 0, 400)
    ground.add(start_sprites)

    start_button_image1 = data.load_image("start_button.png", -1)
    start_button_image = pygame.transform.scale(start_button_image1, (408, 109))
    start_button = StartButton(all_sprites, start_button_image, 390, 530)
    start_button.add(start_sprites)

    cloud_image1 = data.load_image("clouds/1.png", -1)
    cloud_image = pygame.transform.scale(cloud_image1, (200, 150))

    cloud1 = Cloud(all_sprites, cloud_image, 0, 100)
    cloud1.add(clouds)
    cloud1.add(start_sprites)

    cloud2 = Cloud(all_sprites, cloud_image, 150, 50)
    cloud2.add(clouds)
    cloud2.add(start_sprites)

    cloud3 = Cloud(all_sprites, cloud_image, 340, 0)
    cloud3.add(clouds)
    cloud3.add(start_sprites)

    cloud4 = Cloud(all_sprites, cloud_image, 660, 0)
    cloud4.add(clouds)
    cloud4.add(start_sprites)

    cloud5 = Cloud(all_sprites, cloud_image, 850, 50)
    cloud5.add(clouds)
    cloud5.add(start_sprites)

    cloud6 = Cloud(all_sprites, cloud_image, 1000, 100)
    cloud6.add(clouds)
    cloud6.add(start_sprites)

    avatar_image1 = data.load_image("avatar.png", -1)
    avatar_image = pygame.transform.scale(avatar_image1, (400, 400))
    avatar = Avatar(all_sprites, avatar_image, 390, -70)
    avatar.add(start_sprites)

    image1 = data.load_image("first_hero_animation/1.png", -1)
    image = pygame.transform.scale(image1, (32, 37))
    # spining_hero = AnimatedSprite(image, 15, 1, 50, 50)
    spining_hero = AnimatedSprite(all_sprites, image, 0, 370, 'first_hero_animation')
    spining_hero.add(start_sprites)

    ran_hero = Raner_hero(all_sprites, image, 0, 370, 'raning_hero')
    ran_hero.add(play_sprites)

    cursor_image = data.load_image("arrow.png", -1)
    cursor = Sprite(all_sprites)
    cursor.image = cursor_image
    cursor.rect = cursor_image.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                create_particles(pygame.mouse.get_pos())
                start_button.check_click(event.pos)
                if button_pressed:
                    spining_hero.kill()
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            if event.type == pygame.KEYDOWN:
                if button_pressed:
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
        clouds.update()
        if avatar.rect.topleft[1] <= -300:
            avatar.kill()
        if start_button.rect.topleft[1] >= 1200:
            start_button.kill()
        if button_pressed:
            for play_sprite in play_sprites:
                play_sprite.draw(data.screen)
                play_sprite.update(clock.tick(FPS))
            pressed = pygame.key.get_pressed()
            horizontal = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
            ran_hero.set_move(horizontal)
        all_sprites.update()
        all_sprites.draw(data.screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
