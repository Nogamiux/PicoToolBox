# DSpico Toolbox

Per il README in italiano [Clicca qui](./READMEIT.md)

Desktop tool (Windows / Linux) that guides you step by step through all
procedures for a DSpico: firmware flashing, component updates,
emulator installation, covers, themes and DSiWare support.

<p>Hey you, if you're looking for the Linux build, you can find it in this <a href="https://github.com/Simo3ds/PicoToolBox">Repo</a> maintained by Simo3ds.</p>

<p>PicoToolBox is not affiliated with LNH Team, Flashcarts.net, or the guides written on Sanrax.<br>
It is a tool that makes use of these sources to simplify as much as possible the various configurations available for DSpico cartridges.<br>
To properly support these projects, please support the devs behind these 3 sources — without their work, this tool wouldn't even exist.</p>


## Tabs

- **Setup** — Detects the DSpico connected to the PC in RP2040 bootloader
  mode (`RPI-RP2` drive) and flashes the latest **hybrid** firmware
  maintained by the community (`coderkei/dspico-hybrid-fw`). We do not
  distribute the LNH Team's WRFUxxed firmware: for that, follow the
  official guide. Direct links to DSi/3DS guides for those who need the
  software mod. For the record, this feature only works for DSpico devices —
  it does not work in any way on R4, Ace3ds or similar devices.
  It also works on cartridges compatible with Pico-Launcher and Pico-Loader.
- **Install and Update** — Updates Pico Loader and Pico Launcher
  from the LNH Team, with automatic backup of previous files.
  Component updates have not been tested on flashcarts other than the DSpico.
  However, it should work on flashcarts compatible with Pico-Loader and Pico-Launcher.
  The SD initialization function formats and prepares the SD card for use with the DSpico.
  It will not work on other flashcarts — we may consider adding support for them in the future.
- **Setup Emulators** — Catalog of 14 emulators for Pico-Launcher
  (GBA, GB/C, SNES, NES, Atari 2600/5200/7800/800, Genesis, Master
  System/Game Gear, NeoGeo Pocket, PC-Engine, ColecoVision,
  IntelliVision). One click downloads the right file, creates the
  necessary ROM/data folders and updates `_pico/settings.json` to launch
  them directly from Pico-Launcher. BIOS files are not included
  (copyright): you need to source them yourself.
- **Covers** — Opens PicoCover (a third-party tool, not affiliated)
  to generate game covers. (Or TwilightBoxArt if you use TWL.)
- **Themes** — Opens the official theme archive and installs Pico Theme
  Switcher, a homebrew app to change themes directly from the console.
- **DSi** — Prepares the SD for DSiWare/encrypted ROMs by downloading
  `pico_file_dump.nds`; the BIOS/NAND dump must be completed on the
  console (DSi/3DS only).
  Important note: this feature is only available for the DSpico,
  as most traditional flashcarts — with few exceptions — do not run DSi software.
- **Extras** — Optionally, you can install other menus on the DSpico.
  This section allows you to install [AkMenuNext](https://github.com/coderkei/akmenu-next)
  or [TWiLight Menu++](https://github.com/DS-Homebrew/TWiLightMenu).
  It also allows you to backup and restore your save files.

## Quick start (from source)

```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+.

## Creating an executable/installer

The easiest way to get a `.exe` (Windows), `.app` (macOS) or a Linux
binary is [PyInstaller](https://pyinstaller.org/), which must be run
**on the target operating system** (PyInstaller does not cross-compile).

To create an executable, you will first need to clone the repository.
You can do so easily with [Git](https://git-scm.com/) via terminal:
```bash
git clone "https://github.com/Nogamiux/PicoToolBox"
```

Then open a terminal in the cloned repository folder and run the following commands:

```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "DSpico Toolbox" ^
    --add-data "assets/fonts/PressStart2P-Regular.ttf;assets/fonts" main.py
```

(on macOS/Linux replace `;` with `:` in the `--add-data` parameter; on some distros this may be required)

The final executable is located in `dist/DSpico Toolbox/`. For a proper
installable package:

- **Windows**: package the `dist/` folder with
  [Inno Setup](https://jrsoftware.org/isinfo.php).
- **Linux**: distribute the binary, or package it as an
  AppImage with [python-appimage](https://github.com/niess/python-appimage).

## Technical notes

- **SD detection**: based on the presence of `_picoboot.nds` and/or
  the `_pico/` folder in root (as per the official Pico-Launcher layout).
- **RP2040 bootloader detection**: based on the presence of the
  `INFO_UF2.TXT` file, which every RP2040 chip (including the DSpico) exposes
  in root when connected in bootloader mode.
- **Distributed firmware**: only the `.uf2` asset with "hybrid" in the name
  from the latest release of `coderkei/dspico-hybrid-fw`; other variants
  in the release (WRFUxxed without binary, Devkit/Panda) are intentionally ignored.
- **Installed versions**: Pico Loader/Launcher binaries do not contain a
  version number readable from the outside. The tool keeps track of what
  it has installed in `_pico/.dspico_updater_state.json`.

## Credits

<p><a href="https://sanrax.github.io/flashcart-guides/">Sanrax</a> For all the guides regarding DSpico and many other flashcarts.</p>
<p><a href="https://github.com/Simo3ds">Simo3ds</a> For the help provided with the Linux build.</p>
<p><a href="https://github.com/DefeatOf13">DefeatOf13</a> For testing the software on their own DSpico.</p>

## Project structure

```
main.py                       entry point, loads the pixel font
assets/fonts/                  Press Start 2P font for titles/tabs
core/
  drives.py                    SD detection and installed files
  firmware.py                   RP2040 bootloader detection + firmware flash
  github_api.py                  GitHub releases client
  updater.py                      Pico Loader/Launcher download and installation
  emulators.py                     emulator catalog + generic installer
  themes.py                         Pico Theme Switcher installer
  dsi.py                              SD preparation for DSiWare
  links.py                             centralised external URLs
  cheats.py                             usrcheat.dat management (unused for now)
  state.py                               installed component versions
  akmenu.py                               extras section with TWL and AkMenu
  i18n.py                                  Italian and English UI strings
  saves_manager.py                          save backup and restore
ui/
  main_window.py                main window (tabs + SD selector)
  workers.py                     background threads for network/IO
  theme.py                        palette and "pixel" QSS stylesheet
  widgets.py                       shared widgets across tabs
  tabs/
    setup_tab.py                   firmware flash
    install_update_tab.py           Pico Loader/Launcher update
    emulators_tab.py                 emulator installation
    covers_tab.py                     PicoCover launcher
    themes_tab.py                      themes + theme switcher
    dsi_tab.py                          DSiWare support
    extra_tab.py                         extra features
```
