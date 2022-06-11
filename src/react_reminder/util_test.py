from absl.testing import absltest
import datetime
import zoneinfo

from react_reminder import util

_UTC = datetime.timezone.utc
_LA = zoneinfo.ZoneInfo("America/Los_Angeles")


class NextDatetimeTest(absltest.TestCase):
    def test_in_utc(self):
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 4, 30, tzinfo=_UTC),
                then=datetime.time(hour=15, minute=0),
                then_timezone=datetime.timezone.utc,
            ),
            datetime.datetime(2010, 2, 2, 15, 0, tzinfo=_UTC),
        )

    def test_in_la(self):
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 4, 30, tzinfo=_LA),
                then=datetime.time(hour=15, minute=0),
                then_timezone=_LA,
            ),
            datetime.datetime(2010, 2, 2, 15, 0, tzinfo=_LA),
        )

    def test_wrapping(self):
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 14, 30, tzinfo=_UTC),
                then=datetime.time(hour=5, minute=0),
                then_timezone=_UTC,
            ),
            datetime.datetime(2010, 2, 3, 5, 0, tzinfo=_UTC),
        )

    def test_multi_zone(self):
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 14, 30, tzinfo=_UTC),
                then=datetime.time(hour=9, minute=0),
                then_timezone=_LA,
            ),
            datetime.datetime(2010, 2, 2, 9, 0, tzinfo=_LA),
        )
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 3, 30, tzinfo=_LA),
                then=datetime.time(hour=14, minute=0),
                then_timezone=_UTC,
            ),
            datetime.datetime(2010, 2, 2, 14, 0, tzinfo=_UTC),
        )

    def test_wrapping_multi_zone(self):
        self.assertEqual(
            util.next_datetime(
                now=datetime.datetime(2010, 2, 2, 22, 30, tzinfo=_UTC),
                then=datetime.time(hour=1, minute=0),
                then_timezone=_LA,
            ),
            datetime.datetime(2010, 2, 3, 1, 0, tzinfo=_LA),
        )


if __name__ == "__main__":
    absltest.main()
