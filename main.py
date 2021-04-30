#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import zsd_fest
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    job_name = str(update.message.chat_id)
    if context.job_queue.get_jobs_by_name(job_name):
        update.message.reply_text('Already started')
        return

    interval = int(context.args[0]) if context.args else 3600
    context.job_queue.run_repeating(alarm, interval=interval, first=1, context=job_name, name=job_name)
    update.message.reply_text(f'Started with interval {interval} secs')


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""

    job = context.job
    context.bot.send_message(job.context, text=zsd_fest.check_place())


def stop(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    job_name = str(update.message.chat_id)
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
        update.message.reply_text('Stopped')
    else:
        update.message.reply_text('Nothing to stop')


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1780327157:AAE6ZGByNpUEPthCpNCKJHOQT4DKnABhlC4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
