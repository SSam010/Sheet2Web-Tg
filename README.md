# Project Overview

This is a personal project that allows you to fetch data from Google Sheets, perform necessary data transformations, and load them into PostgreSQL. The project includes a one-page website built using Django. Additionally, there is an optional feature for sending notifications via Telegram bot.

The entire project is dockerized and ready to be deployed.

# Setup and Launch

1. Unzip the pgdb archive in the current directory (without creating an additional folder with the archive name!).

2. Specify the settings in the ".env" file located in the project's root directory. The mandatory settings are:
   - `GOOGLE_API_KEY_JSON_NAME`: Place the Google API KEY file in JSON format in the current directory (orders_website) and pass the file name as a value to this key. Instructions for obtaining the Google API Key can be found in open sources, for example, https://habr.com/ru/post/483302/.
   - `UPDATE_PERIOD`: The period for updating data from Google Sheets, specified in seconds.

### Optional settings:

To enable notifications in the Telegram bot (in this example, notifications are sent for orders that have missed their delivery deadline), you need to create a Telegram bot. To do this, go to Telegram and follow the instructions for creating a bot provided by @BotFather. After creating a bot, go to the bot and click \start. Then, go to the Telegram bot @userinfobot to get your chat ID.

- `TELEGRAM_BOT_ID`: Specify the API token for your bot.
- `TELEGRAM_CHAT_ID`: Specify your chat ID.
- 
### System settings:

These settings are necessary for the operation of the application and the script for collecting and sending data to the Telegram bot. Please do not modify them unless necessary!

- `POSTGRES_DB`: The name of the database.
- `POSTGRES_USER`: The database user's login.
- `POSTGRES_PASSWORD`: The database user's password.
- `DB_HOST`: The database host.
- `DB_PORT`: The database port.

After specifying the required settings, launch the containers using the following Docker command:
`docker compose up`

The containers are now deployed and ready to use!

To access the website, use the following URL:
http://localhost:8080/

You should now see a chart showing the price vs order number, a table with data obtained from Google Sheets, and a column showing the calculated price in Russian rubles.

## Additional Notes

The `orders_details_script.py` script in the `~\orders_website\single\scripts\single` directory is responsible for working with Google Sheets, processing and transporting data to the database, and sending notifications via the Telegram bot.

The script for the Telegram bot is located in the same directory and is named `notification_to_telegram.py`.
