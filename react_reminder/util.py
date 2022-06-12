import datetime
import itertools


def next_datetime(
    now: datetime.datetime,
    then: datetime.time,
    then_timezone: datetime.tzinfo,
):
    now_in_tz = now.astimezone(then_timezone)
    today_in_tz = now_in_tz.date()
    then_in_tz = then.replace(tzinfo=then_timezone)

    # Produce all datetimes that could possibly match the spec within
    # at least 24 hours of the current time
    days = [
        today_in_tz + datetime.timedelta(days=-1),
        today_in_tz,
        today_in_tz + datetime.timedelta(days=1),
    ]
    hour_numbers = [
        then_in_tz.hour - 12,
        then_in_tz.hour,
        then_in_tz.hour + 12,
    ]
    hours = [then_in_tz.replace(hour=h) for h in hour_numbers if 0 <= h <= 23]
    all_times = [datetime.datetime.combine(day, hour, then_timezone) for day, hour in itertools.product(days, hours)]
    # Pick the next one in the future.
    future_times = [t for t in all_times if t > now]
    return min(future_times)
