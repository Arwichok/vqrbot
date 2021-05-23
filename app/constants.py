from pathlib import Path

from PIL import Image, ImageFont


SESSION = "session"
BASE_PATH = str(Path(__file__).parent.parent)
TG_LOGO = Image.open(BASE_PATH + "/tg_logo.png")
FONT_SIZE = 20
FONT = ImageFont.truetype(BASE_PATH + "/G_ari_i.TTF", FONT_SIZE)
TEXT = "vqrbot"
L_TEXT = len(TEXT)
DB_FILE = BASE_PATH + "/vqr.db"
CONNECTION = "connection"
TELEGRAPH = "https://telegra.ph"