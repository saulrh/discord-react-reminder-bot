from react_reminder import bot
from react_reminder import path_flag
from react_reminder import reminder_db
import discord
import os
from absl import app
from absl import flags


_TOKEN = os.environ.get("REACT_REMINDER_BOT_TOKEN")


_DB_PATH = path_flag.DEFINE_path(
    "db_path",
    "reminders.sqlite",
    "Path to the sqlite database for persisting reminders",
)


def main(argv):
    # unused
    del argv

    reminders = reminder_db.ReminderDatabase(_DB_PATH.value)
    client = bot.ReactReminderClient(
        reminders=reminders,
        intents=discord.Intents(messages=True, reactions=True, guilds=True),
    )
    client.run(_TOKEN)


if __name__ == "__main__":
    app.run(main)
