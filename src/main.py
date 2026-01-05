import sys
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

from constants import DEFAULT_PALETTE_PATH
from widgets.palette_view import PaletteView
from widgets.color_button import ColorButton
from widgets.palette_grid import PaletteGrid
from widgets.input_screen import InputScreen
from widgets.palette_list import PaletteChosen, PaletteList


class StylixViewer(App):
    """A Textual app to inspect Stylix palettes."""

    CSS_PATH = "widgets/style.tcss"
    palette_file_path = reactive(Path(DEFAULT_PALETTE_PATH))
    """Path to either a single palette or a directory"""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "open_input", "Pick palette path"),
        ("b", "back_to_list", "Back"),
    ]

    def __init__(self, palette_path: str, **kwargs):
        super().__init__(**kwargs)
        self.palette_file_path = Path(palette_path)
        self._last_dir_paths: list[Path] = []

    def on_mount(self) -> None:
        self.load_palettes()

    def update_title(self) -> None:
        self.title = f"{self.__class__.__name__} - {self.palette_file_path}"

    def _parse_paths(self, recursive: bool = False) -> list[Path]:
        """Get a list of palette files from the configured path."""
        p = self.palette_file_path
        if not p.exists():
            self.notify(f"Invalid path: {self.palette_file_path}", severity="error")
            return []

        def is_palette_file(f: Path) -> bool:
            return f.is_file() and f.suffix.lower() in {".json", ".yml", ".yaml"}

        if p.is_file():
            return [p] if is_palette_file(p) else []
        else:
            files = p.rglob("*") if recursive else p.iterdir()
            return [f for f in files if is_palette_file(f)]

    def _clear_content(self) -> None:
        content = self.query_one("#content", VerticalScroll)
        for child in content.children:
            child.remove()

    def clear_and_get_content(self) -> VerticalScroll:
        self._clear_content()
        return self.query_one("#content", VerticalScroll)

    def load_palettes(self) -> None:
        """Checks the palette path and renders content."""
        file_paths: list[Path] = self._parse_paths()

        clean_content = self.clear_and_get_content()

        if self.palette_file_path.is_dir():
            self._last_dir_paths = sorted(file_paths)
            if not self._last_dir_paths:
                clean_content.mount(Label("No palette files found in directory."))
                return
            clean_content.mount(PaletteList(self._last_dir_paths))
            return

        # File mode: render the single palette.
        if not file_paths:
            clean_content.mount(Label("No palette file selected."))
            return

        p = file_paths[0]
        try:
            clean_content.mount(PaletteView(palette_path=p))
        except Exception as e:
            self.notify(f"Failed to load palette from: {p}\n{e}", severity="error")

    # ACTIONS

    def _on_palette_path_chosen(self, result: Path | None) -> None:
        """Handle optional path chosen by InputScreen"""
        if result is not None:
            self.palette_file_path = result

    def action_open_input(self):
        self.push_screen(InputScreen(), callback=self._on_palette_path_chosen)

    def on_palette_chosen(self, message: PaletteChosen) -> None:
        """Handle selection from PaletteList."""
        content = self.clear_and_get_content()
        try:
            content.mount(PaletteView(palette_path=message.path))
        except Exception as e:
            self.notify(
                f"Failed to load palette from: {message.path}\n{e}", severity="error"
            )

    def action_back_to_list(self) -> None:
        """Back to directory list if we came from a directory."""
        if self.palette_file_path.is_dir():
            self.load_palettes()

    # NAVIGATION

    def _focus_move(self, steps: int = 1, *, forward: bool = True) -> None:
        """Move focus on view by n steps.

        Defaults to 1 step forward."""
        for _ in range(steps):
            if forward:
                self.screen.focus_next(ColorButton)
            else:
                self.screen.focus_previous(ColorButton)

    def on_key(self, event: events.Key) -> None:
        match event.key:
            case "l":
                self._focus_move(1, forward=True)
            case "h":
                self._focus_move(1, forward=False)
            case "j":
                self._focus_move(PaletteGrid.COL_COUNT, forward=True)
            case "k":
                self._focus_move(PaletteGrid.COL_COUNT, forward=False)

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="content")
        yield Footer(show_command_palette=False)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PALETTE_PATH
    app = StylixViewer(palette_path=path)
    app.run()


if __name__ == "__main__":
    main()
