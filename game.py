import arcade, random

# TODO: PLACEHOLDERS(BG, PLAYER SPRITE, ENEMY SPRITE)
# TODO: ENEMIES(MOVEMENT, LIFE, ATTACKING, ENEMY PATTERNS, SFX)
# TODO: PLAYER(ABILITIES)
# TODO: GAME("LEVELS", WIN CONDITIONS, MAIN MENU)


# CONSTANTS
# SYSTEM
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SPRITE SCALING
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_BULLET = 0.5
SPRITE_SCALING_ENEMY = 0.8

SPRITE_SCALING_COIN = 0.5

# GAME
COIN_COUNT = 50
BULLET_SPEED = 15
MOVEMENT_SPEED = 10

# SOUND EFFECTS
PLAYER_GUN_SOUND = arcade.load_sound("sound/sfx_laser.ogg")


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
        self.wave = 0

        self.screen_view = 1

        self.set_mouse_visible(False)
        self.background = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.background = arcade.load_texture("images/bg_ground.png")

        self.lifepoints = 5
        self.score = 0
        self.wave = 0

        # Player Sprite - PLACEHOLDER
        self.player_sprite = arcade.Sprite("images/playerShip1_blue.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()

        # Background
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Start screen
        if self.screen_view == 1:
            self.start_screen()
        # Lose screen
        elif self.screen_view == 2:
            self.lose_screen()
        # Game screen
        elif self.screen_view == 0:

            self.player_list.draw()
            self.bullet_list.draw()
            self.enemy_list.draw()

            # Score
            score_text = f"Score {self.score}"
            arcade.draw_text(score_text, 10, 20, arcade.color.WHITE, 12)
            # Lifepoints
            lifepoints_text = f"Life {self.lifepoints}"
            arcade.draw_text(lifepoints_text, 10, 40, arcade.color.WHITE, 12)
            # Wave
            wave_text = f"Wave {self.wave}"
            arcade.draw_text(wave_text, 10, 60, arcade.color.WHITE, 12)

    def on_key_press(self, key, mod):
        # GAME SCREEN
        if self.screen_view == 0:
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
                arcade.play_sound(PLAYER_GUN_SOUND)

        # START SCREEN
        if key == arcade.key.SPACE and self.screen_view == 1:
            # Game Screen view
            self.screen_view = 0

        # LOSE SCREEN
        if self.screen_view == 2:
            # Restart
            if key == arcade.key.ENTER:
                self.setup()
                self.screen_view = 1
            # Lose
            if key == arcade.key.ESCAPE:
                arcade.close_window()

    def on_key_release(self, key, modifiers):
        # GAME SCREEN
        if self.screen_view == 0:
            # Move left
            if key == arcade.key.LEFT:
                # If player has pressed the right key before releasing left key - keeps going right
                if self.player_dx > 0:
                    pass
                else:
                    self.player_dx = 0
            # Move right
            if key == arcade.key.RIGHT:
                # If player has pressed the left key before releasing right key - keeps going left
                if self.player_dx < 0:
                    pass
                else:
                    self.player_dx = 0

    def update(self, delta_time):
        # If the player still has lives remaining and the screen is on the game screen
        if self.screen_view == 0:
            if len(self.enemy_list) == 0:
                # Increase wave
                self.wave += 1
                # Enemy Spawning
                enemy_count = random.randrange(self.wave, (self.wave + 4))
                for i in range(enemy_count):
                    enemy = Enemy("images/spider.png", SPRITE_SCALING_ENEMY)
                    enemy.center_x = random.randrange(SCREEN_WIDTH)
                    enemy.center_y = SCREEN_HEIGHT + enemy.height
                    enemy.change_x = random.randrange(-3, 4)
                    enemy.change_y = random.randrange(-3, -1)
                    self.enemy_list.append(enemy)

            self.enemy_list.update()
            self.bullet_list.update()

            # If player hits the edge of the screen
            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            elif self.player_sprite.right > SCREEN_WIDTH - 1:
                self.player_sprite.right = SCREEN_WIDTH

            # Update Player Position
            self.player_sprite.center_x += self.player_dx

            # Checks if any bullets does something
            for b in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(b, self.enemy_list)
                # If bullet goes above window, remove.
                if b.bottom > SCREEN_HEIGHT:
                    b.kill()
                # If bullet hits enemy, remove.
                if len(hit_list) > 0:
                    b.kill()
                # Remove the enemy hit.
                for e in hit_list:
                    e.kill()
                    self.score += 1
            # If the enemy moves below window, remove. Player loses life.
            for e in self.enemy_list:
                if e.top < 0:
                    self.lifepoints -= 1
                    e.kill()

        if self.lifepoints <= 0:
            self.screen_view = 2

    # SCREENS
    # Start Screen
    def start_screen(self):
        # Base Rectangle
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 600, 300, arcade.color.WHITE)
        # "text", start_x, start_y, colour, size, alignment, x anchor point, y anchor point
        arcade.draw_text(("SPACE TO START"), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.AIR_FORCE_BLUE, 50, align="center", anchor_x="center", anchor_y="center")

    # Lose Screen
    def lose_screen(self):
        # Main text
        arcade.draw_text(("YOU LOSE"), SCREEN_WIDTH / 2, 445, arcade.color.WHITE, 77, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text((f"SCORE: {self.score}"), SCREEN_WIDTH / 2, 380, arcade.color.WHITE, 25, align="center", anchor_x="center", anchor_y="center")
        # Play Again Button
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, 310, 400, 100, arcade.color.GREEN)
        arcade.draw_text(("Enter to Play Again"), SCREEN_WIDTH / 2, 310, arcade.color.WHITE, 25, align="center", anchor_x="center", anchor_y="center")
        # Quit Button
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, 205, 400, 100, arcade.color.RED)
        arcade.draw_text(("Escape to Quit"), SCREEN_WIDTH / 2, 205, arcade.color.WHITE, 25, align="center", anchor_x="center", anchor_y="center")


# Main function to start the game window
def main():
    window = Game()
    window.setup()
    arcade.run()


main()
