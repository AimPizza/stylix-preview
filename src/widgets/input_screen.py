from pathlib import Path
from typing import Optional

from constants import DEFAULT_PALETTE_PATH
from textual.app import ComposeResult
from textual.containers import Grid
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Input


class InputScreen(ModalScreen[Optional[Path]]):
    """Screen with a dialog to choose a palette path."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Input an absolute path to your json palette."),
            Input(placeholder=DEFAULT_PALETTE_PATH, id="path_input"),
            Button("Submit", variant="primary", id="submit"),
            Button("Cancel", id="cancel"),
            id="dialog",
        )

    def _get_path(self) -> Optional[Path]:
        value = self.query_one("#path_input", Input).value.strip()
        if not value:
            return None
        return Path(value).absolute()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # This is what Enter in the Input actually triggers
        event.stop()
        self.dismiss(self._get_path())

    def on_key(self, event: Key) -> None:
        if event.key == "escape":
            event.stop()
            self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "submit":
            self.dismiss(self._get_path())
