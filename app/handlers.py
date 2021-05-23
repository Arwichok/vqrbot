import asyncio
import logging

from aiogram import types as atp, Dispatcher
from aiogram.dispatcher.filters import CommandStart

from app.constants import TELEGRAPH
from app.models import select_qr, create_qr
from app.qr import get_qr


async def start_cmd(msg: atp.Message):
    await msg.answer("Simple bot for create qr code.\n"
                     "Send text or use inline: <code>@vqrbot test.</code>",
                     parse_mode="html")


async def echo(msg: atp.Message, connection):
    qr = select_qr(connection, msg.text)
    if qr:
        await msg.answer_photo(qr[1] or qr[2])
    else:
        out_msg = await msg.answer_photo(get_qr(msg.text))
        create_qr(connection, msg.text, file_id=out_msg.photo[-1].file_id)
        connection.commit()


async def reply_qr(iq: atp.InlineQuery, session, connection):
    data = iq.query[:-1]
    if not data or not session or not connection:
        return
    db_qr = select_qr(connection, data)
    if not db_qr:
        qr = get_qr(data)
        out = await session.post(TELEGRAPH + "/upload", data={"file": qr})
        src = (await out.json())[0].get("src")
        url = TELEGRAPH + src
        create_qr(connection, data, url=url)
        connection.commit()
        logging.info(f"New qr {data} {url}")
        await asyncio.sleep(2)
        await iq.answer([atp.InlineQueryResultPhoto(id="0", photo_url=url, thumb_url=url)])
    elif url := db_qr[1]:
        await iq.answer([atp.InlineQueryResultPhoto(id="0", photo_url=url, thumb_url=url)])
    elif file_id := db_qr[2]:
        await iq.answer([atp.InlineQueryResultCachedPhoto(id="0", photo_file_id=file_id)])
    else:
        logging.warning(f"Not found file_id or url in data `{data}`")


def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart())
    dp.register_message_handler(echo)
    dp.register_inline_handler(reply_qr, text_endswith=".")
