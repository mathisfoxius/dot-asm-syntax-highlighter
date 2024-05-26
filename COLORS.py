class Color_Palette:
    def __init__(self, DEFAULT, BACKGROUND, NUMBERS_AND_ADDRESSES, MOV, CALL, REGISTERS, BOX_COLOR) -> None:
        self.DEFAULT = DEFAULT
        self.BACKGROUND = BACKGROUND
        self.NUMBERS_AND_ADDRESSES = NUMBERS_AND_ADDRESSES
        self.MOV = MOV
        self.CALL = CALL
        self.REGISTERS = REGISTERS
        self.BOX_COLOR = BOX_COLOR

palette1 = Color_Palette("black", "#fff8dc", "#D94F04", "#007172", "#025259", "#F29325", "white")

# https://atelierbram.github.io/syntax-highlighting/atelier-schemes/forest/
light = Color_Palette("#1b1918","#f1efee", "#c38418", "#407ee7", "#c33ff3", "#f22c40", "white")

dark = Color_Palette("#f1efee","#1b1918", "#c38418", "#407ee7", "#c33ff3", "#f22c40", "#2c2421")

