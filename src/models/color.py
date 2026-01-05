

class Color:
    """Store a hex value with helper methods."""

    value: str = ""

    def __init__(self, hex_val: str) -> None:
        self.value = hex_val if hex_val.startswith("#") else f"#{hex_val}"
        pass

    @staticmethod
    def hex_to_rgb(hex_str) -> tuple[int, int, int]:
        """Convert hex color (#RRGGBB or RRGGBB) to an (r, g, b) tuple with 0-255 ints."""
        s = hex_str.lstrip("#")
        if len(s) != 6:
            raise ValueError("Expected 6 hex digits")
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
        return (r, g, b)

    @staticmethod
    def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        """Convert an (r, g, b) tuple (0-255 ints) to a hex string '#RRGGBB'.
        Set uppercase=False to return lowercase hex.
        """
        r, g, b = rgb
        if not all(isinstance(x, int) and 0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("RGB values must be integers in 0-255")
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
