from textual.widget import Widget


class HomeGrid(Widget):
    """Container for the layout of the homescreen."""

    DEFAULT_CSS = """
    HomeGrid {
        layout: grid;
        grid-size: 4;
        grid-gutter: 1;
    }
    """
