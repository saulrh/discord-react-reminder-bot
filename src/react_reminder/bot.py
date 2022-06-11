from absl import logging
import zoneinfo
import discord
import datetime

from react_reminder import emoji
from react_reminder import util
from react_reminder import reminder_db


class ReactReminderClient(discord.Client):
    def __init__(self, reminders: reminder_db.ReminderDatabase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = reminders

    async def on_raw_reaction_add(self, event: discord.RawReactionActionEvent):
        time = emoji.emoji_to_time(event.emoji.name)

        if not time:
            return
        
        remind_at = util.next_datetime(
            now=datetime.datetime.now(datetime.timezone.utc),
            then=time,
            # TODO: stop hardcoding the timezone!
            then_timezone=zoneinfo.ZoneInfo("America/Los_Angeles"),
        )
        logging.info(
            f"{event.user_id} added reaction '{event.emoji}' to message {event.message_id}, storing reminder for {remind_at}"
        )
        self._db.set_reminder(
            user_id=reminder_db.UserId(event.user_id),
            message_id=reminder_db.MessageId(event.message_id),
            emoji=event.emoji.name,
            remind_at=remind_at,
        )
        self.update_queue();

    async def on_raw_reaction_remove(self, event: discord.RawReactionActionEvent):
        time = emoji.emoji_to_time(event.emoji.name)

        if not time:
            return

        logging.info(
            f"{event.user_id} removed reaction '{event.emoji}' from message {event.message_id}"
        )
        self._db.unset_reminder(
            reminder_db.UserId(event.user_id), reminder_db.MessageId(event.message_id),
            emoji=event.emoji.name,
        )
        self.update_queue();

    def update_queue(self):
        pass
