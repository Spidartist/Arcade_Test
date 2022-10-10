
import random
import arcade
import math
import os

# --- Constants ---
SPRITE_SCALING_PREY = 0.9
SPRITE_SCALING_PRED = 0.7
PRED_COUNT = 5
PRED_SPEED = 1.2

PREY_COUNT = 10
MAX_PREY = 30

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Sprite Follow prey Simple Example 2"

PRED_ANGLE_SPEED = 5
SPRITE_SPEED = 0.5
PRED_IMAGE = ":resources:images/topdown_tanks/tank_red.png"
PREY_IMAGE = ":resources:images/topdown_tanks/tank_blue.png"


class Prey(arcade.Sprite):
    """
    This class represents the preds on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """
    def __init__(self, *args):
        super(Prey, self).__init__(*args)
        self.angle = 180
        
    def find_closest(self, pred_list):
        min_dist = 10000
        closest = None
        for pred_sprite in pred_list:
            x_diff = pred_sprite.center_x - self.center_x
            y_diff = pred_sprite.center_y - self.center_y
            distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = pred_sprite
        return closest, min_dist

    def juke_kill(self, pred_list):
        pred_sprite, min_dist = self.find_closest(pred_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        if min_dist <= 200:
            if random.randrange(100) == 0:
                start_x = self.center_x
                start_y = self.center_y

                # Get the destination location for the bullet
                dest_x = pred_sprite.center_x
                dest_y = pred_sprite.center_y

                # Do math to calculate how to get the bullet to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the bullet will travel.
                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)
                self.angle = math.degrees(angle)
                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                self.change_x = math.cos(angle) * SPRITE_SPEED * 4
                self.change_y = -math.sin(angle) * SPRITE_SPEED * 4


