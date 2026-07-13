from test.bases import WorldTestBase


class MM7TestBase(WorldTestBase):
    game = "Mega Man 7"

class TestNoBossWeaknessLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": False,
    }