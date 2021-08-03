# Path to assets directory (i.e. images) relative to the output directory.
ASSETS_PATH = "./assets"

# None is regular or chose 'PIL' for Pillow or 'TK' for Tkinter resizing
SCALED_VERSION = 'PIL'
SCALE_RESAMPLE_METHOD = None
if SCALED_VERSION:
    from PIL import Image
    # Resample methods: NEAREST, ANITALIAS, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS
    SCALE_RESAMPLE_METHOD = Image.ANTIALIAS