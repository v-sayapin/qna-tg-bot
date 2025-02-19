import logging
from telegram.ext import Application

from qna_tg_bot.config import TG_BOT_TOKEN
from qna_tg_bot.handlers import register_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main() -> None:
    app = Application.builder().token(TG_BOT_TOKEN).build()

    register_handlers(app)

    app.run_polling()

if __name__ == '__main__':
    main()
