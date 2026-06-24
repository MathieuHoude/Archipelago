# Mega Man 7 — RAM Map
# All addresses are WRAM offsets (CPU address = offset + $7E0000)
# Confirmed via MesenCE memory viewer and write breakpoints

## Controller Input

| Address | Description |
|---|---|
| `0x00A0` | Unknown (part of controller block) |
| `0x00A1` | Controller held — R/L triggers, X/A buttons |
| `0x00A2` | Controller held — Start/Select, Y/B buttons, D-pad |
| `0x00A3` | Controller held — R/L triggers, X/A buttons (mirror?) |
| `0x00A4` | Controller held — Start/Select, Y/B buttons, D-pad (mirror?) |
| `0x00A5` | Controller pressed this frame only — mirrors 0x00A1/0x00A3 |
| `0x00A6` | Controller pressed this frame only — mirrors 0x00A2/0x00A4 |

⚠️ These addresses are in the $00A0-$00A7 range — avoid using them
for AP custom flags. Your free WRAM block at $7E1800+ is safely clear.

## Player State

| Address | Size | Description |
|---|---|---|
| `0x0B79` | 1 byte | Set to 1 on new game. Purpose unknown, possibly difficulty/game mode |
| `0x0B7A` | 1 byte | Robot Museum completed flag (0 = not completed, 1 = completed) |
| `0x0B7B` | 1 byte | "4 new stages added" animation played flag (0 = not played, 1 = played) |
| `0x0B7C` | 1 byte | Wily Castle access (0 = locked, 1 = Wily 1, 2 = Wily 2, 3 = Wily 3, 4 = Wily 4) |
| `0x0B78` | 1 byte | Proto Man encounter flags (bit 0 = Clue 1 found, bit 1 = Clue 2 found) |
| `0x0B81` | 1 byte | Lives counter (real value, default 2) |
| `0x0C2E` | 1 byte | Health (real value) |
| `0x0BD1` | 1 byte | Health (display copy, overwritten each frame from 0x0C2E) |

## Bolt Counter

| Address | Size | Description |
|---|---|---|
| `0x0BA6` | 1 byte | Bolts low byte (plain binary, units) |
| `0x0BA7` | 1 byte | Bolts high byte (total = BA7 * 256 + BA6, max 999) |

## Unique Items Bitfield — `0x0BA4`

| Bit | Value | Item |
|---|---|---|
| Bit 0 | 1 | R Circuit Plate |
| Bit 1 | 2 | U Circuit Plate |
| Bit 2 | 4 | S Circuit Plate |
| Bit 3 | 8 | H Circuit Plate |
| Bit 4 | 16 | Hyper Bolt |
| Bit 5 | 32 | Exit Unit |
| Bit 6 | 64 | Hyper Rocket Buster |
| Bit 7 | 128 | Energy Balancer |

## Mega Items Bitfield — `0x0BB1`

| Bit | Value | Item |
|---|---|---|
| Bit 0 | 1 | Junk Man Mega Bolt |
| Bit 1 | 2 | Turbo Man Mega Bolt |
| Bit 2 | 4 | Shade Man Mega Bolt |
| Bit 3 | 8 | Cloud Man Mega Bolt |
| Bit 4 | 16 | Mega Health Capsule |
| Bit 5 | 32 | Spring Man Mega Bolt |
| Bit 6 | 64 | Unknown (breakpoint set) |
| Bit 7 | 128 | Unknown (breakpoint set) |

## Weapon Bytes
# Structure: bit 7 = acquired flag, bits 4-0 = ammo (max 28 / 0x1C)
# Bits 6-5 unused (always 0 in normal gameplay)
# Injection formula: write 0x80 | 28 = 0x9C
# Beat exception: bit 7 = acquired, bits 4-0 = whistle count (max 4)
# Injection formula for Beat: write 0x80 | 4 = 0x84

| Address | Weapon |
|---|---|
| TBD | Freeze Cracker |
| TBD | Danger Wrap |
| TBD | Thunder Bolt |
| TBD | Junk Shield |
| TBD | Slash Claw |
| TBD | Wild Coil |
| TBD | Noise Crush |
| TBD | Scorch Wheel |
| TBD | Rush Coil (starting item) |
| TBD | Rush Search |
| TBD | Rush Jet |
| TBD | Super Adapter |
| TBD | Proto Shield |
| TBD | Beat |

## Proto Man Encounter Flags — `0x0B78`

| Bit | Value | Description |
|---|---|---|
| Bit 0 | 1 | Proto Man's Clue 1 found (Cloud Man stage) |
| Bit 1 | 2 | Proto Man's Clue 2 found (Turbo Man stage) |

## AP Custom Flags — $7E1800-$7E180F
# Confirmed free: $7E1800-$7E1D8F (verified unused across full playthrough)

| Address | Description |
|---|---|
| `$7E1800` | Boss check flags byte 1 (8 main bosses, TBD bit order) |
| `$7E1801` | Boss check flags byte 2 (Mash + Wily bosses, TBD) |
| `$7E1802` | Additional check flags (Bass, Proto Man, TBD) |
| `$7E1803` | AP item receive ID (low byte) |
| `$7E1804` | AP item receive ID (high byte) |
| `$7E1805` | AP execute flag (1 = give item, 0 = idle) |
| `$7E1806` | Items received index (low byte) |
| `$7E1807` | Items received index (high byte) |
| `$7E1808` | AP connection state |
| `$7E1809-$7E180F` | Reserved |

## Free ROM Space
# PRG ROM offsets: $007BA6-$007FFF
# CPU addresses:   $C07BA6-$C07FFF
# Size: ~1114 bytes

### Planned ROM patch layout
| Address | Routine |
|---|---|
| `$C07BA0` | AP_SetStartingBolts (confirmed working) |
| `$C07BB0` | AP_SetNewGameFlags (sets 0x0B7A + 0x0B7B = 1) |
| `$C07BC0` | AP_BossDeath hook (TBD) |
| `$C07BE0` | AP_ItemReceive routine (reuses Proto Shield text window) |
| `$C07C10` | Reserved |

## Initialization Routines

### New game routine 1 — $C00BE8
Sets lives (0x0B81 = 2), clears player state

### New game routine 2 — $C00C1E
Clears 0x0BA4 (unique items), 0x0BA6/0x0BA7 (bolts)
AP patch: also sets 0x0B7A = 1, 0x0B7B = 1 here

## Known UI Routines

### Proto Shield text window
Displays item received text — candidate for AP item notification reuse
ROM address: TBD (needs disassembly trace)

## Outstanding / TBD

- All individual weapon addresses
- Bass checkpoint system (not yet understood)
- `0x0BB1` bits 6 and 7 (breakpoint active)
- Proto Shield text window ROM address
- Wily 3 confirmed needs can_traverse_vertical