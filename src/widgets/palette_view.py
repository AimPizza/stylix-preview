from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container

from constants import DEFAULT_PALETTE_PATH
from models.base16 import Base16Palette
from models.palette import Palette
from backends.json import JsonBackend
from backends.yaml import YamlBackend
from widgets.color_button import ColorButton
from widgets.palette_grid import PaletteGrid


class PaletteView(Container):
    """Display a grid of a given color palette."""

    palette: Palette | None = None
    file_path = Path(DEFAULT_PALETTE_PATH)

    # Use a class selector so multiple PaletteViews can coexist.
    SELECTOR = ".color-container"

    def __init__(self, palette_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.file_path = palette_path

    def _load_palette(self, path: Path) -> Palette:
        path = path.expanduser()
        ext = path.suffix.lower()
        if ext == ".json":
            return JsonBackend(path, palette_factory=Base16Palette).value
        if ext in {".yml", ".yaml"}:
            return YamlBackend(path, palette_factory=Base16Palette).value
        raise ValueError(f"Unsupported palette file type: {ext} ({path})")

    async def render_content(self) -> None:
        if self.palette is None:
            raise ValueError("Failed to load content. No palette.")

        content = self.query_one(self.SELECTOR, Container)
        content.remove_children()

        grid = PaletteGrid()
        await content.mount(grid)

        buttons = [
            ColorButton(title=title, hex_code=color.value)
            for title, color in self.palette.colors.items()
        ]
        await grid.mount(*buttons)

    async def on_mount(self) -> None:
        try:
            self.palette = self._load_palette(self.file_path)
            await self.render_content()
        except Exception as e:
            self.notify(str(e))
            self.remove()

    def compose(self) -> ComposeResult:
        yield Container(classes=self.SELECTOR.lstrip("."))
