import random

import pygame
import data
from pygame.sprite import Sprite
from data import all_sprites, trees, clouds, start_sprites, play_sprites

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
        self.add(start_sprites)
        self.add(clouds)
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


class Tree(StartSprite):
    def __init__(self, group, surface, x, y):
        super().__init__(group, surface, x, y)
        self.frames = []
        self.speed = 500
        self.add(start_sprites)
        self.add(trees)
        for i in range(20):
            animate_tree_image1 = data.load_image(f'tree_gif/{i + 1}.png', -1)
            animate_tree_image = pygame.transform.scale(animate_tree_image1, (200, 150))
            self.frames.append(animate_tree_image)
        self.upgrades_count = 1
        self.upgrades_per_frame = 6
        self.cur_frame = 0
        self.image = surface

    def update(self, ms, horizontal, down_flag):
        self.upgrades_count += 1
        self.speed += ms // 1000
        if self.upgrades_count == self.upgrades_per_frame:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.upgrades_count = 0
        if not down_flag:
            self.x -= (self.speed * ms / 1000 + horizontal * self.speed * ms / 2000)
        else:
            self.x -= self.speed * ms / 1000
        if self.x <= -382:
            self.x = 1200


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
        self.down_frames = []
        self.active_frames = []
        self.frames = []
        self.jump_force = 150
        self.down_flag = False
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
        for i in range(3):
            animate_down_hero_image1 = data.load_image(f'down_hero/{i + 1}.png', -1)
            animate_down_hero_image = pygame.transform.scale(animate_down_hero_image1, (96, 111))
            self.down_frames.append(animate_down_hero_image)
        self.upgrades_count = 1
        self.upgrades_per_frame = 7
        self.cur_frame = 0
        self.image = surface

    def update(self, ms):
        self.upgrades_count += 1
        if self.upgrades_count == self.upgrades_per_frame:
            if self.is_grounded():
                if self.down_flag:
                    self.active_frames = self.down_frames.copy()
                else:
                    if self.dir_x >= 0:
                        self.active_frames = self.ranning_frames_forward.copy()
                    else:
                        self.active_frames = self.ranning_frames_back.copy()
                self.cur_frame = (self.cur_frame + 1) % len(self.active_frames)
                self.image = self.active_frames[self.cur_frame]
            elif not self.is_grounded():
                if self.down_flag:
                    data.gravity = 20
                if self.dir_x >= 0:
                    self.active_frames = self.jumping_frames_forward.copy()
                else:
                    self.active_frames = self.jumping_frames_back.copy()
                self.cur_frame = (self.cur_frame + 1) % len(self.active_frames)
                self.image = self.active_frames[self.cur_frame]
            self.upgrades_count = 0
        self.x += self.dir_x * ms / 1000
        if self.x <= 0:
            self.x -= self.dir_x * ms / 1000

        self.y += self.dir_y * ms / 200
        if self.is_grounded():
            self.dir_y = 0
            self.can_jump = True
        else:
            self.can_jump = False
            self.dir_y += data.gravity * ms / 15

    def is_grounded(self):
        return self.y > 370

    def set_move(self, horizontal):
        if not self.down_flag:
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


class Count(Sprite):
    def __init__(self, group):
        super(Count, self).__init__()
        self.time = 0
        self.group = group
        self.count = 0
        self.koef = 1

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"{int(self.count)}", True, 'black')
        text_x = 1100 - text.get_width() // 2
        text_y = text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def update(self, ms):
        self.koef += 0.0005
        self.time += ms
        self.count = self.time * self.koef


def main():
    clock = pygame.time.Clock()
    FPS = 120
    pygame.display.set_caption('Добро пожаловать в игру')

    count = Count(all_sprites)

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

    cloud2 = Cloud(all_sprites, cloud_image, 150, 50)

    cloud3 = Cloud(all_sprites, cloud_image, 340, 0)

    cloud4 = Cloud(all_sprites, cloud_image, 660, 0)

    cloud5 = Cloud(all_sprites, cloud_image, 850, 50)

    cloud6 = Cloud(all_sprites, cloud_image, 1000, 100)

    tree_image1 = data.load_image("tree_gif/1.png", -1)
    tree_image = pygame.transform.scale(tree_image1, (200, 150))

    tree1 = Tree(all_sprites, tree_image, 0, 252)

    tree2 = Tree(all_sprites, tree_image, 300, 252)

    tree3 = Tree(all_sprites, tree_image, 600, 252)

    tree4 = Tree(all_sprites, tree_image, 900, 252)

    tree5 = Tree(all_sprites, tree_image, 1200, 252)

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
        pressed = pygame.key.get_pressed()
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
        horizontal = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
        if avatar.rect.topleft[1] <= -300:
            avatar.kill()
        if start_button.rect.topleft[1] >= 1200:
            start_button.kill()
        if button_pressed:
            for play_sprite in play_sprites:
                play_sprite.draw(data.screen)
                play_sprite.update(clock.tick(FPS))
                trees.update(clock.tick(FPS), horizontal, ran_hero.down_flag)
            if pressed[pygame.K_s]:
                ran_hero.down_flag = True
            elif not pressed[pygame.K_s]:
                ran_hero.down_flag = False
            count.update(clock.tick(FPS))
            count.draw(data.screen)
            ran_hero.set_move(horizontal)
        all_sprites.update()
        all_sprites.draw(data.screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
