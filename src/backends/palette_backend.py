from abc import ABC, abstractmethod

from models.palette import Palette


class PaletteBackend(ABC):
    value: Palette

    def _load(self) -> None:
        """Populate own value.

        Raises ValueError if nessecary fields are not set.
        """
        raise NotImplemented

    def __init__(self) -> None:
        self._load()
