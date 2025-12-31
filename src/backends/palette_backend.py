from abc import ABC, abstractmethod

from models.palette import Palette


class PaletteBackend(ABC):
    value: Palette

    @abstractmethod
    def load(self) -> None:
        """Populate own value.

        Raises ValueError if nessecary fields are not set.
        """
        raise NotImplemented
