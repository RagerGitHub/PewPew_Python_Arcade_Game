# A game where a player has to shoot objects that will kill you if they touch you made with python arcade
# 1/26/23
__author__ = 'Tyler Slomianyj'

# Projects modified from these URLs
# https://api.arcade.academy/en/latest/examples/sprite_collect_coins_move_bouncing.html#sprite-collect-coins-move-bouncing
# https://api.arcade.academy/en/latest/examples/timer.html
# https://api.arcade.academy/en/latest/examples/sprite_bullets.html#sprite-bullets
# Artwork from https://kenney.nl
import random
import arcade

# constants

SPRITE_SCALING = 0.75
SPRITE_SCALING_LASER = 1.25
SPRITE_SCALING_ENEMY = 0.2

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Boom Boom 123"

MOVEMENT_SPEED = 10
BULLET_SPEED = 15
BULLET_COOLDOWN_TICKS = 8

class Enemy(arcade.Sprite):

    def update(self):
        # Move enemies.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 1
            self.change_x *= -1

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 2
            self.change_x *= -1

        if self.bottom < 0:
            self.bottom = 1
            self.change_y *= -1

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 2
            self.change_y *= -1

class Player(arcade.Sprite):

    def update(self):

        # Move player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds

        if self.left < 0:

            self.left = 0
            self.change_x = -self.change_x

        elif self.right > SCREEN_WIDTH:

            self.right = SCREEN_WIDTH
            self.change_x = -self.change_x

        if self.bottom < 0:

            self.bottom = 0
            self.change_y = -self.change_y

        elif self.top > SCREEN_HEIGHT:

            self.top = SCREEN_HEIGHT
            self.change_y = -self.change_y

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.level = 1

        # Hide cursor
        self.set_mouse_visible(False)
        self.bullet_cooldown = 0

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Score
        self.score = 0

        # timer
        self.total_time = 0.0

        # Set up the player
        self.player_sprite = Player(":resources:images/space_shooter/playerShip1_orange.png", SPRITE_SCALING)
        self.player_sprite.center_x = 1/2*SCREEN_WIDTH
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Spawn enemies
        for i in range((self.level*2 + 3)):


            # Create enemy sprite
            enemy = Enemy(":resources:images/enemies/saw.png", SPRITE_SCALING_ENEMY)
            enemy.center_x = random.randrange(45, SCREEN_WIDTH-45)
            enemy.center_y = random.randrange(150, SCREEN_HEIGHT)
            enemy.change_x = random.randint(-5, 5)
            enemy.change_y = random.randint(-5, 5)


            # Append enemy to sprite list
            self.enemy_list.append(enemy)



    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()


        # Draw level and timer
        arcade.draw_text(f"Level: {self.level}", 10, 20, arcade.color.WHITE, 14)
        minutes = int(30-self.total_time) // 60

        # Calculate seconds by using a modulus
        seconds = int(30 -self.total_time) % 60

        # Figure out your output
        output = f"Time left: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, 1/2 * SCREEN_WIDTH - 60, SCREEN_HEIGHT-40, arcade.color.RED, 15)

    def update_enemy_speed(self):

        for i in self.enemy_list:
            i.update()

    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """



        # If the player presses a key, update the speed
        if key == arcade.key.A:

            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.D:

            self.player_sprite.change_x = MOVEMENT_SPEED

        elif key == arcade.key.SPACE:
            if self.bullet_cooldown < BULLET_COOLDOWN_TICKS:
                return
            self.bullet_cooldown = 0

            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            # The image points to the right, and we want it to point up. So
            # rotate it.
            bullet.angle = 90

            # Give the bullet a speed
            bullet.change_y = BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):

        """Called when the user releases a key. """



        # If a player releases a key, zero out the speed.

        # This doesn't work well if multiple keys are pressed.

        # Use 'better move by keyboard' example if you need to

        # handle this.

        if key == arcade.key.A or key == arcade.key.D:

            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on bullet sprites
        self.bullet_list.update()
        #self.update_enemy_speed()
        self.update_enemy_speed()

        #for enemy in self.enemy_list:
            #enemy.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
        #quitting if player touches enemy
        for enemy in self.enemy_list:
            player_death = arcade.check_for_collision_with_list(enemy, self.player_list)
            if len(player_death) > 0:
                quit()
        self.total_time += delta_time
        if len(self.enemy_list) == 0:
            self.level += 1
            self.total_time = 0
            for i in range((self.level * 2 + 3)):
                # Create enemy sprite
                enemy = Enemy(":resources:images/enemies/saw.png", SPRITE_SCALING_ENEMY)
                enemy.center_x = random.randrange(45, SCREEN_WIDTH - 45)
                enemy.center_y = random.randrange(150, SCREEN_HEIGHT)
                enemy.change_x = random.randint(-5, 5)
                enemy.change_y = random.randint(-5, 5)

                # Append enemy to sprite list
                self.enemy_list.append(enemy)

                # If the bullet flies off-screen, remove it.
                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()
        # if the timer runs out, quit
        if 30 - self.total_time < 0:
            quit()


        # part of bullet cooldown
        self.bullet_cooldown += 1




        # Move the player

        self.player_list.update()




def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()