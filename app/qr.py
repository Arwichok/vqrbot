import io

import qrcode
from PIL import Image, ImageDraw

from app.constants import TEXT, FONT_SIZE, FONT, TG_LOGO, L_TEXT


def get_qr(data: str):
    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_L)
    size = img.pixel_size
    tx, ty = int(size - L_TEXT * FONT_SIZE / 2), int(size - FONT_SIZE - FONT_SIZE / 4)
    bg = Image.new("RGBA", (size, size))
    bg.paste(img, (0, 0))
    sec = TG_LOGO.resize((FONT_SIZE, FONT_SIZE))
    bg.paste(sec, (tx - FONT_SIZE, int(ty + FONT_SIZE / 4)), mask=sec)
    ImageDraw.Draw(bg).text((tx, ty), TEXT, fill="black", font=FONT)
    # lx = int(size/2-FS*1.5)
    # ts = int(size/2-FS)
    # qr_logo = logo.resize((FS*3,FS*3))
    # bg.paste(qr_logo, (lx,lx))
    # ImageDraw.Draw(bg).text((ts,ts), "VQR\nBOT", fill="red", font=font, embedded_color=True)
    # bg.show()
    bim = io.BytesIO()
    bg.save(bim, "PNG")
    return bim.getvalue()
