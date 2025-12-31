from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from backends.json import JsonBackend
from models.base16 import Base16Palette
from models.palette import Palette
from widgets.color_button import ColorButton
from widgets.home_grid import HomeGrid


class StylixViewer(App):
    """A Textual app to inspect Stylix palettes."""

    palette: Palette

    CSS_PATH = "widgets/style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, palette_path: str, **kwargs):
        super().__init__(**kwargs)
        json_backend = JsonBackend(palette_path, palette_factory=Base16Palette)
        self.palette = json_backend.value

        self.title = f"{self.title} - {json_backend.path.as_posix()}"

    def compose(self) -> ComposeResult:
        yield Header()
        with HomeGrid():
            for title, color in self.palette.colors.items():
                yield ColorButton(title=title, hex_code=color.value)
        yield Footer(show_command_palette=False)


if __name__ == "__main__":
    app = StylixViewer(palette_path="/etc/stylix/palette.json")
    app.run()
