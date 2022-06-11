import logging
import zoneinfo
import discord
import datetime

import apscheduler.schedulers.base

from react_reminder import emoji
from react_reminder import util


def make_job_id(user_id: int, message_id: int, emoji_name: str) -> str:
    return f"{user_id}-{message_id}-{emoji_name}"


class _ReactReminderClient(discord.Client):
    def __init__(self, scheduler: apscheduler.schedulers.base.BaseScheduler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sched = scheduler

    async def on_raw_reaction_add(self, event: discord.RawReactionActionEvent):
        time = emoji.emoji_to_time(event.emoji.name)

        if not time:
            return
        
        remind_at = util.next_datetime(
            now=datetime.datetime.now(datetime.timezone.utc),
            then=time,
            # TODO: stop hardcoding the user's timezone!
            then_timezone=zoneinfo.ZoneInfo("America/Los_Angeles"),
        )
        logging.info(
            f"{event.user_id} added reaction '{event.emoji}' to message {event.message_id}, storing reminder for {remind_at}"
        )
        job_id = make_job_id(event.user_id, event.message_id, event.emoji.name)
        self._sched.add_job(
            func=ReminderCallback,
            trigger='date',
            args=[event.user_id, event.guild_id, event.channel_id, event.message_id, event.emoji.name],
            id=job_id,
            run_date=remind_at,
        )

    async def on_raw_reaction_remove(self, event: discord.RawReactionActionEvent):
        time = emoji.emoji_to_time(event.emoji.name)

        if not time:
            return

        logging.info(
            f"{event.user_id} removed reaction '{event.emoji}' from message {event.message_id}"
        )
        job_id = make_job_id(event.user_id, event.message_id, event.emoji.name)
        self._sched.remove_job(job_id=job_id)


CLIENT = None
def GetClient(*args, **kwargs) -> _ReactReminderClient:
    global CLIENT
    if not CLIENT:
        CLIENT = _ReactReminderClient(        intents=discord.Intents(messages=True, reactions=True, guilds=True, members=True),
                                              *args, **kwargs)
    return CLIENT



async def ReminderCallback(user_id: int, guild_id: int, channel_id: int, message_id: int, emoji_name: str):
    logging.info(f"Reminding {user_id} of {message_id}")
    client = GetClient()
    user = client.get_user(user_id)
    logging.info(user)
    if not user:
        return
    await user.send(content=f"This is a reminder! You asked to be reminded of a message at this time: https://discord.com/channels/{guild_id}/{channel_id}/{message_id}")
