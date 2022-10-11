import random
import arcade
import math
import os

# --- Constants ---
SPRITE_SCALING_PREY = 0.9
SPRITE_SCALING_PRED = 0.7

PREY_COUNT = 10
PRED_COUNT = 5

PRED_SPEED = 1.2

MAX_PREY = 30

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Pred VS Prey"

PRED_ANGLE_SPEED = 5
SPRITE_SPEED = 0.5
PRED_IMAGE = ":resources:images/topdown_tanks/tank_red.png"
PREY_IMAGE = ":resources:images/topdown_tanks/tank_blue.png"


class Animal(arcade.Sprite):

    def __init__(self, *args):
        super(Animal, self).__init__(*args)
        self.breed_point = 0
        self.angle = 0
        self.max_breed = 0
        self.image = None
        self.scale_size = 0
        self.max_count = 0
        self.init_count = 0

    def make_animal(self, image, scale_size):
        return Animal(image, scale_size)

    def breed(self):
        if self.breed_point >= self.max_breed:
            new_animal = self.make_animal(self.image, self.scale_size)
            new_animal.center_x = self.center_x + random.randrange(-2, 2)
            new_animal.center_y = self.center_y + random.randrange(-2, 2)
            new_animal.change_x = random.randrange(-1, 1, 2) * self.change_x
            new_animal.change_y = random.randrange(-1, 1, 2) * self.change_y
            new_animal.angle = math.degrees(math.atan2(new_animal.change_y, new_animal.change_x)) + 90
            self.breed_point = 0
            return new_animal
        else:
            self.breed_point += random.randrange(1, 2)
        return 1

    def find_closest(self, diff_list):
        min_dist = 10000
        closest = None
        for pred_sprite in diff_list:
            x_diff = pred_sprite.center_x - self.center_x
            y_diff = pred_sprite.center_y - self.center_y
            distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = pred_sprite
        return closest, min_dist


class Prey(Animal):
    def __init__(self, *args):
        super(Prey, self).__init__(*args)
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) + 90
        self.scale_size = SPRITE_SCALING_PREY
        self.max_breed = 700
        self.image = PREY_IMAGE
        self.dist_juke = 200
        self.dist_go_away = 500
        self.change_x = 0.6
        self.change_y = 0.4
        self.breed_point = 0
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)

    def make_animal(self, image, scale_size):
        return Prey(image, scale_size)

    def juke_kill(self, pred_list):
        pred_sprite, min_dist = self.find_closest(pred_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        if min_dist <= self.dist_go_away:
            if random.randrange(100) == 0:
                start_x = self.center_x
                start_y = self.center_y

                # Get the destination location for the bullet
                dest_x = pred_sprite.center_x
                dest_y = pred_sprite.center_y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                self.change_x = -math.cos(angle) * SPRITE_SPEED * 4
                self.change_y = -math.sin(angle) * SPRITE_SPEED * 4
                changed_angle = math.degrees(math.atan2(self.change_y, self.change_x))
                self.angle = changed_angle + 90

        if min_dist <= self.dist_juke:
            if random.randrange(100) == 0:
                start_x = self.center_x
                start_y = self.center_y

                # Get the destination location for the bullet
                dest_x = pred_sprite.center_x
                dest_y = pred_sprite.center_y

                # Do math to calculate how to get the bullet to the destination.

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                self.change_x = math.sin(angle) * SPRITE_SPEED * 8
                self.change_y = math.cos(angle) * SPRITE_SPEED * 8
                changed_angle = math.degrees(math.atan2(self.change_y, self.change_x))
                self.angle = changed_angle + 90


class Pred(Animal):

    def __init__(self, *args):
        super(Pred, self).__init__(*args)
        self.breed_point = 0
        self.max_breed = 900
        self.hungry_point = 500
        self.angle = 0
        self.image = PRED_IMAGE
        self.scale_size = SPRITE_SCALING_PRED
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)

    def make_animal(self, image, scale_size):
        return Pred(image, scale_size)

    def hunger(self):
        if self.hungry_point <= 0:
            self.kill()
        else:
            self.hungry_point -= 1

    def follow_prey(self, prey_list):
        prey_sprite, min_dist = self.find_closest(prey_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the prey
        if random.randrange(50) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = prey_sprite.center_x
            dest_y = prey_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            self.angle = math.degrees(angle) + 90

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * PRED_SPEED * 1.3 * (SCREEN_WIDTH / (min_dist * 4))
            self.change_y = math.sin(angle) * PRED_SPEED * 1.3 * (SCREEN_HEIGHT / (min_dist * 4))


class MyGame(arcade.Window):

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.prey_list = None
        self.pred_list = None
        self.winner = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.prey_list = arcade.SpriteList()
        self.pred_list = arcade.SpriteList()

        for i in range(PREY_COUNT):
            prey_sprite = Prey(PREY_IMAGE, SPRITE_SCALING_PREY)
            self.prey_list.append(prey_sprite)

        for i in range(PRED_COUNT):
            pred = Pred(PRED_IMAGE, SPRITE_SCALING_PRED)
            self.pred_list.append(pred)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.pred_list.draw()
        self.prey_list.draw()

        for i, prey in enumerate(self.prey_list):
            angle_rad = math.radians(prey.angle)
            arcade.draw_line(prey.center_x, prey.center_y, prey.center_x + 20 * math.sin(angle_rad),
                             prey.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Prey Breed: {prey.breed_point}"
            arcade.draw_text(output, 10, i * 20, arcade.color.WHITE, 14)

        for i, pred in enumerate(self.pred_list):
            angle_rad = math.radians(pred.angle)
            arcade.draw_line(pred.center_x, pred.center_y, pred.center_x + 20 * math.sin(angle_rad),
                             pred.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Breed: {pred.breed_point}"
            arcade.draw_text(output, 900, i * 20, arcade.color.WHITE, 14)
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

        # new_prey = arcade.SpriteList()
        for prey_sprite in self.prey_list:
            if len(self.prey_list) < MAX_PREY:
                ret = prey_sprite.breed()
                if ret != 1:
                    self.prey_list.append(ret)

            prey_sprite.juke_kill(self.pred_list)

            if prey_sprite.center_x > SCREEN_WIDTH:
                prey_sprite.change_x = -prey_sprite.change_x

            if prey_sprite.center_y > SCREEN_HEIGHT:
                prey_sprite.change_y = -prey_sprite.change_y

            if prey_sprite.center_x < 0:
                prey_sprite.change_x = -prey_sprite.change_x

            if prey_sprite.center_y < 0:
                prey_sprite.change_y = -prey_sprite.change_y

        for pred in self.pred_list:
            pred.hunger()
            ret = pred.breed()
            if ret != 1:
                self.prey_list.append(ret)
            if len(self.prey_list) > 0:
                pred.follow_prey(self.prey_list)
            if pred.center_x > SCREEN_WIDTH:
                pred.center_x = SCREEN_WIDTH

            if pred.center_y > SCREEN_HEIGHT:
                pred.center_y = SCREEN_HEIGHT

            if pred.center_x < 0:
                pred.center_x = 0

            if pred.center_y < 0:
                pred.center_y = 0
        # Generate a list of all sprites that collided with the prey.
        for pred in self.pred_list:
            hit_list = arcade.check_for_collision_with_list(pred, self.prey_list)
            if hit_list is not None:
                for prey in hit_list:
                    prey.kill()
                pred.hungry_point += 100 * len(hit_list)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
