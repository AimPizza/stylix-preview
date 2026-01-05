from abc import ABC, abstractmethod

from models.palette import Palette

from typing import Mapping, TypedDict


class FlatTheme(TypedDict, total=False):
    """Legacy theme format. Colors are placed as str,str bindings into root."""

    system: str | None
    name: str | None
    author: str | None
    variant: str | None
    scheme: str | None
    slug: str | None


class PaletteTheme(FlatTheme):
    """Modern theme format. Colors are in self.palette."""

    palette: Mapping[str, str]


ThemeDict = FlatTheme | PaletteTheme
"""Provide fields a scheme can have.

Additionally, there are str, str bindings for the color values."""


class PaletteBackend(ABC):
    value: Palette

    @abstractmethod
    def _load(self) -> None:
        """Populate own value.

        Raises ValueError if nessecary fields are not set.
        """
        raise NotImplementedError

    def load_title(
        self,
    ) -> None:
        """Generate a palette title.

        Title can come from:
        - palette
        - filename"""
        raise NotImplementedError

    def __init__(self) -> None:
        self._load()
