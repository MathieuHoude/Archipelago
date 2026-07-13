import unittest

from .. import names
from ..client import WILY_FLAG_TO_LOCATION


class TestMM7ClientMappings(unittest.TestCase):
    def test_wily_flags_send_reward_locations(self) -> None:
        expected = {
            0x01: names.guts_man_g_defeated_item,
            0x02: names.gamerizer_defeated_item,
            0x04: names.hannya_ned_defeated_item,
        }

        self.assertEqual(expected, WILY_FLAG_TO_LOCATION)

    def test_wily_flags_do_not_send_event_locations(self) -> None:
        event_locations = {
            names.guts_man_g_defeated,
            names.gamerizer_defeated,
            names.hannya_ned_defeated,
        }

        for location_name in WILY_FLAG_TO_LOCATION.values():
            with self.subTest(location=location_name):
                self.assertNotIn(location_name, event_locations)