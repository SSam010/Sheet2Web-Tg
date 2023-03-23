import json

import telegram

# Import config file
with open("configuration.json", "r") as f:
    config = json.load(f)


# Message send function
async def send_notification(message):
    bot = telegram.Bot(token=config["TELEGRAM_BOT_ID"])
    await bot.send_message(chat_id=config["TELEGRAM_CHAT_ID"], text=message)
