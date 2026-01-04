from collections.abc import Callable
from typing import Generic, TypeVar, override

from models.color import Color
from models.palette import Palette

from .palette_backend import PaletteBackend
from pathlib import Path
import json


P = TypeVar("P", bound=Palette)


class JsonBackend(PaletteBackend, Generic[P]):
    """Loads a palette from a JSON file with keys like 'base00'..'base0F'."""

    path: Path
    value: P

    @override
    def __init__(self, path: Path, palette_factory: Callable[[], P]) -> None:
        self.path = path
        self.value = palette_factory()
        self._load()

    @override
    def _load(self) -> None:
        if not self.path:
            raise ValueError("path not set")

        try:
            with open(self.path, "r") as file:
                palette_raw: dict[str, str] = json.load(file)
        except Exception as e:
            raise IOError("Failed to read json palette") from e

        for key, val in palette_raw.items():
            if key.startswith("base"):
                self.value.set_base_n_color(int(key[-2:], 16), color=Color(hex_val=val))
