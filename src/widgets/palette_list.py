from dataclasses import dataclass
from pathlib import Path

from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Label, ListItem, ListView


class PaletteChosen(Message):
    """Posted when the user selects a palette in the list."""

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path


class PaletteList(ListView):
    """A fast directory view: one row per palette file."""

    def __init__(self, paths: list[Path], **kwargs) -> None:
        super().__init__(**kwargs)
        self.paths = paths

    def compose(self) -> ComposeResult:
        for p in self.paths:
            yield ListItem(Label(str(p.name)))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        idx = event.index
        if 0 <= idx < len(self.paths):
            self.post_message(PaletteChosen(self.paths[idx]))
