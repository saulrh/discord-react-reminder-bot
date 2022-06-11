import sqlite3
import pathlib
from typing import Optional, NewType
import dataclasses
import datetime
from absl import logging as absl_logging


UserId = NewType("UserId", int)
MessageId = NewType("MessageId", int)


@dataclasses.dataclass
class Reminder:
    user_id: int
    message_id: int
    remind_at: datetime.datetime


class LocaleAwarenessRequiredError(Exception):
    pass


class ReminderDatabase:
    def __init__(self, path: pathlib.Path):
        self._con = sqlite3.connect(path)
        self._ensure_schema()

    def _ensure_schema(self):
        absl_logging.info("Setting db schema")
        self._con.execute(
            "CREATE TABLE IF NOT EXISTS reminders ("
            "user_id INTEGER NOT NULL, "
            "message_id INTEGER NOT NULL, "
            "emoji TEXT NOT NULL, "
            "remind_at INTEGER NOT NULL, "
            "PRIMARY KEY(user_id, message_id, emoji))"
        )
        self._con.commit()

    def set_reminder(
        self,
        user_id: UserId,
        message_id: MessageId,
            emoji: str,
        remind_at: datetime.datetime,
    ):
        self._con.execute(
            "INSERT OR REPLACE INTO reminders "
            "(user_id, message_id, emoji, remind_at) "
            "VALUES (:user_id, :message_id, :emoji, :remind_at)",
            {
                "user_id": user_id,
                "message_id": message_id,
                "emoji": emoji,
                "remind_at": remind_at.timestamp(),
            },
        )
        self._con.commit()

    def unset_reminder(self, user_id: UserId, message_id: MessageId, emoji: str):
        self._con.execute(
            "DELETE FROM reminders "
            "WHERE user_id = :user_id "
            "AND message_id = :message_id "
            "AND emoji = :emoji ",
            {"user_id": user_id, "emoji": emoji, "message_id": message_id},
        )
        self._con.commit()

    def next_reminder(self) -> Optional[Reminder]:
        cur = self._con.execute(
            "SELECT user_id, message_id, remind_at FROM reminders "
            "ORDER BY remind_at ASC "
            "LIMIT 1"
        )
        res = cur.fetchone()
        if res:
            return Reminder(*res)
        else:
            return None
