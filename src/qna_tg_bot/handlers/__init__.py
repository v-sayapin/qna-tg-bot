from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from qna_tg_bot.utils import find_answer

async def start(update: Update, _) -> None:
    welcome_message = 'Привет, Солнышко 🌞❤️! Напиши часть вопроса, и мой бот найдет для тебя ответ.'
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, _) -> None:
    user_input = update.message.text
    answer = find_answer(user_input)
    await update.message.reply_html(answer)

def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

