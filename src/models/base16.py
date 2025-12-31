from typing import override
from color import Color
from .palette import Palette


class Base16Palette(Palette):

    @override
    def get_base_n_color(self, n: int) -> Color:
        if n > 15 or n < 0:
            raise ValueError("Invalid base16 index")
        return self.colors["base{:02X}".format(n)]

    @override
    def set_base_n_color(self, n: int, color: Color) -> None:
        if n > 15 or n < 0:
            raise ValueError("Invalid base16 index")
        self.colors["base{:02X}".format(n)] = color
