from __future__ import annotations

import hashlib
import os
import pkgutil
from typing import Optional, TYPE_CHECKING

import settings
import Utils
from worlds.Files import APProcedurePatch

if TYPE_CHECKING:
    from . import MegaMan7World


# TODO: replace/add these once you settle on the exact clean ROM.
# Leave empty during early development if you are still validating dumps.
MM7_KNOWN_MD5: set[str] = set()


class MM7Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Mega Man VII (USA) SNES ROM file."""

    rom_file: RomFile = RomFile("Megaman VII (USA).sfc")


class MM7ProcedurePatch(APProcedurePatch):
    """Procedure patch for Mega Man 7.

    Minimal development version.

    Expected data file:
        worlds/mm7/data/mm7_basepatch.bsdiff4

    That bsdiff should be generated from:
        clean base ROM -> ROM with your current ASM patch applied

    The current Python world/client do the AP randomization and SNI sync.
    The ROM patch only installs the runtime hooks/mailbox/check flags.
    """

    game = "Mega Man 7"
    patch_file_ending = ".apmm7"
    result_file_ending = ".sfc"

    # Keep this empty until you confirm exact base ROM checksum(s).
    hash = []

    procedure = [
        ("apply_bsdiff4", ["mm7_basepatch.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "MegaMan7World", patch: MM7ProcedurePatch) -> None:
    """Write files needed by the procedure patch.

    For the current minimal milestone, all ASM changes should live in a
    prebuilt bsdiff file: data/mm7_basepatch.bsdiff4.

    Later, this function can also write slot-specific bytes/tokens such as:
    - AP marker
    - player name
    - seed name
    - options
    - ROM receive ID table, if you decide to externalize it
    """
    basepatch = pkgutil.get_data(__name__, "data/mm7_basepatch.bsdiff4")
    if basepatch is None:
        raise FileNotFoundError(
            "Missing worlds/mm7/data/mm7_basepatch.bsdiff4. "
            "Build it from clean Mega Man 7 ROM -> ASM-patched ROM, then place it in data/."
        )

    patch.write_file("mm7_basepatch.bsdiff4", basepatch)


def get_base_rom_path(file_name: str = "") -> str:
    if file_name:
        return file_name

    options = settings.get_settings()
    file_name = options["mm7_options"]["rom_file"]

    return Utils.user_path(file_name)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    cached_rom: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if cached_rom:
        return cached_rom

    path = get_base_rom_path(file_name)
    with open(path, "rb") as rom_file:
        rom = rom_file.read()

    rom = strip_snes_copier_header(rom)

    if MM7_KNOWN_MD5:
        md5 = hashlib.md5(rom).hexdigest()
        if md5 not in MM7_KNOWN_MD5:
            raise Exception(
                f"Supplied Mega Man 7 ROM does not match known MD5 hashes. Got {md5}."
            )

    setattr(get_base_rom_bytes, "base_rom_bytes", rom)
    return rom


def strip_snes_copier_header(rom: bytes) -> bytes:
    """Remove a 512-byte copier header if present.

    SNES ROM dumps are sometimes distributed with a 0x200-byte copier header.
    Most modern patch workflows expect headerless ROMs.
    """
    if len(rom) % 0x8000 == 0x200:
        return rom[0x200:]
    return rom
