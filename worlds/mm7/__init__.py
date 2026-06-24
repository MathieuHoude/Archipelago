from __future__ import annotations

import base64
import os
from typing import Any, Dict, List

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import names
from .items import (
    MM7Item,
    item_groups,
    item_name_to_id,
    create_item as create_mm7_item,
)
from .locations import (
    MM7_LOCATION_ID_BASE,
    MM7Location,
    location_table,
)
from .options import MegaMan7Options
from .rom import MM7ProcedurePatch, MM7Settings, patch_rom
from .client import MM7SNIClient


class MegaMan7WebWorld(WebWorld):
    theme = "stone"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Mega Man 7 for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["YourName"],
        )
    ]


# Minimal first milestone:
# These names must match the boss flag mapping in client.py.
#
# ROM/client flag order:
# 01 = Freeze, 02 = Cloud, 04 = Junk, 08 = Turbo,
# 10 = Slash, 20 = Shade, 40 = Burst, 80 = Spring.
MINIMAL_BOSS_LOCATIONS: List[str] = [
    names.freeze_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.turbo_man_defeated,
    names.slash_man_defeated,
    names.shade_man_defeated,
    names.burst_man_defeated,
    names.spring_man_defeated,
]

# One randomized item per minimal boss location.
MINIMAL_ITEM_POOL: List[str] = [
    names.freeze_cracker,
    names.danger_wrap,
    names.thunder_bolt,
    names.junk_shield,
    names.slash_claw,
    names.wild_coil,
    names.noise_crush,
    names.scorch_wheel,
]

# Temporary SNI auth token.
# This must match ctx.rom in client.py validate_rom().
MM7_ROM_AUTH_TOKEN = b"MM7_AP_TEST"


class MegaMan7World(World):
    """Mega Man 7 for Archipelago.

    Minimal development version:
    - creates only 8 Robot Master defeated checks
    - randomizes only the 8 Robot Master weapons
    - relies on the SNI client to read $7E1FA1 boss flags
    - relies on the ROM mailbox to receive items
    """

    game = "Mega Man 7"
    web = MegaMan7WebWorld()

    options_dataclass = MegaMan7Options
    options: MegaMan7Options

    settings: MM7Settings
    settings_key = "mm7_options"

    # Use the canonical AP item ids from items.py.
    # items.py correctly adds MM7_ITEM_ID_BASE and excludes event items.
    item_name_to_id = item_name_to_id
    item_name_groups = item_groups

    # Your full locations.py currently has boss defeated locations as code=None
    # event locations. For this minimal build, we intentionally give these
    # boss-defeat checks real AP location ids here without changing locations.py.
    location_name_to_id = {
        location_name: MM7_LOCATION_ID_BASE + index
        for index, location_name in enumerate(MINIMAL_BOSS_LOCATIONS)
    }

    def create_item(self, name: str) -> MM7Item:
        return create_mm7_item(name, self.player)

    def create_items(self) -> None:
        self.multiworld.itempool += [
            self.create_item(item_name)
            for item_name in MINIMAL_ITEM_POOL
        ]

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        main_stages = Region("Main Stages", self.player, self.multiworld)

        menu.connect(main_stages)

        for location_name in MINIMAL_BOSS_LOCATIONS:
            location_code = self.location_name_to_id[location_name]
            main_stages.locations.append(
                MM7Location(
                    self.player,
                    location_name,
                    location_code,
                    main_stages,
                )
            )

        self.multiworld.regions += [menu, main_stages]

    def set_rules(self) -> None:
        # Minimal milestone:
        # your ROM patch makes all 8 Robot Master stages visible/selectable,
        # so no AP access rules are needed yet.
        pass

    def generate_basic(self) -> None:
        # Temporary minimal goal:
        # receive all 8 Robot Master weapons.
        #
        # This is not the final game goal; it just lets generation succeed and
        # gives you a practical smoke-test objective for the first AP loop.
        self.multiworld.completion_condition[self.player] = lambda state: all(
            state.has(item_name, self.player)
            for item_name in MINIMAL_ITEM_POOL
        )

    def get_filler_item_name(self) -> str:
        # Not used in the 8-location/8-item minimal build.
        return names.small_bolt

    def generate_output(self, output_directory: str) -> None:
        patch = MM7ProcedurePatch(
            player=self.player,
            player_name=self.multiworld.player_name[self.player],
        )
        patch_rom(self, patch)
        patch.write(
            os.path.join(
                output_directory,
                f"MM7_{self.multiworld.player_name[self.player]}_"
                f"{self.multiworld.seed_name}.apmm7",
            )
        )

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        # SNI clients authenticate using base64(ctx.rom), not the normal player name.
        # For now this must match client.py:
        #     ctx.rom = b"MM7_AP_TEST"
        #
        # Later, replace this temporary token with a real ROM marker/name written
        # into the patched ROM, like MMX does with patch.name.
        auth_name = base64.b64encode(MM7_ROM_AUTH_TOKEN).decode()

        player_name = self.multiworld.player_name[self.player]
        multidata["connect_names"][auth_name] = multidata["connect_names"][player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "minimal": True,
            "ap_wram_base": 0x1FA1,
            "boss_flag_order": {
                "freeze": 0x01,
                "cloud": 0x02,
                "junk": 0x04,
                "turbo": 0x08,
                "slash": 0x10,
                "shade": 0x20,
                "burst": 0x40,
                "spring": 0x80,
            },
        }
