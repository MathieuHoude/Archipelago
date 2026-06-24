from pathlib import Path
import subprocess
import bsdiff4

ROOT = Path(__file__).resolve().parents[3]

clean_rom = ROOT / "worlds/mm7/build/mm7_clean.sfc"
patched_rom = ROOT / "worlds/mm7/build/mm7_patched.sfc"
asm_patch = ROOT / "worlds/mm7/src/mm7_ap.asm"
output_patch = ROOT / "worlds/mm7/data/mm7_basepatch.bsdiff4"

if not clean_rom.exists():
    raise FileNotFoundError(f"Missing clean ROM: {clean_rom}")

patched_rom.write_bytes(clean_rom.read_bytes())

subprocess.run(
    ["asar", str(asm_patch), str(patched_rom)],
    check=True,
)

output_patch.parent.mkdir(parents=True, exist_ok=True)
output_patch.write_bytes(
    bsdiff4.diff(clean_rom.read_bytes(), patched_rom.read_bytes())
)

print(f"Wrote {output_patch}")
print(f"Clean ROM:   {clean_rom}")
print(f"Patched ROM: {patched_rom}")