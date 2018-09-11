import arcade, random

# TODO: PLACEHOLDERS(BG, PLAYER SPRITE, ENEMY SPRITE)
# TODO: ENEMIES(MOVEMENT, LIFE, ATTACKING, ENEMY PATTERNS)
# TODO: PLAYER(ABILITIES)
# TODO: GAME("LEVELS", WIN/LOSE CONDITIONS)


# CONSTANTS
# SYSTEM
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE SCALING
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_BULLET = 0.5

SPRITE_SCALING_COIN = 0.5

# GAME
COIN_COUNT = 50
BULLET_SPEED = 15
MOVEMENT_SPEED = 10


class Enemy(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1
        if self.right > SCREEN_WIDTH:
            self.change_x *= -1


class Bullet(arcade.Sprite):
    def update(self):
        self.center_y += BULLET_SPEED


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Tartarus")

        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None

        self.player_sprite = None
        self.bullet_sprite = None
        self.enemy_sprite = None

        self.lifepoints = 5
        self.score = 0
        self.player_dx = 0

        self.set_mouse_visible(False)
        # Background - PLACEHOLDER
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.lifepoints = 5

        # Player Sprite - PLACEHOLDER
        self.player_sprite = arcade.Sprite("images/playerShip1_blue.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        # Score
        score_text = f"Score {self.score}"
        arcade.draw_text(score_text, 10, 20, arcade.color.WHITE, 12)
        # Lifepoints
        lifepoints_text = f"Life {self.lifepoints}"
        arcade.draw_text(lifepoints_text, 10, 40, arcade.color.WHITE, 12)

    def on_key_press(self, key, mod):
        # Movement
        if key == arcade.key.LEFT:
            self.player_dx = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.player_dx = MOVEMENT_SPEED

        # Shoot Bullets
        if key == arcade.key.SPACE:
            bullet = Bullet("images/laserBlue01.png", SPRITE_SCALING_BULLET)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            if self.player_dx > 0:
                pass
            else:
                self.player_dx = 0
        if key == arcade.key.RIGHT:
            if self.player_dx < 0:
                pass
            else:
                self.player_dx = 0

    def update(self, delta_time):
        if len(self.enemy_list) == 0:
            # Enemy Spawning
            enemy_count = random.randrange(3, 12)
            for i in range(enemy_count):
                enemy = Enemy("images/spider.png", SPRITE_SCALING_PLAYER)
                enemy.center_x = random.randrange(SCREEN_WIDTH)
                enemy.center_y = SCREEN_HEIGHT + enemy.height
                enemy.change_x = random.randrange(-3, 4)
                enemy.change_y = random.randrange(-4, -1)
                self.enemy_list.append(enemy)

        self.enemy_list.update()
        self.bullet_list.update()
        # Update Player Position
        self.player_sprite.center_x += self.player_dx
        # If player hits the edge of the screen
        if self.player_sprite.center_x == SCREEN_WIDTH or self.player_sprite.center_x == 0:
            self.player_dx = 0

        for b in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(b, self.enemy_list)

            if b.bottom > SCREEN_HEIGHT:
                b.kill()

            if len(hit_list) > 0:
                b.kill()

            for e in hit_list:
                e.kill()
                self.score += 1

        for e in self.enemy_list:
            if e.top < 0:
                self.lifepoints -= 1
                e.kill()


def main():
    window = Game()
    window.setup()
    arcade.run()


main()
