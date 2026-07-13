from BaseClasses import CollectionState

from .bases import MM7TestBase
from .. import names


class TestWilyLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
    }

    def test_wily_capsule_requires_wily_boss_events(self) -> None:
        state = CollectionState(self.multiworld)

        self.assertFalse(
            self.multiworld.get_location(names.wily_capsule, self.player).can_reach(state),
            "Wily Capsule should not be reachable with no Wily boss defeated events.",
        )

        state.collect(self.get_item_by_name(names.guts_man_g_defeated))
        self.assertFalse(
            self.multiworld.get_location(names.wily_capsule, self.player).can_reach(state),
            "Wily Capsule should not be reachable with only Guts Man G defeated.",
        )

        state.collect(self.get_item_by_name(names.gamerizer_defeated))
        self.assertFalse(
            self.multiworld.get_location(names.wily_capsule, self.player).can_reach(state),
            "Wily Capsule should not be reachable with only two Wily bosses defeated.",
        )

        state.collect(self.get_item_by_name(names.hannya_ned_defeated))
        self.assertTrue(
            self.multiworld.get_location(names.wily_capsule, self.player).can_reach(state),
            "Wily Capsule should be reachable after all three Wily boss defeated events.",
        )
    
    def test_guts_man_g_reward_requires_wily_1_access(self) -> None:
        self.assertAccessDependency(
            [names.guts_man_g_defeated_item],
            [[names.wily_1_access]],
            only_check_listed=True,
        )

    def test_gamerizer_reward_requires_wily_2_access(self) -> None:
        self.assertAccessDependency(
            [names.gamerizer_defeated_item],
            [[names.wily_2_access]],
            only_check_listed=True,
        )

    def test_hannya_ned_reward_requires_wily_3_access(self) -> None:
        self.assertAccessDependency(
            [names.hannya_ned_defeated_item],
            [[names.wily_3_access]],
            only_check_listed=True,
        )

    def test_wily_boss_events_require_access_codes(self) -> None:
        self.assertAccessDependency(
            [names.guts_man_g_defeated],
            [[names.wily_1_access]],
            only_check_listed=True,
        )

        self.assertAccessDependency(
            [names.gamerizer_defeated],
            [[names.wily_2_access]],
            only_check_listed=True,
        )

        self.assertAccessDependency(
            [names.hannya_ned_defeated],
            [[names.wily_3_access]],
            only_check_listed=True,
        )