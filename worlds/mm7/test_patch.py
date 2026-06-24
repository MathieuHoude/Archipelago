ROM_PATH = "MM7.sfc"  # asar output

MM7_LIVES_OFFSET = 0x000BF3
MM7_BOLTS_LOW    = 0x007BA1
MM7_BOLTS_HIGH   = 0x007BA6

with open(ROM_PATH, "rb") as f:
    rom = bytearray(f.read())

lives = 5
bolts = 750

rom[MM7_LIVES_OFFSET] = lives
rom[MM7_BOLTS_LOW]    = bolts & 0xFF
rom[MM7_BOLTS_HIGH]   = (bolts >> 8) & 0xFF

with open("mm7_test_python.sfc", "wb") as f:
    f.write(rom)

print(f"Done — lives: {lives}, bolts: {bolts}")