import datetime


def next_datetime(
    now: datetime.datetime,
    then: datetime.time,
    then_timezone: datetime.tzinfo,
):
    now_in_timezone = now.astimezone(then_timezone)
    today_in_timezone = now_in_timezone.date()
    then_today = datetime.datetime.combine(today_in_timezone, then, then_timezone)
    if then_today > now:
        return then_today
    else:
        tomorrow_in_timezone = today_in_timezone + datetime.timedelta(days=1)
        then_tomorrow = datetime.datetime.combine(
            tomorrow_in_timezone, then, then_timezone
        )
        return then_tomorrow
