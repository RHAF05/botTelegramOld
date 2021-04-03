#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import datetime
import sqlite3

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Este es el comado de ayuda')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def pole(update: Update, _: CallbackContext) -> None:
    """Pole para AP"""
    weekno = datetime.datetime.today().weekday()
    now = datetime.datetime.now()
    hour = now.hour

    db = sqlite3.connect("data.db")
    cursor = db.cursor()

    #sacamos las fecha de consulta
    fecha_ant = "'" + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + "'"
    fecha_act = datetime.datetime(now.year, now.month, (now.day+1))

    # if weekno < 7:
    if weekno < 5 and now.hour>=5:
        if(update.message.text.lower()=="pole"):
            user = update.effective_user
            #Validamos que no se haya hecho la pole
            datos = cursor.execute("SELECT * FROM poles WHERE pole='pole' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
            if len(datos.fetchall())==0:
                registros = ('pole',user.mention_markdown_v2(),3.5,now)
                datos = cursor.execute("INSERT INTO poles(pole,user,points,date) VALUES(?,?,?,?)",registros)
                db.commit()
                update.message.reply_markdown_v2(
                    f'Erda bien y tal, {user.mention_markdown_v2()}\ ha hecho la pole',
                )
        elif (update.message.text.lower()=="plata"):
            user = update.effective_user
            # Validamos que se haya hecho la pole
            datos = cursor.execute("SELECT * FROM poles WHERE pole='pole' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
            if len(datos.fetchall())>0:
                # Validamos que no se haya hecho una plata
                datos = cursor.execute("SELECT * FROM poles WHERE pole='plata' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
                if len(datos.fetchall())==0:
                    #Validamos que si este usuario ya hizo alguna position, no puede hacer plata
                    datos = cursor.execute("SELECT * FROM poles WHERE user='"+str(user.mention_markdown_v2())+"' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
                    if len(datos.fetchall())==0:
                        registros = ('plata',user.mention_markdown_v2(),2,now)
                        datos = cursor.execute("INSERT INTO poles(pole,user,points,date) VALUES(?,?,?,?)",registros)
                        db.commit()
                        update.message.reply_markdown_v2(
                            f'muy bien, {user.mention_markdown_v2()}\ ha hecho la plata',
                        )
        elif (update.message.text.lower()=="bronce"):
            user = update.effective_user
            # Validamos que se haya hecho la plata
            datos = cursor.execute("SELECT * FROM poles WHERE pole='plata' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
            if len(datos.fetchall())>0:
                # Validamos que no se haya hecho una plata
                datos = cursor.execute("SELECT * FROM poles WHERE pole='bronce' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
                if len(datos.fetchall())==0:
                    #Validamos que si este usuario ya hizo alguna position, no puede hacer plata
                    datos = cursor.execute("SELECT * FROM poles WHERE user='"+str(user.mention_markdown_v2())+"' AND date >=  '" +str(now.year) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2) + "'")
                    if len(datos.fetchall())==0:
                        registros = ('bronce',user.mention_markdown_v2(),0.5,now)
                        datos = cursor.execute("INSERT INTO poles(pole,user,points,date) VALUES(?,?,?,?)",registros)
                        db.commit()
                        update.message.reply_markdown_v2(
                            f'Algo es algo, {user.mention_markdown_v2()}\ ha conseguido el bronce',
                        )
        elif (update.message.text.lower()=="fail"):
            user = update.effective_user
            registros = ('fail',user.mention_markdown_v2(),0,now)
            datos = cursor.execute("INSERT INTO poles(pole,user,points,date) VALUES(?,?,?,?)",registros)
            db.commit()
            update.message.reply_markdown_v2(
                f'Al menos lo intento, {user.mention_markdown_v2()}\ ha conseguido un Fail',
            )
    elif (update.message.text.lower()=="poleprueba" or update.message.text.lower()=="plataprueba" or update.message.text.lower()=="bronceprueba" or update.message.text.lower()=="fail"):
        user = update.effective_user
        update.message.reply_markdown_v2(
            f'Deja de molestarme {user.mention_markdown_v2()} que estas no son horas de estar haciendo {update.message.text.lower()}',
        )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1730057456:AAHQ99r1lHoiEmKdl2NpVcza17hipO-lI_A")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, pole))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()