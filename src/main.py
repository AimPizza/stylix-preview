from pathlib import Path
from typing import Optional
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from backends.json import JsonBackend
from models.base16 import Base16Palette
from models.palette import Palette
from widgets.color_button import ColorButton
from widgets.home_grid import HomeGrid
from widgets.input_screen import InputScreen


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

    def _on_palette_path_chosen(self, result: Optional[Path]) -> None:
        if result is not None:
            self.notify(result.as_posix())

    async def on_key(self, event: events.Key) -> None:
        match event.key:
            # other navigation
            case "f":
                self.push_screen(InputScreen(), callback=self._on_palette_path_chosen)
            # VIM keys
            case "l":
                self.screen.focus_next(ColorButton)
            case "h":
                self.screen.focus_previous(ColorButton)
            case "j":
                _ = [
                    self.screen.focus_next(ColorButton)
                    for _ in range(HomeGrid.COL_COUNT)
                ]
            case "k":
                _ = [
                    self.screen.focus_previous(ColorButton)
                    for _ in range(HomeGrid.COL_COUNT)
                ]


if __name__ == "__main__":
    app = StylixViewer(palette_path="/etc/stylix/palette.json")
    app.run()
