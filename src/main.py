from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button
from textual.reactive import reactive, Reactive


class ColorButton(Button):
    """A button that accepts a color (hex) and uses this as its background color."""

    color: Reactive[str] = reactive("#000000")

    def __init__(self, color: str, label: str | None = None, **kwargs):
        super().__init__(label or color, **kwargs)
        self.color = color

    def on_mount(self) -> None:
        self.styles.background = self.color

    def watch_color(self, color: str) -> None:
        self.styles.background = color


class StylixViewer(App):
    """A Textual app to inspect Stylix palettes."""

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ColorButton(color="#191d0c")
        yield ColorButton(color="#59421e")


if __name__ == "__main__":
    app = StylixViewer()
    app.run()