class Pred(arcade.Sprite):
    """
    This class represents the preds on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """
    def __init__(self, *args):
        super(Pred, self).__init__(*args)
        self.breed_point = 0
        self.hungry_point = 500
        self.angle = 0

    def hunger(self):
        if self.hungry_point <= 0:
            self.kill()
        else:
            self.hungry_point -= 1

    def breed(self):
        if self.breed_point >= 600:
            new_pred = Pred(PRED_IMAGE, SPRITE_SCALING_PRED)
            new_pred.center_x = self.center_x + random.randrange(-2, 2)
            new_pred.center_y = self.center_y + random.randrange(-2, 2)
            new_pred.change_x = random.randrange(-1, 1, 2) * self.change_x
            new_pred.change_y = random.randrange(-1, 1, 2) * self.change_y
            new_pred.angle = self.angle + 180
            self.breed_point = 0
            return new_pred
        else:
            self.breed_point += 1
        return 1

    def find_closest(self, prey_list):
        min_dist = 10000
        closest = None
        for prey_sprite in prey_list:
            x_diff = prey_sprite.center_x - self.center_x
            y_diff = prey_sprite.center_y - self.center_y
            distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = prey_sprite
        return closest, min_dist

    def follow_prey(self, prey_list):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """
        prey_sprite, min_dist = self.find_closest(prey_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the prey
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = prey_sprite.center_x
            dest_y = prey_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            self.angle = math.degrees(angle) + 90
            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * PRED_SPEED * 1.3 * (SCREEN_WIDTH / (min_dist * 5))
            self.change_y = math.sin(angle) * PRED_SPEED * 1.3 * (SCREEN_HEIGHT / (min_dist * 5))


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
        self.prey_list = None
        self.pred_list = None
        self.winner = None
        # Set up the prey info

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.prey_list = arcade.SpriteList()
        self.pred_list = arcade.SpriteList()

        # Character image from kenney.nl
        for i in range(PREY_COUNT):
            prey_sprite = Prey(PREY_IMAGE, SPRITE_SCALING_PREY)
            prey_sprite.center_x = random.randrange(SCREEN_WIDTH)
            prey_sprite.center_y = random.randrange(SCREEN_HEIGHT)
            prey_sprite.change_x = 0.6
            prey_sprite.change_y = 0.4
            prey_sprite.breed_point = 0
            self.prey_list.append(prey_sprite)

        # Create the preds
        for i in range(PRED_COUNT):
            # Create the pred instance
            # pred image from kenney.nl
            pred = Pred(PRED_IMAGE, SPRITE_SCALING_PRED)

            # Position the pred
            pred.center_x = random.randrange(SCREEN_WIDTH)
            pred.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the pred to the lists
            self.pred_list.append(pred)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.pred_list.draw()
        self.prey_list.draw()
        for i, prey in enumerate(self.prey_list):
            angle_rad = math.radians(prey.angle)
            arcade.draw_line(prey.center_x, prey.center_y, prey.center_x + 20 * math.sin(angle_rad), prey.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Prey Breed: {prey.breed_point}"
            arcade.draw_text(output, 10, i*20, arcade.color.WHITE, 14)
        for i, pred in enumerate(self.pred_list):
            angle_rad = math.radians(pred.angle)
            arcade.draw_line(pred.center_x, pred.center_y, pred.center_x + 20 * math.sin(angle_rad), pred.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Breed: {pred.breed_point}"
            arcade.draw_text(output, 900, i*20, arcade.color.WHITE, 14)
            output = f"Hungry: {pred.hungry_point}"
            arcade.draw_text(output, 1050, i * 20, arcade.color.WHITE, 14)

        if self.winner is not None:
            output = self.winner + " win!"
            arcade.draw_text(output, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, 14)
            arcade.pause(1)

    def on_update(self, delta_time):
        """ Movement and game logic """

        if len(self.pred_list) == 0:
            self.winner = "Prey"
        if len(self.prey_list) == 0:
            self.winner = "Predator"

        new_gen = arcade.SpriteList()

        for prey_sprite in self.prey_list:
            # Move the center of the prey sprite to match the mouse x, y
            prey_sprite.juke_kill(self.pred_list)
            # Check if we need to bounce of right edge
            if prey_sprite.center_x > SCREEN_WIDTH:
                prey_sprite.change_x *= -1
            # Check if we need to bounce of top edge
            if prey_sprite.center_y > SCREEN_HEIGHT:
                prey_sprite.change_y *= -1
            # Check if we need to bounce of left edge
            if prey_sprite.center_x < 0:
                prey_sprite.change_x *= -1
            # Check if we need to bounce of bottom edge
            if prey_sprite.center_y < 0:
                prey_sprite.change_y *= -1
            if len(self.prey_list) < MAX_PREY:
                if prey_sprite.breed_point >= 600:
                    new_prey = Prey(PREY_IMAGE, SPRITE_SCALING_PREY)
                    new_prey.center_x = prey_sprite.center_x + random.randrange(-1, 1)
                    new_prey.center_y = prey_sprite.center_y + random.randrange(-1, 1)
                    new_prey.change_x = random.randrange(-1, 1, 2) * prey_sprite.change_x
                    new_prey.change_y = random.randrange(-1, 1, 2) * prey_sprite.change_y
                    new_prey.angle = prey_sprite.angle + 180
                    new_prey.breed_point = 0
                    new_gen.append(new_prey)
                    prey_sprite.breed_point = 0
                else:
                    prey_sprite.breed_point += random.randrange(1, 6)
        for new in new_gen:
            self.prey_list.append(new)
        new_pred = arcade.SpriteList()
        for pred in self.pred_list:
            pred.hunger()
            ret = pred.breed()
            if ret != 1:
                new_pred.append(ret)
            if len(self.prey_list) > 0:
                pred.follow_prey(self.prey_list)
            if pred.center_x > SCREEN_WIDTH:
                pred.center_x = SCREEN_WIDTH

            # Check if we need to bounce of top edge
            if pred.center_y > SCREEN_HEIGHT:
                pred.center_y = SCREEN_HEIGHT
            # Check if we need to bounce of left edge
            if pred.center_x < 0:
                pred.center_x = 0
            # Check if we need to bounce of bottom edge
            if pred.center_y < 0:
                pred.center_y = 0
        for new in new_pred:
            self.pred_list.append(new)
        # Generate a list of all sprites that collided with the prey.
        for pred in self.pred_list:
            hit_list = arcade.check_for_collision_with_list(pred, self.prey_list)
            if hit_list is not None:

                # Loop through each colliding sprite, remove it, and add to the score.
                for prey in hit_list:
                    prey.kill()
                pred.hungry_point += 100*len(hit_list)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
