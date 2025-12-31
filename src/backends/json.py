from typing import overload, override

from models.color import Color

from .palette_backend import PaletteBackend
from pathlib import Path
import json


class JsonBackend(PaletteBackend):
    """Make sure to set path variable when initializing the object."""

    path: Path
    """OS Path to json file"""

    @override
    def load(self) -> None:
        if not self.path:
            raise ValueError("path not set")

        try:
            with open(self.path, "r") as file:
                palette_raw: dict[str, str] = json.load(file)
        except Exception:
            raise IOError("Failed to read json palette")

        for key, val in palette_raw.items():
            if key.startswith("base"):
                self.value.set_base_n_color(int(key[-2:], 16), color=Color(value=val))
