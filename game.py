import arcade, random

# TODO: PLACEHOLDERS(BG, PLAYER SPRITE, ENEMY SPRITE)

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

        self.score = 0
        self.player_dx = 0

        self.set_mouse_visible(False)
        # Background - PLACEHOLDER
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()

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
        self.bullet_list.update()
        # Update Player Position
        self.player_sprite.center_x += self.player_dx
        # If player hits the edge of the screen
        if self.player_sprite.center_x > SCREEN_WIDTH or self.player_sprite.center_x < 0:
            self.player_dx = 0

        for b in self.bullet_list:
            if b.bottom > SCREEN_HEIGHT:
                b.kill()


def main():
    window = Game()
    window.setup()
    arcade.run()


main()
