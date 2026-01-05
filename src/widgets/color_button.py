
import pyperclip
from textual.reactive import reactive
from textual.widgets import Button
from models.color import Color


class ColorButton(Button):

    title = reactive("")
    hex_code = reactive("#000000")

    def __init__(self, title: str, hex_code: str, **kwargs):
        super().__init__(self._format_label(title, hex_code), **kwargs)
        self.title = title
        self.hex_code = hex_code
        self._apply_color_styles()

    def watch_title(self, _: str, __: str) -> None:
        self._sync_label()

    def watch_hex_code(self, _: str, __: str) -> None:
        self._sync_label()
        self._apply_color_styles()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pyperclip.copy(self.hex_code)
        self.notify(f"copied: {self.hex_code}")

    @staticmethod
    def _format_label(title: str, hex_code: str) -> str:
        return f"{title}\n{hex_code}"

    def _sync_label(self) -> None:
        self.label = self._format_label(self.title, self.hex_code)

    def _apply_color_styles(self) -> None:
        self.styles.background = self.hex_code
        self.styles.background_tint = "transparent"  # removes tint when btn is focused
        # Pick readable foreground (simple luminance check).
        r, g, b = Color.hex_to_rgb(self.hex_code)
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        self.styles.color = "black" if luminance > 140 else "white"
