"""
Sprite Follow Player 2

This calculates a 'vector' towards the player and randomly updates it based
on the player's location. This is a bit more complex, but more interesting
way of following the player.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_follow_simple_2
"""

import random
import arcade
import math
import os

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 10
COIN_SPEED = 1.0
PLAYER_COUNT = 5
MAX_PLAYER = 30

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Sprite Follow Player Simple Example 2"

SPRITE_SPEED = 0.5


class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """
    def __init__(self, *args):
        super(Coin, self).__init__(*args)
        self.breed_point = 0
        self.hungry_point = 500

    def hunger(self):
        if self.hungry_point <= 0:
            self.kill()
        else:
            self.hungry_point -= 1

    def breed(self):
        if self.breed_point >= 600:
            new_coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)
            new_coin.center_x = self.center_x + random.randrange(-2, 2)
            new_coin.center_y = self.center_y + random.randrange(-2, 2)
            self.breed_point = 0
            return new_coin
        else:
            self.breed_point += 1
        return 1

    def find_closest(self, player_list):
        min_dist = 10000
        closest = None
        for player_sprite in player_list:
            x_diff = player_sprite.center_x - self.center_x
            y_diff = player_sprite.center_y - self.center_y
            distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = player_sprite
        return closest

    def follow_sprite(self, player_list):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """
        player_sprite = self.find_closest(player_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * COIN_SPEED
            self.change_y = math.sin(angle) * COIN_SPEED


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Character image from kenney.nl
        for i in range(PLAYER_COUNT):
            player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                          SPRITE_SCALING_PLAYER)
            player_sprite.center_x = random.randrange(SCREEN_WIDTH)
            player_sprite.center_y = random.randrange(SCREEN_HEIGHT)
            player_sprite.change_x = 0.6
            player_sprite.change_y = 0.4
            player_sprite.breed_point = 0
            self.player_list.append(player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.coin_list.draw()
        self.player_list.draw()
        for i, player in enumerate(self.player_list):
            output = f"Score: {player.breed_point}"
            arcade.draw_text(output, 10, i*20, arcade.color.WHITE, 14)
        for i, coin in enumerate(self.coin_list):
            output = f"Score: {coin.breed_point}"
            arcade.draw_text(output, 1000, i*20, arcade.color.WHITE, 14)
        for i, coin in enumerate(self.coin_list):
            output = f"Score: {coin.hungry_point}"
            arcade.draw_text(output, 1100, i*20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """
        new_gen = arcade.SpriteList()
        for player_sprite in self.player_list:
            # Move the center of the player sprite to match the mouse x, y
            player_sprite.center_x += player_sprite.change_x
            player_sprite.center_y += player_sprite.change_y
            # Check if we need to bounce of right edge
            if player_sprite.center_x > SCREEN_WIDTH:
                player_sprite.change_x *= -1
            # Check if we need to bounce of top edge
            if player_sprite.center_y > SCREEN_HEIGHT:
                player_sprite.change_y *= -1
            # Check if we need to bounce of left edge
            if player_sprite.center_x < 0:
                player_sprite.change_x *= -1
            # Check if we need to bounce of bottom edge
            if player_sprite.center_y < 0:
                player_sprite.change_y *= -1
            if len(self.player_list) < MAX_PLAYER:
                if player_sprite.breed_point >= 600:
                    new_player = arcade.Sprite(
                        ":resources:images/animated_characters/female_person/femalePerson_idle.png",
                        SPRITE_SCALING_PLAYER)
                    new_player.center_x = player_sprite.center_x + random.randrange(-1, 1)
                    new_player.center_y = player_sprite.center_y + random.randrange(-1, 1)
                    new_player.change_x = -player_sprite.change_x
                    new_player.change_y = -player_sprite.change_y
                    new_player.breed_point = 0
                    new_gen.append(new_player)
                    player_sprite.breed_point = 0
                else:
                    player_sprite.breed_point += random.randrange(1, 6)
        for new in new_gen:
            self.player_list.append(new)
        new_coin = arcade.SpriteList()
        for coin in self.coin_list:
            coin.hunger()
            ret = coin.breed()
            if ret != 1:
                new_coin.append(ret)
            coin.follow_sprite(self.player_list)
        for new in new_coin:
            self.coin_list.append(new)
        # Generate a list of all sprites that collided with the player.
        for coin in self.coin_list:
            hit_list = arcade.check_for_collision_with_list(coin, self.player_list)
            if hit_list is not None:

                # Loop through each colliding sprite, remove it, and add to the score.
                for player in hit_list:
                    player.kill()
                coin.hungry_point += 100*len(hit_list)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
