import arcade
import math
import os
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Test angle"

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.agent = None
        # Set up the prey info

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.agent = arcade.Sprite(":resources:images/topdown_tanks/tank_blue.png", 0.8)
        self.agent.change_x = 2
        self.agent.change_y = 2
        angle = math.atan2(self.agent.change_x, self.agent.change_y)
        self.agent.angle = math.degrees(angle) + 90

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.agent.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.agent.center_x += self.agent.change_x
        self.agent.center_y += self.agent.change_y



def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()