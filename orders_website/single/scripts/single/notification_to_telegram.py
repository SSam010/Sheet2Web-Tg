import telegram

from orders_website.settings import TELEGRAM_BOT_ID, TELEGRAM_CHAT_ID


# Message send function
async def send_notification(message):
    bot = telegram.Bot(token=TELEGRAM_BOT_ID)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
