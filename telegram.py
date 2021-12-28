import telebot

token = '5087527978:AAFvsAyZ0_5m4pixFE41WRqS7BtlEi3U1jc'
bot = telebot.TeleBot(token, threaded=False)

def send_message_new_price(chatid, message):
    bot.send_message(chatid, message)
