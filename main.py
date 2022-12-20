from telegram.ext import *
from CONSTANTS import *

print("KoureasBot started...")


def start_command(update,context):
    update.message.reply_text("Type something")

def help_command(update,context):
    update.message.reply_text("help text")

def handle_message(update,context):
    update.message.reply_text(update.message.text+ "...bales")



def main():
    updater = Updater(API_KEY,use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))

    updater.start_polling(5)
    updater.idle()

    
main()