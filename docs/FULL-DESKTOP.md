# Optional full desktop beta

The standard theme in this repository works through `omarchy theme install`. The full desktop bundle is a separate, explicit installation for **Omarchy 4.0.6-1**.

## Features

- Animated rain lines that follow the weather report's intensity and wind. Rain is limited to the wallpaper and stops when the report is dry.
- Paper folder/file icons and an Oreo-derived cursor with blue, green and rose mask ribbons.
- A custom bar, MPRIS media panel, notification cards, OSD gauges and short pointer/popup animations.
- Theme-scoped GTK and Zen providers, a declarative editor theme, and a Starship prompt.

## Install and restore

Download `catch-the-rainbow-full-1.0.0-beta.1.tar.gz` and `SHA256SUMS` from the [release](https://github.com/agriby-chaniago/omarchy-catch-the-rainbow-theme/releases/tag/v1.0.0-beta.1), verify the checksum, extract the archive and read its README. Then run from the extracted directory:

```sh
./install.py plan
./install.py install
```

Run `./install.py restore` from the same bundle to restore the state before that installation. If files have changed since the installation, restoration stops before writing and reports the conflicts. `--force` keeps a separate copy of the conflicting files before restoring.

The installer records affected files, symlinks and appearance settings in a private journal under `~/.local/state/omarchy-custom/catch-the-rainbow/installations/`. Keep that journal if you want to restore later.

## Scope

This is a desktop customization bundle: it installs custom shell components and app providers, and adds managed cursor/prompt initialization. Existing bar positions, widget settings, idle settings, unrelated plugins, monitor rules and keybindings are preserved. Optional personal third-party plugins are not installed by this bundle.

The full installer makes the local Catch the Rainbow theme a personally managed theme. If the standard theme was installed as a Git checkout, its `.git` metadata is preserved in the backup and removed from the active theme so Omarchy can load the full theme's explicitly requested Lua/terminal configuration. Restoring the bundle restores that checkout. Update the full setup using a reviewed bundle release.

Switching to another theme changes theme-scoped colors, GTK/Zen styling, weather rain and cursor selection. Custom shell components and the prompt remain installed until you use the full restore command.

The optional components are tied to the tested Omarchy shell API. They are not promised to work across every Omarchy update. The installer refuses an untested Omarchy package version; see the bundle's validation notes for what was actually checked.
