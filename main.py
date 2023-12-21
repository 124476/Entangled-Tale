import datetime
import os
import random
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def newDialog():
    font_path = os.path.join("data/fonts", "comic.ttf")
    font = pygame.font.Font(font_path, 20)
    render_fraze_1 = font.render('', True, (255, 255, 255))
    render_fraze_2 = font.render('', True, (255, 255, 255))
    render_fraze_3 = font.render('', True, (255, 255, 255))
    return render_fraze_1, render_fraze_2, render_fraze_3


def mathGame():
    global background, all_sprites, player_group, player, door, \
        door_group, rectangle_group, loc5
    fon = pygame.transform.scale(load_image('a1_m4.png'), (800, 500))
    screen.blit(fon, (0, 0))

    a = random.randint(0, 100)
    difference = random.randint(0, 9)
    b = difference - a
    fraze_1 = 'Я великий маг этого подземелья,'
    fraze_2 = 'и я никому не дам ходить по нему'
    fraze_3 = 'без моего разрешения!'
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))
    font_path = os.path.join("data/fonts", "comic.ttf")
    font = pygame.font.Font(font_path, 20)
    render_fraze_1, render_fraze_2, render_fraze_3 = newDialog()

    win = False
    i = 1
    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and k == 0:
                    screen.fill((0, 0, 0))
                    screen.blit(fon, (0, 0))
                    if b < 0:
                        question = f"{a}{b}"
                    else:
                        question = f"{a} + {b}"
                    fraze_1 = 'Но ты можешь попытать удачу,'
                    fraze_2 = 'и решить мою задачу'
                    fraze_3 = 'сколько будет: ' + question
                    render_fraze_1, render_fraze_2, render_fraze_3 = (
                        newDialog())
                    i = 1
                    k = 1
                elif 48 <= event.key <= 58 and k == 1:
                    fraze_1 = event.key - 48
                    render_fraze_1, render_fraze_2, render_fraze_3 = (
                        newDialog())
                    if fraze_1 == difference:
                        screen.fill((0, 0, 0))
                        screen.blit(fon, (0, 0))
                        fraze_1 = 'Я вижу, что ты неплох в математике'
                        fraze_2 = 'на этот раз я тебя пропускаю,'
                        fraze_3 = 'но мы еще встретимся!'
                        win = True
                    else:
                        screen.fill((0, 0, 0))
                        screen.blit(fon, (0, 0))
                        fraze_1 = 'Я вижу, что ты слаб,'
                        fraze_2 = 'возвращайся,'
                        fraze_3 = 'лишь когда будешь достоин'
                    i = 1
                    k = 2
                elif event.key == pygame.K_z and k == 2:
                    if win:
                        all_sprites = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        rectangle_group = pygame.sprite.Group()
                        background = Background('a1_m5.png', (900, 784))
                        all_sprites.add(background)
                        player = Player(450, 300, 1)
                        player.loc = 4

                        loc5 = 0
                        camera.update(player)
                        door = Door(20000, 20000, 1)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                        return
                    else:
                        end_screen(1, False)
                        return

        if i <= len(fraze_1):
            render_fraze_1 = font.render(fraze_1[:i], True, (255, 255, 255))
        elif i <= len(fraze_1) + len(fraze_2):
            render_fraze_2 = font.render(fraze_2[:i - len(fraze_1)], True,
                                         (255, 255, 255))
        elif i <= len(fraze_1) + len(fraze_2) + len(fraze_3):
            render_fraze_3 = font.render(
                fraze_3[:i - len(fraze_1) - len(fraze_2)], True,
                (255, 255, 255))
        i += 1
        screen.blit(render_fraze_1, (230, 85))
        screen.blit(render_fraze_2, (230, 115))
        screen.blit(render_fraze_3, (230, 145))
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(20)
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(0.7)
    fon = pygame.transform.scale(load_image('blackfon.png'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type ==
                  pygame.MOUSEBUTTONDOWN):
                if True:
                    act1()
                    return
        clock.tick(FPS)


def end_screen(n, winOrdie):
    fon = pygame.transform.scale(load_image('gameover.jpg'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()

    font_path = os.path.join("data/fonts", "comic.ttf")
    font = pygame.font.Font(font_path, 35)
    if winOrdie:
        t = font.render(f"Win", True, (0, 0, 0))
    else:
        t = font.render(f"Lose", True, (0, 0, 0))
    tm = (datetime.datetime.now() - time).total_seconds()
    t2 = font.render(f"{int(tm // 60)} min {int(tm - (tm // 60) * 60)} sec",
                     True, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type ==
                  pygame.MOUSEBUTTONDOWN):
                if True:
                    if n == 1:
                        act1()
                    elif n == 2:
                        act2()
                    elif n == 3:
                        act3()
                    return

        screen.blit(t, (300, 200))
        screen.blit(t2, (300, 300))
        pygame.display.flip()
        clock.tick(FPS)


def act1():
    global all_sprites, player_group, player, background, door, door_group, \
        i, word_group, x, y, loc5, time
    time = datetime.datetime.now()
    fon = pygame.transform.scale(load_image('act1.png'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    background = Background('a1_m1.png', (1360, 760))
    door = Door(1180, 440, 1)
    all_sprites.add(background)
    door_group.add(door)
    player = Player(290, 470, 1)
    word_group = pygame.sprite.Group()
    x, y = 0, 0
    loc5 = 0
    i = 0
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)


def act2():
    global all_sprites, player_group, player, background, door, \
        door_group, time
    time = datetime.datetime.now()
    fon = pygame.transform.scale(load_image('act2.png'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(1)

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    background = Background('a2_m1.jpg', (3000, 1500))
    door = Door(580, 640, 2)
    door2 = Door(1860, 640, 2)
    all_sprites.add(background)
    door_group.add(door)
    door_group.add(door2)
    player = Player(1090, 720, 2)
    player.loc = 6
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)


def act3():
    fon = pygame.transform.scale(load_image('act3.png'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    clock.tick(1)


def menu():
    fon = pygame.transform.scale(load_image('Menu.png'), (800, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    act1()
                    return
                if event.key == pygame.K_2:
                    act2()
                    return
                if event.key == pygame.K_3:
                    act3()
                    return
                if event.key == pygame.K_p:
                    return

        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    image = load_image('m.c.front_stop.jpg')
    image = pygame.transform.scale(image, (40, 60))

    def __init__(self, pos_x, pos_y, stena):
        super().__init__(player_group, all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.x = pos_x + 20
        self.y = pos_y + 60
        self.step = 1
        self.back = False
        self.last_skin_change_time = 0
        self.direction = ''
        self.mask = pygame.mask.from_surface(self.image)
        self.loc = 0
        if stena == 1:
            self.stena = [(2, 0, 0)]
        elif stena == 2:
            self.stena = [(34, 177, 76), (0, 162, 232)]

    def stop(self):
        image = self.image
        if self.direction == 'left':
            image = load_image(f'm.c.left_stop.jpg')
        elif self.direction == 'right':
            image = load_image(f'm.c.right_stop.jpg')
        elif self.direction == 'down':
            image = load_image(f'm.c.front_stop.jpg')
        elif self.direction == 'up':
            image = load_image(f'm.c.back_stop.jpg')
        self.image = pygame.transform.scale(image, (40, 60))

    def update(self, move_up, move_down, move_left, move_right):
        global all_sprites, background, player, player_group, door_group, \
            door, word_group, x, y
        image = self.image
        current_time = pygame.time.get_ticks()
        if move_left:
            self.direction = 'left'
            self.rect.x -= 5
            self.x -= 5
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.x += 5
                self.x += 5
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True

            image = load_image(f'm.c.left_walk_{self.step}.jpg')
        if move_right:
            self.direction = 'right'
            self.rect.x += 5
            self.x += 5
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.x -= 5
                self.x -= 5
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True

            image = load_image(f'm.c.right_walk_{self.step}.jpg')
        if move_up:
            self.direction = 'up'
            self.rect.y -= 5
            self.y -= 5
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.y += 5
                self.y += 5
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True

            image = load_image(f'm.c.back_walk_{self.step}.jpg')
        if move_down:
            self.direction = 'down'
            self.rect.y += 5
            self.y += 5
            if background.get_rgb(self.x, self.y) in self.stena:
                self.rect.y -= 5
                self.y -= 5
            if current_time - self.last_skin_change_time > 150:
                self.last_skin_change_time = current_time
                if self.step == 1:
                    self.step += 1
                    self.back = False
                elif self.step == 2:
                    if self.back:
                        self.step -= 1
                    else:
                        self.step += 1
                elif self.step == 3:
                    self.step -= 1
                    self.back = True

            image = load_image(f'm.c.front_walk_{self.step}.jpg')
        self.image = pygame.transform.scale(image, (40, 60))
        if pygame.sprite.collide_mask(self, door):
            if self.loc == 0:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('a1_m2.png', (600, 1300))
                all_sprites.add(background)
                player = Player(240, 950, 1)
                player.loc = 1
                wizardRus.rect.x = 240
                wizardRus.rect.y = 600
                wizardRus.canRun = False
                wizardRus.y = 600
                all_sprites.add(wizardRus)
                door = Door(240, 100, 1)
            elif self.loc == 1:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                word_group = pygame.sprite.Group()
                door_group = pygame.sprite.Group()
                background = Background('a1_m3.png', (2100, 500))
                all_sprites.add(background)
                door = Door(1800, 200, 1)
                player = Player(200, 330, 1)
                player.loc = 2
            elif self.loc == 2:
                all_sprites = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                background = Background('a1_m4.jpg', (700, 500))
                all_sprites.add(background)
                player = Player(375, 300, 1)
                player.loc = 3
                mathGame()
                x = player.x
                y = player.y
            elif self.loc == 5:
                door.rect.x = 20000
                self.loc = 6
                end_screen(2, True)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


class Letters(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        a = random.choice(['letter_a.png', 'letter_b.png', 'letter_v.png',
                           'letter_g.png', 'letter_d.png'])
        image_path = load_image(a)
        self.image = pygame.transform.scale(image_path, (40, 60))
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.rect.x -= 9
        if pygame.sprite.collide_mask(self, player):
            end_screen(1, False)
            return


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path, size):
        super().__init__()
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_threshold(self.image, (237, 28, 36),
                                               (1, 1, 1, 255))

    def get_rgb(self, x, y):
        pixel = pygame.PixelArray(self.image)
        return self.image.unmap_rgb(pixel[x][y])


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tip):
        super().__init__(all_sprites)
        if tip == 1:
            image_path = load_image('exit-enter_a1.png')
        elif tip == 2:
            image_path = load_image('exit-enter_a2.png')
        self.image = pygame.transform.scale(image_path, (120, 96))
        self.rect = self.image.get_rect().move(pos_x, pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vx, vy, xx, yy, canDamage):
        if canDamage:
            image_path = load_image('redrect.jpg')
        else:
            image_path = load_image('warning rect.png')
        image_path = pygame.transform.scale(image_path, (xx, yy))
        sprite_image = image_path
        super().__init__(rectangle_group, all_sprites)
        self.image = sprite_image
        self.rect = self.image.get_rect().move(pos_x, pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = vx
        self.vy = vy
        self.canDamage = canDamage

    def update(self):
        global rectangle_group
        self.rect.x += 2 * self.vx
        self.rect.y += 2 * self.vy
        if self.canDamage:
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.x = 10000
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x = 10000

            if pygame.sprite.collide_mask(self, player):
                for j in rectangle_group:
                    j.rect.x = 10000

                rectangle_group = pygame.sprite.Group()
                end_screen(1, False)
                return


class wizardRus(pygame.sprite.Sprite):
    image = load_image('wizardRus.png')
    image = pygame.transform.scale(image, (80, 90))

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = wizardRus.image
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.canRun = False
        self.y = pos_y

    def update(self):
        if self.canRun:
            self.rect.y -= 10
            self.y -= 10
            if self.y <= 300:
                self.rect.y = -1000
        if player.y <= 800:
            self.canRun = True


wizardRus = wizardRus(2000, 2000)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


clock = pygame.time.Clock()
FPS = 60
# группы спрайтов
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
rectangle_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
word_group = pygame.sprite.Group()

time = datetime.datetime.now()
x, y = 0, 0
rect = Rectangle(20000, 20000, 0, 0, 10, 500, False)

loc5 = 0
camera = Camera()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Entangled Tale')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    start_screen()

    i = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    menu()
            if event.type == pygame.KEYUP:
                player.stop()
        keys = pygame.key.get_pressed()

        screen.fill((2, 0, 0))
        # Обновление игровых объектов
        player.update(keys[pygame.K_UP], keys[pygame.K_DOWN],
                      keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
        player.update(keys[pygame.K_w], keys[pygame.K_s],
                      keys[pygame.K_a], keys[pygame.K_d])
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        camera.update(player)
        wizardRus.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        if player.loc == 2:
            i += 1
            if i % 40 == 0:
                letter = Letters(x - player.x + 2500,
                                 random.randint(y - player.y + 450,
                                                y - player.y + 660))
                word_group.add(letter)
            word_group.update()
            word_group.draw(screen)
        if player.loc == 4:
            if loc5 <= 1000 and loc5 % 200 == 0:
                try:
                    n = random.randint(-1, 3) * 200
                    while n == m:
                        n = random.randint(-1, 3) * 200
                    m = n
                except:
                    m = random.randint(-1, 3) * 200
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, False)
            if loc5 <= 1000 and loc5 % 200 == 140:
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, True)
            if 1000 <= loc5 <= 3000 and loc5 % 100 == 0:
                rect.rect.x = 20000
                Rectangle(x - player.x + 800,
                          y - player.y + random.randint(-100, 150), -3, 0, 10,
                          random.randint(50, 300), True)
            if 3200 <= loc5 <= 4000 and loc5 % 200 == 0:
                n = random.randint(-1, 3) * 200
                while n == m:
                    n = random.randint(-1, 3) * 200
                m = n
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, False)
            if 3200 <= loc5 <= 4140 and loc5 % 200 == 140:
                rect.rect.x = 20000
                rect = Rectangle(x - player.x + m,
                                 y - player.y - 78, 0, 0, 450,
                                 519, True)
            if loc5 == 4200:
                rect.rect.x = 20000
            if loc5 == 4400:
                door = Door(350, 150, 1)
                player.loc = 5
            loc5 += 1

            rectangle_group.update()
        door_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
