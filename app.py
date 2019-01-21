import logging
import os
import random
import re
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ['TELEGRAM_TOKEN']
LC_FILE = "luoghicomuni.txt"

def start(bot, update):
    update.message.reply_text('Benvenuto! Digita il comando /luogocomune o /lc ogni volta che vuoi!')


def help(bot, update):
    update.message.reply_text('Digita il comando /luogocomune o /lc ogni volta che vuoi!')

def luogocomune(bot, update):
    logger.log("### Messaggio ricevuto: '"+update.message.text+"'") 
    textsearch = re.match('^\s*?$', update.message.text)
    filelc = open(LC_FILE, 'r')
    if textsearch != None:
        update.message.reply_text(random.choice(list(filelc)))
    else:
        filelcstr = filelc.read()
        items=re.findall("^.*?"+update.message.text.strip()+".*?$",filelcstr,re.MULTILINE)
        update.message.reply_text(random.choice(list(items)))
    filelc.close()

def add(bot, update):
    logger.log("### SUGGERIMENTO: "+update.message.text)
    update.message.reply_text('Grazie per il suggerimento, provvederemo ad aggiungerlo quanto prima!')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("luogocomune", luogocomune))
        dp.add_handler(CommandHandler("lc", luogocomune))
        dp.add_handler(CommandHandler("add", add))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
