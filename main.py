from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (
  NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.core.window import Window
from collections import deque
from random import randint

BOARD_SIZE = 60
VLEFT = -1, 0
VUP = 0, 1
VRIGHT = 1, 0
VDOWN = 0, -1

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self._v = VLEFT
        elif keycode[1] == 'up':
            self._v = VUP
        elif keycode[1] == 'right':
            self._v = VRIGHT
        elif keycode[1] == 'down':
            self._v = VDOWN
        else:
          return False

        return True

    _square_size = 25, 25
    _min_snake_len = 20
    _v = VRIGHT
    _offsets = deque()
    _apple_offset = None

    def _current_pos(self):
        if (len(self._offsets) < 1):
            return BOARD_SIZE / 2, BOARD_SIZE / 2

        return self._offsets[-1]

    def _random_offset(self):
        return randint(1, BOARD_SIZE) - 1, randint(1, BOARD_SIZE) - 1

    def _is_valid(self, offset):
        if offset is None:
            return False
        if offset[0] < 0 or offset[0] >= BOARD_SIZE:
            return False
        if offset[1] < 0 or offset[1] >= BOARD_SIZE:
            return False
        return self._offsets.count(offset) == 0

    def _move_apple(self, offset):
        self._apple_offset = offset

    def start(self):
        Window.size = (BOARD_SIZE * self._square_size[0] / 2, BOARD_SIZE * self._square_size[1] / 2)
        offset = self._random_offset()
        self._move_apple(offset)
        Clock.schedule_interval(self._update, 0.1)

    def _game_over(self):
      Clock.unschedule(self._update)
      with self.canvas:
          Label(
            text='Game Over!',
            pos=(BOARD_SIZE * self._square_size[0] / 2, BOARD_SIZE * self._square_size[1] / 2)
          )

    def _next(self):
        current_pos = self._current_pos()
        next_pos = current_pos[0] + self._v[0], current_pos[1] + self._v[1]
        if not self._is_valid(next_pos):
            self._game_over()
            return

        if next_pos == self._apple_offset:
            apple_offset = None
            while 1 == 1:
                apple_offset = self._random_offset()
                if self._is_valid(apple_offset):
                    break
            self._move_apple(apple_offset)
            self._offsets.append(next_pos)
            self._min_snake_len += 20
        else:
            if len(self._offsets) > self._min_snake_len:
                tail = self._offsets.popleft()
                with self.canvas:
                    Color(0.1, 0.1, 0.1, 1.0, mode='rgba')
                    self._fill_square(tail)
            self._offsets.append(next_pos)

    def _fill_square(self, offset):
        Rectangle(pos=(offset[0] * self._square_size[0], offset[1] * self._square_size[1]), size=(self._square_size[0], self._square_size[1]))

    def _draw_snake(self):
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1.0, mode='rgba')
            self._fill_square(self._offsets[-1])

    def _draw_apple(self):
        with self.canvas:
            Color(1.0, 0.0, 0.0, 1.0, mode='rgba')
            self._fill_square(self._apple_offset)

    def _calculate_square_size(self):
        x = self.size[0]
        y = self.size[1]
        return x / BOARD_SIZE, y / BOARD_SIZE

    def _rerender(self):
        with self.canvas:
            Color(0.1, 0.1, 0.1, 1.0, mode='rgba')
            Rectangle(pos=self.pos, size=self.size)
            Color(0.9, 0.9, 0.9, 1.0, mode='rgba')
            for offset in self._offsets:
                self._fill_square(offset)
            self._draw_apple()

    def _update(self, dt):
        square_size = self._calculate_square_size()
        if square_size != self._square_size:
            self._square_size = square_size
            self._rerender()
        self._next()
        self._draw_snake()
        self._draw_apple()
        
class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        game.start()
        return game

if __name__ == '__main__':
    SnakeApp().run()
