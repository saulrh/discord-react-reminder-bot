import click
import os
import enum

from react_reminder import bot
from react_reminder import scheduler


_TOKEN = os.environ.get("REACT_REMINDER_BOT_TOKEN")


class AdminOp(enum.Enum):
    pass

