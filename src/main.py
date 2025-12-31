from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button

from widgets.color_button import ColorButton
from widgets.home_grid import HomeGrid


class StylixViewer(App):
    """A Textual app to inspect Stylix palettes."""

    CSS_PATH = "widgets/style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with HomeGrid():
            yield ColorButton(title="Base 00", hex_code="#191d0c")
            yield ColorButton(title="Base 01", hex_code="#59421e")
            yield ColorButton(title="Base blabla", hex_code="#ffffff")
        yield Footer()


if __name__ == "__main__":
    app = StylixViewer()
    app.run()
