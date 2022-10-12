import arcade
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Test Hitbox"


def collision_checking_list():
    pass


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player = None
        self.player_2 = None
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player = arcade.Sprite(":resources:images/topdown_tanks/tank_red.png", 1)
        self.player.center_x = 500
        self.player.center_y = 600
        self.player.angle = 90

        self.player_2 = arcade.Sprite(":resources:images/topdown_tanks/tank_blue.png", 1)
        self.player_2.center_x = 600
        self.player_2.center_y = 600
        self.player_2.angle = 90

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.player.draw()
        self.player_2.draw()
        self.player.draw_hit_box()
        print(self.player.collision_radius)
        self.player_2.draw_hit_box()
        print(self.player.hit_box)
        for phi in range(-30, 40, 10):
            angle_rad = math.radians(self.player.angle + phi)
            arcade.draw_line(self.player.center_x, self.player.center_y,
                             self.player.center_x + 150 * math.sin(angle_rad),
                             self.player.center_y - 150 * math.cos(angle_rad), arcade.color.BLUE, 1)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
