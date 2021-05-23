from aiogram.dispatcher.middlewares import BaseMiddleware

from app.constants import SESSION, CONNECTION
from app.models import create_user, select_user


class VarsMiddleware(BaseMiddleware):
    def __init__(self, session, connection):
        super().__init__()
        self.session = session
        self.connection = connection

    def process(self, msg, data):
        if not select_user(self.connection, msg.from_user.id):
            create_user(self.connection, msg.from_user.id, msg.from_user.full_name)
        data[SESSION] = self.session
        data[CONNECTION] = self.connection

    async def on_pre_process_message(self, msg, data):
        self.process(msg, data)

    async def on_pre_process_inline_query(self, msg, data):
        self.process(msg, data)
