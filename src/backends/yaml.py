from collections.abc import Callable
from typing import Generic, TypeVar, override

from models.color import Color
from models.palette import Palette

from .palette_backend import PaletteBackend, ThemeSchema
from pathlib import Path
import yaml


P = TypeVar("P", bound=Palette)


class YamlBackend(PaletteBackend, Generic[P]):
    """Loads a palette from a Yaml file."""

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
                palette_raw: ThemeSchema = yaml.safe_load(file)
                print(palette_raw)

            if not isinstance(palette_raw, dict):
                raise IOError("Invalid yaml palette: expected a mapping at the root")

            palette = palette_raw.get("palette", {})
            if not isinstance(palette, dict):
                raise IOError("Invalid yaml palette: 'palette' must be a mapping")

            for key, val in palette.items():
                if key.startswith("base"):
                    self.value.set_base_n_color(
                        int(key[-2:], 16), color=Color(hex_val=val)
                    )
            self.load_title(palette_raw)

        except Exception as e:
            raise IOError("Failed to read yaml palette") from e
