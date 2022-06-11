from typing import Optional
import datetime

_CLOCKS = {
    "🕛": datetime.time(hour=0, minute=0),
    "🕐": datetime.time(hour=1, minute=0),
    "🕑": datetime.time(hour=2, minute=0),
    "🕒": datetime.time(hour=3, minute=0),
    "🕓": datetime.time(hour=4, minute=0),
    "🕔": datetime.time(hour=5, minute=0),
    "🕕": datetime.time(hour=6, minute=0),
    "🕖": datetime.time(hour=7, minute=0),
    "🕗": datetime.time(hour=8, minute=0),
    "🕘": datetime.time(hour=9, minute=0),
    "🕙": datetime.time(hour=10, minute=0),
    "🕚": datetime.time(hour=11, minute=0),
    "🕧": datetime.time(hour=0, minute=30),
    "🕜": datetime.time(hour=1, minute=30),
    "🕝": datetime.time(hour=2, minute=30),
    "🕞": datetime.time(hour=3, minute=30),
    "🕟": datetime.time(hour=4, minute=30),
    "🕠": datetime.time(hour=5, minute=30),
    "🕡": datetime.time(hour=6, minute=30),
    "🕢": datetime.time(hour=7, minute=30),
    "🕣": datetime.time(hour=8, minute=30),
    "🕤": datetime.time(hour=9, minute=30),
    "🕥": datetime.time(hour=10, minute=30),
    "🕦": datetime.time(hour=11, minute=30),
}


def emoji_to_time(emoji: str) -> Optional[datetime.time]:
    return _CLOCKS.get(emoji, None)
