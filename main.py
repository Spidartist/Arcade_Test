import random
import arcade
import math

# --- Constants ---
SPRITE_SCALING_PREY = 0.9
SPRITE_SCALING_PRED = 0.7

PRED_COUNT = 5
PREY_COUNT = 10

PRED_SPEED = 1.2
PREY_SPEED = 0.5

CURRENT_PREY = 0
CURRENT_PRED = 0

MAX_PREY = 15

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MAX_DISTANCE = math.sqrt(SCREEN_HEIGHT ** 2 + SCREEN_WIDTH ** 2)

SCREEN_TITLE = "Sprite Follow prey Simple Example 2"

PRED_IMAGE = ":resources:images/topdown_tanks/tank_red.png"
PREY_IMAGE = ":resources:images/topdown_tanks/tank_blue.png"


class Animal(arcade.Sprite):
    def __init__(self, *args):
        super(Animal, self).__init__(*args)
        self.hunger_point = 0
        self.breed_point = 0
        self.max_breed = 0
        self.angle = 0
        self.image = None
        self.scale = 0

    def find_closest(self, diff_list):
        min_dist = 10000
        closest = None
        for diff_sprite in diff_list:
            x_diff = diff_sprite.center_x - self.center_x
            y_diff = diff_sprite.center_y - self.center_y
            distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = diff_sprite
        return closest, min_dist

    def new_animal(self, image, scale):
        return Animal(image, scale)

    def breed(self):
        if self.breed_point >= self.max_breed:
            new_pred = self.new_animal(self.image, self.scale)
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

    def change_angle_func(self):
        return math.degrees(math.atan2(self.change_y, self.change_x)) + 90


class Pred(Animal):
    def __init__(self, *args):
        super(Pred, self).__init__(*args)
        self.hunger_point = 400
        self.max_breed = 600
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.change_x = random.randrange(8, 14, 2) / 10 * PRED_SPEED
        self.change_y = random.randrange(8, 14, 2) / 10 * PRED_SPEED
        self.angle = self.change_angle_func()
        self.image = PRED_IMAGE
        self.scale = SPRITE_SCALING_PRED

    def hunger(self):
        global CURRENT_PRED
        if self.hunger_point <= 0:
            self.kill()
            CURRENT_PRED -= 1
        else:
            self.hunger_point -= 1

    def follow_prey(self, prey_list):
        prey_sprite, min_dist = self.find_closest(prey_list)
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = prey_sprite.center_x
            dest_y = prey_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            dist_diff = math.sqrt(x_diff ** 2 + y_diff ** 2)
            scale_speed = MAX_DISTANCE / dist_diff / 2
            angle = math.atan2(y_diff, x_diff)
            self.angle = math.degrees(angle) + 90

            self.change_x = math.cos(angle) * PRED_SPEED * scale_speed
            self.change_y = math.sin(angle) * PRED_SPEED * scale_speed

    def new_animal(self, image, scale):
        return Pred(image, scale)


class Prey(Animal):
    def __init__(self, *args):
        super(Prey, self).__init__(*args)
        self.hunger_point = 800
        self.max_hunger = 800
        self.max_breed = 500
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.change_x = random.randrange(6, 14, 2) / 10 * PREY_SPEED
        self.change_y = random.randrange(6, 14, 2) / 10 * PREY_SPEED
        self.angle = self.change_angle_func()
        self.dst_away = 500
        self.dst_juke = 200
        self.need_heal = False
        self.image = PREY_IMAGE
        self.scale = SPRITE_SCALING_PREY

    def hunger(self):
        if not self.need_heal:
            if self.hunger_point <= 0:
                self.change_x = 0
                self.change_y = 0
                self.hunger_point = 0
                self.need_heal = True
            else:
                self.hunger_point -= 1

    def heal(self):
        if self.need_heal:
            self.hunger_point += 2
        if self.hunger_point >= self.max_hunger:
            self.need_heal = False

    def juke_kill(self, pred_list):
        pred_sprite, min_dist = self.find_closest(pred_list)

        if min_dist <= self.dst_away:
            if random.randrange(100) == 0:
                start_x = self.center_x
                start_y = self.center_y

                dest_x = pred_sprite.center_x
                dest_y = pred_sprite.center_y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y

                angle = math.atan2(y_diff, x_diff)

                self.change_x = -math.cos(angle) * PREY_SPEED * 4
                self.change_y = -math.sin(angle) * PREY_SPEED * 4

                self.angle = self.change_angle_func()

        if min_dist <= self.dst_juke:
            if random.randrange(100) == 0:
                start_x = self.center_x
                start_y = self.center_y

                dest_x = pred_sprite.center_x
                dest_y = pred_sprite.center_y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y

                angle = math.atan2(y_diff, x_diff)
                direction = random.randrange(-1, 1, 2)

                self.change_x = direction * math.sin(angle) * PREY_SPEED * 12
                self.change_y = direction * math.cos(angle) * PREY_SPEED * 12

                self.angle = self.change_angle_func()
        self.center_x += self.change_x
        self.center_y += self.change_y

    def new_animal(self, image, scale):
        return Prey(image, scale)


