from __future__ import annotations

import logging
from typing import Dict, Optional

from NetUtils import color
from worlds.AutoSNIClient import SNIClient

from . import names
from .items import rom_receive_id
from .locations import location_name_to_id

snes_logger = logging.getLogger("SNES")

print("MM7 CLIENT.PY LOADED")

# FXPAK Pro / SNI memory mapping.
# See existing SNES/SNI worlds such as Super Mario World.
ROM_START = 0x000000
WRAM_START = 0xF50000

# HiROM internal header. This is intentionally loose for the first prototype.
MM7_ROM_HEADER = ROM_START + 0x00FFC0
ROM_HEADER_SIZE = 0x15

# AP runtime/check block in WRAM.
# These must match your ASM symbols.
AP_BOSS_FLAGS = WRAM_START + 0x1FA1
AP_BOSS_FLAGS_2 = WRAM_START + 0x1FA2
AP_DEBUG_FLAGS = WRAM_START + 0x1FA3
AP_ITEM_ID_LO = WRAM_START + 0x1FA4
AP_ITEM_ID_HI = WRAM_START + 0x1FA5
AP_EXECUTE_FLAG = WRAM_START + 0x1FA6
AP_RECV_INDEX_LO = WRAM_START + 0x1FA7
AP_RECV_INDEX_HI = WRAM_START + 0x1FA8
AP_CONNECTION = WRAM_START + 0x1FA9

# Boss medal/check flag order confirmed from testing:
# 01 = Freeze, 02 = Cloud, 04 = Junk, 08 = Turbo,
# 10 = Slash, 20 = Shade, 40 = Burst, 80 = Spring.
BOSS_FLAG_TO_LOCATION: Dict[int, str] = {
    0x01: names.freeze_man_defeated,
    0x02: names.cloud_man_defeated,
    0x04: names.junk_man_defeated,
    0x08: names.turbo_man_defeated,
    0x10: names.slash_man_defeated,
    0x20: names.shade_man_defeated,
    0x40: names.burst_man_defeated,
    0x80: names.spring_man_defeated,
}


class MM7SNIClient(SNIClient):
    game = "Mega Man 7"
    patch_suffix = ".apmm7"

    async def validate_rom(self, ctx) -> bool:
        # Temporary prototype auth token.
        # Later this should be a real AP ROM marker read from the patched ROM.
        print("MM7 validate_rom called")
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.rom = b"MM7_AP_TEST"

        return True

    async def game_watcher(self, ctx) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # If we are not connected to an AP room yet, do not try to sync.
        if ctx.server is None or ctx.slot is None:
            return

        # 1. Send boss-defeat location checks from ROM flags.
        boss_flags = await snes_read(ctx, AP_BOSS_FLAGS, 1)
        if boss_flags is None:
            return

        new_checks = []
        flags = boss_flags[0]

        for bit, location_name in BOSS_FLAG_TO_LOCATION.items():
            if not flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        if new_checks:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])
            for location_id in new_checks:
                ctx.locations_checked.add(location_id)

        # 2. Deliver received AP items to the ROM-side AP_CheckItemReceive mailbox.
        execute_flag = await snes_read(ctx, AP_EXECUTE_FLAG, 1)
        recv_index_raw = await snes_read(ctx, AP_RECV_INDEX_LO, 2)
        if execute_flag is None or recv_index_raw is None:
            return

        # Wait until the ROM has consumed the previous item.
        if execute_flag[0] != 0:
            return

        recv_index = recv_index_raw[0] | (recv_index_raw[1] << 8)
        if recv_index >= len(ctx.items_received):
            return

        network_item = ctx.items_received[recv_index]

        try:
            item_name: Optional[str] = ctx.item_names.lookup_in_game(network_item.item)
        except Exception:
            # This should not normally happen, but do not crash the client if
            # the item lookup table is incomplete during early development.
            snes_logger.warning("Could not resolve received item id %s", network_item.item)
            return

        receive_id = rom_receive_id.get(item_name)
        if receive_id is None:
            snes_logger.warning("No MM7 ROM receive id for item: %s", item_name)
            return

        sending_player = ctx.player_names.get(network_item.player, f"Player {network_item.player}")
        location_text = ctx.location_names.lookup_in_slot(network_item.location, network_item.player)

        snes_logger.info(
            "Received %s from %s at %s (%d/%d)",
            color(item_name, "red", "bold"),
            color(sending_player, "yellow"),
            location_text,
            recv_index + 1,
            len(ctx.items_received),
        )

        snes_buffered_write(ctx, AP_ITEM_ID_LO, bytes([receive_id & 0xFF]))
        snes_buffered_write(ctx, AP_ITEM_ID_HI, bytes([(receive_id >> 8) & 0xFF]))
        snes_buffered_write(ctx, AP_EXECUTE_FLAG, bytes([0x01]))
        await snes_flush_writes(ctx)

        # Optional future goal handling:
        # Once Wily Capsule writes a ROM flag, read it here and send:
        # await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
