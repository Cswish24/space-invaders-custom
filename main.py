import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player_ufo.png')
        self.rect = self.image.get_rect(midbottom=(600, 780))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.left -= 1
        if keys[pygame.K_RIGHT] and self.rect.right <= 1200:
            self.rect.right += 1

    def update(self):
        self.player_input()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('graphics/enemy_ufo.png')
        self.rect = self.image.get_rect(midbottom=position)
        self.velocity_x = 1
        self.adjust_y = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.adjust_y
        self.adjust_y = 0


class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        super().__init__()
        self.image = pygame.image.load('graphics/player_bullet.png')
        self.rect = self.image.get_rect(midbottom=player_pos)
        self.velocity = -2

    def destroy_bullet(self):
        if self.rect.y < -10:
            self.kill()

    def update(self):
        self.rect.y += self.velocity
        self.destroy_bullet()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, enemy_pos):
        super().__init__()
        self.image = pygame.image.load('graphics/enemy_bullet.png')
        self.rect = self.image.get_rect(midtop=enemy_pos)
        self.velocity = 2

    def destroy_bullet(self):
        if self.rect.y > 810:
            self.kill()

    def update(self):
        self.rect.y += self.velocity
        self.destroy_bullet()


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/brick.png')
        self.rect = self.image.get_rect(midtop=pos)


# ---------------Basic configurations-----------------
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 100)
game_active = True
start_time = 0
score = 0
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops = -1)

# ------------Object Groups-------------------
player = pygame.sprite.GroupSingle()
player_bullet = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
bricks = pygame.sprite.Group()
player.add(Player())


# -----------creates brick obstacles------------------
for x in range(100, 1100, 40):
    for y in range(200, 600, 40):
        bricks.add(Brick((x, y)))

for x in range(110, 1110, 40):
    for y in range(190, 590, 40):
        bricks.add(Brick((x, y)))

# ------------creates enemy postions--------------------
ypos = 60
for y in range(3):
    xpos = 180
    for x in range(15):
        enemies.add(Enemy((xpos, ypos)))
        xpos += 60
    ypos += 40

sky_surface = pygame.image.load('graphics/sky.png').convert()

# ------------------main game loop---------------------------
while True:

    for event in pygame.event.get():
        # --------------allows exiting game----------------------
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # --------------creates bullets on space key press-----------
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(player_bullet) < 3:
                player_bullet.add(Player_Bullet(player.sprite.rect.midtop))

    if game_active:
        # ----------------collsion detection-------------------
        for bullet in player_bullet:
            if pygame.sprite.spritecollide(bullet, enemies, True):
                bullet.kill()

        for bullet in player_bullet:
            if pygame.sprite.spritecollide(bullet, bricks, True):
                bullet.kill()

        for bullet in enemy_bullets:
            if pygame.sprite.spritecollide(bullet, bricks, True):
                bullet.kill()

        for bullet in player_bullet:
            if pygame.sprite.spritecollide(bullet, enemy_bullets, True):
                bullet.kill()

        if pygame.sprite.spritecollide(player.sprite, enemy_bullets, False):
            game_active = False

        # --------------------end collision detection-------------------------

        # --------------------enemy mechanics change---------------------------
        enemy_velocity_change = False

        for enemy in enemies:
            if enemy.rect.x < 10 or enemy.rect.x > 1160:
                enemy_velocity_change = True
                break

        if enemy_velocity_change:
            for enemy in enemies:
                enemy.velocity_x *= -1
        for enemy in enemies:
            if randint(0, len(enemies)*100) == 5:
                enemy_bullets.add(EnemyBullet(enemy_pos=enemy.rect.midbottom))
        # --------------------end enemy mechanics change----------------------

        # --------------------draw and update---------------------------------
        screen.blit(sky_surface, (0, 0))

        player.draw(screen)
        player.update()

        enemies.draw(screen)
        enemies.update()

        bricks.draw(screen)
        bricks.update()

        player_bullet.draw(screen)
        player_bullet.update()

        enemy_bullets.draw(screen)
        enemy_bullets.update()
        # ----------------------end draw and update---------------------------

        # ----------------------check for end of game-------------------------
        if not bool(enemies) or not bool(player):
            game_active = False

        if not game_active:
            score_message = test_font.render(
                f'Game Over', False, (255, 255, 255))
            score_message_rect = score_message.get_rect(center=(600, 330))
            screen.blit(score_message, score_message_rect)

        # ----------------------end check for end of game---------------------

    # -----------------------frame rate control-----------------------------
    pygame.display.update()
    clock.tick(200)
