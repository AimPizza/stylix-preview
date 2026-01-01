from textual.widget import Widget


class HomeGrid(Widget):
    """Container for the layout of the homescreen."""

    COL_COUNT = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.styles.padding = 1
        self.styles.layout = "grid"
        self.styles.grid_size_columns = self.COL_COUNT
        self.styles.grid_gutter_horizontal = 1
        self.styles.grid_gutter_vertical = 2
        self.styles.grid_rows = "auto"
