import sys
from pathlib import Path
from typing import Optional

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

from backends.json import JsonBackend
from backends.yaml import YamlBackend
from constants import DEFAULT_PALETTE_PATH
from models.base16 import Base16Palette
from models.palette import Palette
from widgets.color_button import ColorButton
from widgets.home_grid import HomeGrid
from widgets.input_screen import InputScreen


class StylixViewer(App):
    """A Textual app to inspect Stylix palettes."""

    palette: Optional[Palette] = None
    palette_file_path = reactive(Path(DEFAULT_PALETTE_PATH))

    CSS_PATH = "widgets/style.tcss"

    BINDINGS = [("q", "quit", "Quit"), ("f", "open_input", "Pick palette path")]

    def __init__(self, palette_path: str, **kwargs):
        super().__init__(**kwargs)
        self._suppress_palette_watch = False

        self._last_palette_error: Optional[str] = None
        self._last_failed_palette_path: Optional[Path] = None

        self.palette_file_path = Path(palette_path)

    def _load_palette(self, path: Path) -> Palette:
        """Load a palette from `path` using the correct backend based on extension."""
        path = path.expanduser()

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Palette file not found: {path.as_posix()}")

        ext = path.suffix.lower()
        if ext == ".json":
            backend = JsonBackend(path.as_posix(), palette_factory=Base16Palette)
            return backend.value

        if ext in {".yml", ".yaml"}:
            backend = YamlBackend(path.as_posix(), palette_factory=Base16Palette)
            return backend.value

        raise ValueError(f"Unsupported palette file type: {ext} ({path.as_posix()})")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="content")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self._render_content()

    def update_title(self) -> None:
        self.title = f"{self.__class__.__name__} - {self.palette_file_path.as_posix()}"

    def _clear_content(self) -> None:
        content = self.query_one("#content", Container)
        for child in list(content.children):
            child.remove()

    def _render_content(self) -> None:
        """Mount either the error label or a fresh HomeGrid based on current palette."""
        self.update_title()
        self._clear_content()

        content = self.query_one("#content", Container)

        if self.palette is None:
            failed_path = self._last_failed_palette_path or self.palette_file_path
            details = self._last_palette_error or "Unknown error"
            content.mount(
                Label(
                    "Couldn't load palette from: "
                    f"{failed_path.as_posix()}\n\n{details}"
                )
            )
            return

        grid = HomeGrid()
        content.mount(grid)

        for title, color in self.palette.colors.items():
            grid.mount(ColorButton(title=title, hex_code=color.value))

    def watch_palette_file_path(self, old_path: Path, new_path: Path) -> None:
        if self._suppress_palette_watch:
            return

        try:
            self.palette = self._load_palette(new_path)
        except Exception as e:
            self.palette = None
            self._last_failed_palette_path = new_path
            self._last_palette_error = str(e)

            if self.is_running:
                self.notify(self._last_palette_error, severity="error")
                self._render_content()

            return

        self._last_failed_palette_path = None
        self._last_palette_error = None

        if self.is_running:
            self._render_content()

    def _on_palette_path_chosen(self, result: Optional[Path]) -> None:
        if result is not None:
            self.palette_file_path = result

    def _focus_move(self, steps: int, *, forward: bool) -> None:
        for _ in range(steps):
            if forward:
                self.screen.focus_next(ColorButton)
            else:
                self.screen.focus_previous(ColorButton)

    def action_open_input(self):
        self.push_screen(InputScreen(), callback=self._on_palette_path_chosen)

    def on_key(self, event: events.Key) -> None:
        match event.key:
            case "l":
                self._focus_move(1, forward=True)
            case "h":
                self._focus_move(1, forward=False)
            case "j":
                self._focus_move(HomeGrid.COL_COUNT, forward=True)
            case "k":
                self._focus_move(HomeGrid.COL_COUNT, forward=False)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PALETTE_PATH
    app = StylixViewer(palette_path=path)
    app.run()
