# DSpico Toolbox

Tool desktop (Windows / macOS / Linux) che guida passo passo tutte le
procedure per una DSpico: flashing del firmware, aggiornamento dei
componenti, installazione emulatori, cover, temi e supporto DSiWare.

## Tab

- **Setup** — Rileva la DSpico collegata al PC in modalità bootloader
  RP2040 (drive `RPI-RP2`) e flasha l'ultimo firmware **ibrido**
  mantenuto dalla community (`coderkei/dspico-hybrid-fw`). Non
  distribuiamo il firmware WRFUxxed del LNH Team: per quello segui la
  guida ufficiale. Link diretti alle guide DSi/3DS per chi ha bisogno
  della mod software.
- **Install and Update** — Aggiorna Pico Loader e Pico Launcher
  dell'LNH Team, con backup automatico dei file precedenti.
- **Setup Emulators** — Catalogo di 14 emulatori per Pico-Launcher
  (GBA, GB/C, SNES, NES, Atari 2600/5200/7800/800, Genesis, Master
  System/Game Gear, NeoGeo Pocket, PC-Engine, ColecoVision,
  IntelliVision). Un click scarica il file giusto, crea le cartelle
  ROM/dati necessarie e aggiorna `_pico/settings.json` per farli
  lanciare al volo da Pico-Launcher. Le eventuali BIOS non sono
  incluse (copyright): vanno procurate autonomamente.
- **Covers** — Apre PicoCover (strumento di terze parti, non
  affiliato) per generare le cover dei giochi.
- **Themes** — Apre l'archivio temi ufficiale e installa Pico Theme
  Switcher, un homebrew per cambiare tema direttamente dalla console.
- **DSi** — Prepara la SD per DSiWare/ROM cifrate scaricando
  `pico_file_dump.nds`; il dump di BIOS/NAND va completato sulla
  console (solo su DSi/3DS).

## Avvio rapido (da sorgente)

```bash
python3 -m venv venv
source venv/bin/activate        # su Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Richiede Python 3.10+.

## Creare un eseguibile/installer

Il modo più semplice per ottenere un `.exe` (Windows), un `.app` (macOS) o
un binario Linux è [PyInstaller](https://pyinstaller.org/), da eseguire
**sul sistema operativo di destinazione** (PyInstaller non fa cross-compile)

Per creare un eseguibile, sarà a priori necessario clonare la repository,
si può fare tranquillamente con [Git](https://git-scm.com/) via terminale:
```bash
git clone "https://github.com/Nogamiux/PicoToolBox"
```

Successivamente, aprire un terminale nella cartella della repository appena clonata ed eseguire i seguenti comandi:

```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "DSpico Toolbox" ^
    --add-data "assets/fonts/PressStart2P-Regular.ttf;assets/fonts" main.py
```

(su macOS/Linux sostituisci il `;` con `:` nel parametro `--add-data`, in alcune distro potrebbe essere necessario)

L'eseguibile finale si trova in `dist/DSpico Toolbox/`. Per un vero
pacchetto installabile:

- **Windows**: impacchetta la cartella `dist/` con
  [Inno Setup](https://jrsoftware.org/isinfo.php).
- **macOS**: usa `--windowed` (già incluso sopra) per generare un `.app`.
- **Linux**: distribuisci il binario, oppure impacchettalo come
  AppImage con [python-appimage](https://github.com/niess/python-appimage).

## Note tecniche

- **Rilevamento SD**: si basa sulla presenza di `_picoboot.nds` e/o
  della cartella `_pico/` in root (come da layout ufficiale Pico-Launcher).
- **Rilevamento bootloader RP2040**: si basa sulla presenza del file
  `INFO_UF2.TXT`, che ogni chip RP2040 (quindi anche la DSpico) espone
  in root quando è collegato in modalità bootloader.
- **Firmware distribuito**: solo l'asset `.uf2` con "hybrid" nel nome
  dell'ultima release di `coderkei/dspico-hybrid-fw`; le altre varianti
  della release (WRFUxxed senza binario, Devkit/Panda) vengono ignorate
  di proposito.
- **Versioni installate**: i file binari di Pico Loader/Launcher non
  contengono un numero di versione leggibile dall'esterno. Il tool
  tiene traccia di cosa ha installato lui stesso in
  `_pico/.dspico_updater_state.json`.

## Struttura del progetto

```
main.py                       punto d'ingresso, carica il font pixel
assets/fonts/                  font Press Start 2P per titoli/tab
core/
  drives.py                    rilevamento SD e file installati
  firmware.py                   rilevamento bootloader RP2040 + flash firmware
  github_api.py                  client per le release GitHub
  updater.py                      download/installazione Pico Loader/Launcher
  emulators.py                     catalogo emulatori + installer generico
  themes.py                         installer Pico Theme Switcher
  dsi.py                              preparazione SD per DSiWare
  links.py                             URL esterni centralizzati
  cheats.py                             gestione usrcheat.dat (non wired in UI)
  state.py                               versioni componenti installati
ui/
  main_window.py                finestra principale (tab + selettore SD)
  workers.py                     thread in background per rete/IO
  theme.py                        palette e QSS "quadrettato"
  widgets.py                       widget condivisi tra le tab
  tabs/
    setup_tab.py                   flash firmware
    install_update_tab.py           aggiornamento Pico Loader/Launcher
    emulators_tab.py                 installazione emulatori
    covers_tab.py                     apertura PicoCover
    themes_tab.py                      temi + theme switcher
    dsi_tab.py                          supporto DSiWare
```
