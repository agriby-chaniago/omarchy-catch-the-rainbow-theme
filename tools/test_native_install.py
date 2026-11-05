#!/usr/bin/env python3
"""Test the actual Omarchy installer in an isolated temporary home.

Requires an installed Omarchy with its native theme commands on PATH. This
does not switch the active desktop's theme or run the optional full bundle.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import tomllib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--url", default="https://github.com/agriby-chaniago/omarchy-catch-the-rainbow-theme")
parser.add_argument("--report", type=Path)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="ctr-native-install-") as temporary:
    home = Path(temporary)
    environment = os.environ.copy()
    for key in ["WAYLAND_DISPLAY", "DISPLAY", "HYPRLAND_INSTANCE_SIGNATURE", "DBUS_SESSION_BUS_ADDRESS", "OMARCHY_THEME_SKIP_BACKGROUND"]:
        environment.pop(key, None)
    environment.update({
        "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".local/share"), "XDG_STATE_HOME": str(home / ".local/state"),
        "XDG_CACHE_HOME": str(home / ".cache"), "XDG_RUNTIME_DIR": str(home / "run"),
        "OMARCHY_THEME_HEADLESS": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
    })
    (home / "run").mkdir(mode=0o700)
    (home / ".local/state/omarchy/current").mkdir(parents=True)
    result = subprocess.run(["omarchy", "theme", "install", args.url], env=environment, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    current = home / ".local/state/omarchy/current"
    theme = current / "theme"
    source = home / ".config/omarchy/themes/catch-the-rainbow"
    assert (source / ".git").is_dir(), "Native repository install path was not exercised"
    assert (current / "theme.name").read_text().strip() == "catch-the-rainbow"
    assert (current / "background").is_symlink()
    assert hashlib.sha256((current / "background").read_bytes()).hexdigest() == "d433f438bb72eeeb174f3ec0c926a8be1265bfe8d64b128419997db54129ca23"
    palette = tomllib.loads((theme / "colors.toml").read_text())
    assert palette["mode"] == "light" and palette["background"] == "#b8bfce"
    for name in ["kitty.conf", "alacritty.toml", "foot.ini", "ghostty.conf", "hyprland.lua", "neovim.lua", "shell.toml"]:
        assert (theme / name).is_file(), name
        assert "{{" not in (theme / name).read_text(), name
    assert "background #b8bfce" in (theme / "kitty.conf").read_text()
    assert 'background = "#b8bfce"' in (theme / "alacritty.toml").read_text()
    shell = tomllib.loads((theme / "shell.toml").read_text())
    overrides = 0
    for fragment in source.glob("shell.*.toml"):
        for section, values in tomllib.loads(fragment.read_text()).items():
            for key, value in values.items():
                assert shell[section][key] == value, (section, key)
                overrides += 1
    assert not (home / ".config/omarchy/plugins").exists(), "Standard theme installed custom plugins"
    assert not (home / ".config/omarchy/hooks").exists(), "Standard theme installed hooks"
    report = {
        "passed": True, "url": args.url,
        "commit": subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip(),
        "omarchy": subprocess.check_output(["omarchy", "version"], text=True).strip(),
        "freshHome": True, "nativeRepositoryInstall": True, "headlessNoActiveSession": True,
        "generatedTerminalAndEditorConfigs": True, "shellOverrideValuesChecked": overrides,
        "wallpaperMatchesSelectedOriginal": True, "customPluginsOrHooksInstalled": False,
    }
if args.report:
    args.report.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
