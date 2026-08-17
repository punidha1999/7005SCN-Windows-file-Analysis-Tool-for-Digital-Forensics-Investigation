import datetime
import unittest

from core.metadata import FileMetadata
from core.timeline import build_timeline, find_timestamp_anomalies


class TimelineTests(unittest.TestCase):
    @staticmethod
    def _meta(created, modified):
        return FileMetadata(
            path="C:/evidence/sample.txt",
            name="sample.txt",
            size=10,
            created=created,
            modified=modified,
            accessed=modified,
            is_hidden=False,
            is_system=False,
            is_readonly=False,
            is_archive=True,
            owner="TEST\\Examiner",
            extension=".txt",
            attributes=0,
        )

    def test_timeline_is_chronological(self):
        created = datetime.datetime(2026, 1, 1, 10, 0, 0)
        modified = datetime.datetime(2026, 1, 2, 11, 0, 0)
        events = build_timeline([self._meta(created, modified)])

        self.assertEqual([event.kind for event in events], ["created", "modified"])
        self.assertLessEqual(events[0].timestamp, events[1].timestamp)

    def test_modified_before_created_is_anomaly(self):
        created = datetime.datetime(2026, 1, 2, 10, 0, 0)
        modified = datetime.datetime(2026, 1, 1, 10, 0, 0)
        anomalies = find_timestamp_anomalies([self._meta(created, modified)])

        self.assertEqual(len(anomalies), 1)


if __name__ == "__main__":
    unittest.main()