class MyGame(arcade.Window):

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.prey_list = None
        self.pred_list = None
        self.winner = None

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        global CURRENT_PRED
        global CURRENT_PREY
        """ Set up the game and initialize the variables. """

        self.prey_list = arcade.SpriteList()
        self.pred_list = arcade.SpriteList()

        for i in range(PREY_COUNT):
            prey = Prey(PREY_IMAGE, SPRITE_SCALING_PREY)
            self.prey_list.append(prey)
            CURRENT_PREY += 1

        # Create the preds
        for i in range(PRED_COUNT):
            pred = Pred(PRED_IMAGE, SPRITE_SCALING_PRED)
            self.pred_list.append(pred)
            CURRENT_PRED += 1

    def on_draw(self):
        """ Draw everything """
        global CURRENT_PRED
        global CURRENT_PREY
        self.clear()
        self.pred_list.draw()
        self.prey_list.draw()
        num_pred = f"Num Pred: {CURRENT_PRED}"
        arcade.draw_text(num_pred, 1050, 750, arcade.color.WHITE, 14)
        num_prey = f"Num Prey: {CURRENT_PREY}"
        arcade.draw_text(num_prey, 10, 750, arcade.color.WHITE, 14)
        for i, prey in enumerate(self.prey_list):
            angle_rad = math.radians(prey.angle)
            arcade.draw_line(prey.center_x, prey.center_y, prey.center_x + 20 * math.sin(angle_rad),
                             prey.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Breed: {prey.breed_point}"
            arcade.draw_text(output, 10, i * 20, arcade.color.WHITE, 14)
            output = f"Hungry: {prey.hunger_point}"
            arcade.draw_text(output, 160, i * 20, arcade.color.WHITE, 14)
        for i, pred in enumerate(self.pred_list):
            angle_rad = math.radians(pred.angle)
            arcade.draw_line(pred.center_x, pred.center_y, pred.center_x + 20 * math.sin(angle_rad),
                             pred.center_y - 20 * math.cos(angle_rad), arcade.color.BLUE, 1)
            output = f"Breed: {pred.breed_point}"
            arcade.draw_text(output, 900, i * 20, arcade.color.WHITE, 14)
            output = f"Hungry: {pred.hunger_point}"
            arcade.draw_text(output, 1050, i * 20, arcade.color.WHITE, 14)

        if self.winner is not None:
            output = self.winner + " win!"
            arcade.draw_text(output, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, 14)
            arcade.pause(0.5)

    def on_update(self, delta_time):
        """ Movement and game logic """
        global CURRENT_PRED
        global CURRENT_PREY
        if len(self.pred_list) == 0:
            self.winner = "Prey"
        if len(self.prey_list) == 0:
            self.winner = "Predator"

        new_prey = arcade.SpriteList()
        for prey_sprite in self.prey_list:
            if prey_sprite.center_x > SCREEN_WIDTH:
                prey_sprite.change_x *= -1

            if prey_sprite.center_y > SCREEN_HEIGHT:
                prey_sprite.change_y *= -1

            if prey_sprite.center_x < 0:
                prey_sprite.change_x *= -1

            if prey_sprite.center_y < 0:
                prey_sprite.change_y *= -1
            prey_sprite.angle = prey_sprite.change_angle_func()

            if CURRENT_PRED > 0:
                prey_sprite.hunger()
                prey_sprite.heal()
                prey_sprite.juke_kill(self.pred_list)

                if CURRENT_PREY < MAX_PREY:
                    ret = prey_sprite.breed()
                    if ret != 1:
                        new_prey.append(ret)
                        CURRENT_PREY += 1
        for new in new_prey:
            self.prey_list.append(new)

        new_pred = arcade.SpriteList()
        for pred in self.pred_list:
            if pred.center_x > SCREEN_WIDTH:
                pred.change_x *= -1

            if pred.center_y > SCREEN_HEIGHT:
                pred.change_y *= -1

            if pred.center_x < 0:
                pred.change_x *= -1

            if pred.center_y < 0:
                pred.change_y *= -1
            pred.angle = pred.change_angle_func()

            if CURRENT_PRED > 0 and CURRENT_PREY > 0:
                pred.follow_prey(self.prey_list)
                pred.hunger()
                ret = pred.breed()
                if ret != 1:
                    new_pred.append(ret)
                    CURRENT_PRED += 1
        for new in new_pred:
            self.pred_list.append(new)

        for pred in self.pred_list:
            hit_list = arcade.check_for_collision_with_list(pred, self.prey_list)
            if hit_list is not None:
                for prey in hit_list:
                    prey.kill()
                    CURRENT_PREY -= 1
                pred.hunger_point += 100 * len(hit_list)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
