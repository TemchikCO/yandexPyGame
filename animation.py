import pygame
import data

spriteGroup = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(spriteGroup)
        self.frames = []
        self.cloud_frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.upgrades_per_frame = 20
        self.upgrades_count = 0
        for i in range(11):
            self.cloud_frames.append('data')

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.upgrades_count += 1
        if self.upgrades_count == self.upgrades_per_frame:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.upgrades_count = 0


image1 = data.load_image("many_bird.png", -1)
image = pygame.transform.scale(image1, (400, 400))
spining_hero = AnimatedSprite(image, 8, 3, 50, 50)

running = True
clock = pygame.time.Clock()
FPS = 120
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    data.screen.fill((255, 255, 0))
    spriteGroup.draw(data.screen)
    spriteGroup.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
