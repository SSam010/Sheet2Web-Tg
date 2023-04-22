import asyncio
import logging
import time
from datetime import datetime
from xml.etree import ElementTree

import gspread
import psycopg2
import requests
import telegram

from notification_to_telegram import send_notification
from orders_website.settings import GOOGLE_API_KEY_JSON_NAME, DB_HOST, DB_PORT, \
    UPDATE_PERIOD, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

check_data = 0


# Getting the exchange rate of the ruble against the dollar
def get_rate() -> float:
    global check_data

    check_data = datetime.now()

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    xml_string = response.content.decode('windows-1251')
    root = ElementTree.fromstring(xml_string)
    for valute in root.findall('Valute'):
        if valute.find('CharCode').text == 'USD':
            usd_rate = float(valute.find('Value').text.replace(',', '.'))
            return usd_rate


# Calculating the price in rubles and adding relevant records to the database
def transform_load_date(rows_from_worksheet):
    for row in rows_from_worksheet:
        # Calculating the price in rubles
        price_rub = round(float(row['стоимость,$']) * usd_rate_now, 2)
        row['стоимость в руб.'] = price_rub

        # Delivery late checking
        order_delivery_time = datetime.strptime(row['срок поставки'], "%d.%m.%Y")
        if order_delivery_time < time_now:
            expired_delivery.append(f"заказ {row['заказ №']}, дата доставки {row['срок поставки']} просрочен")

        # adding relevant records to the database
        query_add = """INSERT INTO single_orders (id, order_number, price_usd, delivery_time, price_rub) 
        VALUES ({}, {}, {}, '{}', {})""".format(
            row['№'], row['заказ №'], row['стоимость,$'], order_delivery_time, row['стоимость в руб.'])

        # Executing the request
        cur.execute(query_add)


if __name__ == "__main__":
    # Connecting Google API key file
    gs = gspread.service_account(filename=GOOGLE_API_KEY_JSON_NAME)

    while True:
        # Connecting table by ID
        table_id = '1JNmSvJYdw8nXXMGoyyrk2mJjsIhZNr0_Qd_wzk1gQFk'
        sheets = gs.open_by_key(table_id)

        # Getting the first sheet from table
        worksheet = sheets.sheet1
        rows = worksheet.get_all_records()

        # Getting the exchange rate
        if check_data != datetime.today():
            usd_rate_now = get_rate()

        # Making a connection to the database
        connection_db = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER,
                                         password=POSTGRES_PASSWORD, host=DB_HOST,
                                         port=DB_PORT)
        cur = connection_db.cursor()

        # Deleting old records from a table in a database
        query_for_delete_notes = "DELETE FROM single_orders"
        # Executing the request
        cur.execute(query_for_delete_notes)

        # Getting the current time and creating an empty list with expired orders
        time_now = datetime.now()
        expired_delivery = list()

        transform_load_date(rows)

        # Closing the database connection
        connection_db.commit()
        connection_db.close()

        # Outputting logs to the console
        logging.basicConfig(level=logging.INFO)
        logging.info('Data update completed')

        # Sending numbers of late orders to telegram
        try:
            if len(expired_delivery) > 0:
                message = '\n'.join(expired_delivery)
                asyncio.run(send_notification(message))
        except telegram.error.InvalidToken:
            logging.error(
                'The message in Telegram was not sent. Please check the correctness of the TELEGRAM_BOT_ID input.')
        except telegram.error.BadRequest:
            logging.error(
                'The message in Telegram was not sent. Please check the correctness of the TELEGRAM_CHAT_ID input.')

        # Entering standby mode
        time.sleep(int(UPDATE_PERIOD))
