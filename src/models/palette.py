from abc import ABC, abstractmethod
from typing import Optional

from .color import Color


class Palette(ABC):
    """Unspecified n base palette."""

    base: int
    name: Optional[str]
    colors: dict[str, Color]

    @abstractmethod
    def get_base_n_color(self, n: int) -> Color:
        """0-based color index.

        Asserts the correct base.

        :param int n: base index
        """
        raise NotImplemented

    @abstractmethod
    def set_base_n_color(self, n: int, color: Color) -> None:
        """Set color at 0-based index.

        Asserts the correct base.

        :param int n: base index
        :param Color color: color to set
        """
        raise NotImplemented
