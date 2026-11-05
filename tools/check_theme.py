#!/usr/bin/env python3
"""Check the native theme's data, artwork identity and distribution boundary."""
from pathlib import Path
import hashlib
import json
import struct
import tomllib

ROOT = Path(__file__).resolve().parents[1]
colors = tomllib.loads((ROOT / "colors.toml").read_text())
assert colors["mode"] == "light"
assert colors["background"] == "#b8bfce"
for name in ["foreground", "accent", "selection", "red", "green", "yellow", "blue", "magenta", "cyan", "muted"]:
    value = colors[name]
    assert value.startswith("#") and len(value) == 7, name
    int(value[1:], 16)
for path in ROOT.glob("shell.*.toml"):
    data = tomllib.loads(path.read_text())
    assert list(data) == [path.name.removeprefix("shell.").removesuffix(".toml")], path
assert (ROOT / "icons.theme").read_text().strip() == "Yaru-blue"
assert not any((ROOT / name).exists() for name in ["hyprland.lua", "kitty.conf", "alacritty.toml", "foot.ini", "ghostty.conf", "vscode.json"])
assert not (ROOT / "payload").exists(), "The full bundle must stay opt-in"
editor = json.loads((ROOT / "vscode-theme.json").read_text())
assert editor["type"] == "light"
artwork = ROOT / "backgrounds/blackmore-overcast.jpg"
assert hashlib.sha256(artwork.read_bytes()).hexdigest() == "d433f438bb72eeeb174f3ec0c926a8be1265bfe8d64b128419997db54129ca23"
preview = (ROOT / "preview.png").read_bytes()
assert preview[:8] == b"\x89PNG\r\n\x1a\n"
width, height = struct.unpack(">II", preview[16:24])
assert width * 9 == height * 16, (width, height)
assert b"eXIf" not in preview
readme = (ROOT / "README.md").read_text()
assert "omarchy theme install https://github.com/agriby-chaniago/omarchy-catch-the-rainbow-theme" in readme
assert "Optional full desktop" in readme
assert (ROOT / "LICENSE").read_text().startswith("MIT License")
print(json.dumps({"passed": True, "mode": colors["mode"], "preview": [width, height], "nativeThemeOnly": True, "artworkUnchanged": True}))
