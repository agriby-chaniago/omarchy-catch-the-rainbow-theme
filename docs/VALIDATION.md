# Beta validation

The initial public beta targets the installed Omarchy 4.0.6-1 API, Hyprland 0.56.2 and Quickshell 0.3.2. This is a tested target, not a claim of compatibility with every Omarchy version.

## Standard theme

`python3 tools/check_theme.py` validates the light palette, shell fragment syntax, native install boundary, 16:9 preview and original artwork hash.

`python3 tools/test_native_install.py` runs the actual `omarchy theme install` command against the public repository URL, with a new temporary home, separate state/config/cache directories and headless mode. It checks native generation of terminal/editor/compositor configuration, all shell override values, the selected wallpaper, and that no custom plugins or hooks are installed. It does not change the active desktop.

The preview shows a real isolated Hyprland compositor running the native Omarchy shell, Kitty and VS Code with example content. It uses the standard repository theme and its own clean editor profile. The selected wallpaper is unchanged. No personal application windows, notifications or cursor are included.

## Optional full bundle

The full bundle's installation and restore code is tested against temporary account directories. The six scenarios cover complete installation/restoration, failure rollback, later user-edit conflicts, damaged-backup refusal, provider scoping/JSONC preservation, and conversion from an existing standard Git checkout followed by restoration.

Its runtime payload passes manifest, SVG, Xcursor, Hyprcursor and terminal-palette checks. All 61 Xcursor shapes were rebuilt from the included editable source and compared byte-for-byte with the shipped files.

The previous personal bundle was exercised on the author's active desktop. The public beta adds the standard-checkout conversion path; that path is tested with isolated file journals and native theme staging. A full public-bundle install/restore on a second physical machine has not been performed.

## Limits

No reboot, interactive lock/unlock, OS upgrade, or cross-version plugin update is part of this beta's validation. Screenshots use an isolated session and example terminal/editor content. Theme colors and native installation are verified separately from any claims about hardware brightness, battery use or performance.
