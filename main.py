import random
# files
# alphabet
from string import ascii_letters

# model
from model import BOT_CONFIG, model, vectorizer


RUSSIAN_LETTERS = ['ё','й','ц','у','к','е','н','г','ш','щ','з','х','ъ','ф','ы','в','а','п','р','о','л','д','ж','э','я','ч','с','м','и','т','ь','б','ю']
TOKEN = "5005485456:AAGe6MNQTdo2dTGJ_XfKI5VBkaQTa1PEHlU" #smartbot_28_01_bot


# BOT_CONFIG = {
#     "intents": {
#         "hello": {
#             "examples": ["Hi", "Hello", "Good evening"],
#             "responses": ["Hi", "Hello", "Good evening"],
#         },
#         "thanks": {
#             "examples": ["Thank you", "Thanks", "Thank you very much"],
#             "responses": ["You are Welcome", "Ok", "Contact again"],
#         },
#         "goodbuy": {
#             "examples": ["Buy", "Goodbuy", "See you"],
#             "responses": ["Goodbuy", "Buy", "See you later"],
#         },
#         "good": {
#             "examples": ["Good", "Ok", "Very well"],
#             "responses": ["Very well", "Good!", "Well"],
#         },
#         "bad": {
#             "examples": ["Bad", "Very bad", "Poorly"],
#             "responses": ["Sorry", "I apologize", "Excuse me"],
#         },
#     }
# }

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(bot(clean_text(update.message.text)))


def main():
    '''input_text = ""

    while True:
        input_text = input("Enter message: ")
        if input_text == "":
            print("You don't text anything!")
        else:
            bot_answer = bot(clean_text(input_text))
            print(bot_answer)
            if leave(bot_answer):
                break'''
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



def clean_text(text):
    output_text = ""
    for ch in text:
        if ch in ascii_letters or ch in RUSSIAN_LETTERS:
            output_text += ch
    return output_text


def leave(bot_answer):
    exit_intents = ["bye", "goodbye", "while"]
    for intent in exit_intents:
        if bot_answer in BOT_CONFIG["intents"][intent]["responses"]:
            return True
    return False
        

def get_intent(input_text):
    return model.predict(vectorizer.transform([input_text]))[0]


def bot(input_text):
    intent = get_intent(input_text)
    return random.choice(BOT_CONFIG["intents"][intent]["responses"])


if __name__ == "__main__":
    main()