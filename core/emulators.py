from __future__ import annotations

import json
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass, field
from typing import Callable, Optional

import requests

ProgressCB = Optional[Callable[[str], None]]


class EmulatorInstallError(RuntimeError):
    pass


@dataclass
class EmulatorSpec:
    id: str
    name: str
    console: str
    download_url: str
    is_zip: bool = False
    main_nds_in_zip: Optional[str] = None
    dest_filename: Optional[str] = None
    dest_dir: str = "_pico/emulators"
    extra_files_from_zip: list[tuple[str, str]] = field(default_factory=list)
    rom_folders: list[str] = field(default_factory=list)
    extra_root_folders: list[str] = field(default_factory=list)
    file_associations: list[str] = field(default_factory=list)
    argv_compatible: bool = True
    bios_note: str = ""


CATALOG: list[EmulatorSpec] = [
    EmulatorSpec(
        id="gbarunner3",
        name="GBARunner3 (GBA)",
        console="Game Boy Advance",
        download_url="https://files.deletecat.com/GBARunner3-hicode.zip",
        is_zip=True,
        main_nds_in_zip="GBARunner3.nds",
        extra_files_from_zip=[("_gba", "_gba")],
        rom_folders=["ROMs/GBA"],
        file_associations=["gba"],
        bios_note="Richiede un dump BIOS GBA rinominato bios.bin, da mettere in /_gba/.",
    ),
    EmulatorSpec(
        id="gameyob",
        name="GameYob (GB/GBC)",
        console="Game Boy / Color",
        download_url="https://github.com/Stewmath/GameYob/releases/download/v0.5.2/gameyob.zip",
        is_zip=True,
        main_nds_in_zip="gameyob.nds",
        rom_folders=["ROMs/GB"],
        file_associations=["gb", "gbc"],
        bios_note="gbc_bios.bin opzionale in /ROMs/GB/ per la modalità colore.",
    ),
    EmulatorSpec(
        id="snemulds",
        name="SNEmulDS 0.6d (SNES, fork Coto)",
        console="Super Nintendo",
        download_url="https://sanrax.github.io/flashcart-guides/assets/SNEmulDS-0.6d-NTR-TGDS1.65.zip",
        is_zip=True,
        main_nds_in_zip="SNEmulDS.nds",
        dest_dir="Emulators",
        extra_files_from_zip=[("snemul.cfg", "snemul.cfg")],
        rom_folders=["ROMs/SNES"],
        argv_compatible=False,
        bios_note="Compatibilità limitata: consulta la compatibility list SNEmulDS.",
    ),
    EmulatorSpec(
        id="nesds",
        name="NesDS (NES)",
        console="Nintendo Entertainment System",
        download_url="https://github.com/DS-Homebrew/NesDS/releases/latest/download/nesDS.nds",
        rom_folders=["ROMs/NES"],
        file_associations=["nes"],
    ),
    EmulatorSpec(
        id="stellads",
        name="StellaDS (Atari 2600)",
        console="Atari 2600",
        download_url="https://github.com/wavemotion-dave/StellaDS/releases/latest/download/StellaDS.nds",
        rom_folders=["ROMs/2600"],
        file_associations=["a26"],
        bios_note="I ROM .bin vanno rinominati .a26.",
    ),
    EmulatorSpec(
        id="a5200ds",
        name="A5200DS (Atari 5200)",
        console="Atari 5200",
        download_url="https://github.com/wavemotion-dave/A5200DS/releases/latest/download/A5200DS.nds",
        rom_folders=["ROMs/5200", "ROMs/BIOS"],
        file_associations=["a52"],
        bios_note="5200.rom opzionale in /ROMs/BIOS/ (altrimenti usa il BIOS open-source integrato).",
    ),
    EmulatorSpec(
        id="a7800ds",
        name="A7800DS (Atari 7800)",
        console="Atari 7800",
        download_url="https://github.com/wavemotion-dave/A7800DS/releases/latest/download/A7800DS.nds",
        rom_folders=["ROMs/7800", "ROMs/BIOS"],
        file_associations=["a78"],
        bios_note="highscore.rom opzionale in /ROMs/BIOS/ per salvare i punteggi. ROM NTSC consigliate.",
    ),
    EmulatorSpec(
        id="a8ds",
        name="A8DS (Atari 800/400)",
        console="Atari 800/400",
        download_url="https://github.com/wavemotion-dave/A8DS/releases/latest/download/A8DS.nds",
        rom_folders=["ROMs/800", "ROMs/BIOS"],
        file_associations=["car", "xex", "atr", "atx"],
        bios_note="BIOS ufficiali opzionali in /ROMs/BIOS/ (altrimenti usa il BIOS open-source Altirra).",
    ),
    EmulatorSpec(
        id="picodrivetwl",
        name="PicoDriveTWL (Genesis/MegaDrive)",
        console="Sega Genesis / Mega Drive",
        download_url="https://github.com/DS-Homebrew/PicoDriveTWL/releases/download/v2.0.2/PicoDriveTWL.nds",
        rom_folders=["ROMs/Genesis"],
        file_associations=["gen", "smd", "md"],
    ),
    EmulatorSpec(
        id="s8ds",
        name="S8DS (Master System / Game Gear)",
        console="Sega Master System / Game Gear",
        download_url="https://github.com/FluBBaOfWard/S8DS/releases/latest/download/S8DS.zip",
        is_zip=True,
        main_nds_in_zip="S8DS.nds",
        rom_folders=["ROMs/SMS", "ROMs/GG", "ROMs/BIOS"],
        extra_root_folders=["data/S8DS"],
        file_associations=["sms", "gg", "sg", "sc"],
        bios_note="BIOS opzionali in /ROMs/BIOS/, da abilitare nelle impostazioni dell'emulatore.",
    ),
    EmulatorSpec(
        id="ngpds",
        name="NGPDS (NeoGeo Pocket / Color)",
        console="NeoGeo Pocket",
        download_url="https://github.com/FluBBaOfWard/NGPDS/releases/latest/download/NGPDS.zip",
        is_zip=True,
        main_nds_in_zip="NGPDS.nds",
        rom_folders=["ROMs/NGPocket", "ROMs/BIOS"],
        extra_root_folders=["data/NGPDS"],
        file_associations=["ngp", "ngc"],
        bios_note="BIOS in /ROMs/BIOS/: ngp-color-bios.ngp e ngp-bnw-bios.ngp.",
    ),
    EmulatorSpec(
        id="nitrografx",
        name="NitroGrafx (PC-Engine/TurboGrafx-16)",
        console="PC-Engine / TurboGrafx-16",
        download_url="https://github.com/FluBBaOfWard/NitroGrafx/releases/download/v0.9.0/NitroGrafx0_9_0.zip",
        is_zip=True,
        main_nds_in_zip="NitroGrafx.nds",
        rom_folders=["ROMs/TurboGrafx"],
        extra_root_folders=["data/NitroGrafx"],
        file_associations=["pce", "iso", "cue"],
        bios_note="Un BIOS CD-ROM opzionale va in /ROMs/TurboGrafx/ per i giochi su CD.",
    ),
    EmulatorSpec(
        id="colecods",
        name="ColecoDS (ColecoVision e affini)",
        console="ColecoVision / MSX / SG-1000",
        download_url="https://github.com/wavemotion-dave/ColecoDS/releases/latest/download/ColecoDS.nds",
        rom_folders=["ROMs/Coleco", "ROMs/BIOS"],
        file_associations=["col", "cas", "com", "cv", "ddp", "dsk", "mtx", "msx", "m5", "pen", "pv", "pv1"],
        bios_note="coleco.rom in /ROMs/BIOS/ (più altre BIOS opzionali per l'hardware simile supportato).",
    ),
    EmulatorSpec(
        id="nintvds",
        name="NINTV-DS (IntelliVision)",
        console="IntelliVision",
        download_url="https://github.com/wavemotion-dave/NINTV-DS/releases/latest/download/NINTV-DS.nds",
        rom_folders=["ROMs/INTV", "ROMs/BIOS"],
        file_associations=["int"],
        bios_note="Richiede grom.bin ed exec.bin in /ROMs/BIOS/ (altri BIOS opzionali per compatibilità estesa).",
    ),
]

CATALOG_BY_ID = {spec.id: spec for spec in CATALOG}


def _sd_path(sd_root: str, relative: str) -> str:
    return os.path.join(sd_root, *relative.split("/"))


def _download(url: str, dest_path: str, progress: ProgressCB = None) -> None:
    if progress:
        progress(f"Scarico {os.path.basename(dest_path)}...")
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    f.write(chunk)


def _find_file_in_zip(extract_dir: str, filename: str) -> Optional[str]:
    target = filename.lower()
    for root, _dirs, files in os.walk(extract_dir):
        for f in files:
            if f.lower() == target:
                return os.path.join(root, f)
    return None


def _find_dir_in_zip(extract_dir: str, dirname: str) -> Optional[str]:
    target = dirname.lower()
    for root, dirs, _files in os.walk(extract_dir):
        for d in dirs:
            if d.lower() == target:
                return os.path.join(root, d)
    return None


def install_emulator(spec: EmulatorSpec, drive, progress: ProgressCB = None) -> list[str]:
    sd_root = drive.mountpoint
    dest_dir_abs = _sd_path(sd_root, spec.dest_dir)
    os.makedirs(dest_dir_abs, exist_ok=True)

    installed: list[str] = []
    final_name = spec.dest_filename

    with tempfile.TemporaryDirectory() as tmp:
        download_name = os.path.basename(spec.download_url.split("?")[0]) or f"{spec.id}.bin"
        dl_path = os.path.join(tmp, download_name)
        _download(spec.download_url, dl_path, progress)

        if spec.is_zip:
            extract_dir = os.path.join(tmp, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            if progress:
                progress("Estraggo l'archivio...")
            with zipfile.ZipFile(dl_path) as zf:
                zf.extractall(extract_dir)

            if not spec.main_nds_in_zip:
                raise EmulatorInstallError(f"Configurazione incompleta per {spec.name}.")
            nds_src = _find_file_in_zip(extract_dir, spec.main_nds_in_zip)
            if not nds_src:
                raise EmulatorInstallError(
                    f"Non ho trovato {spec.main_nds_in_zip} nello zip di {spec.name}."
                )
            final_name = final_name or os.path.basename(nds_src)
            dest_path = os.path.join(dest_dir_abs, final_name)
            shutil.copy2(nds_src, dest_path)
            installed.append(f"{spec.dest_dir}/{final_name}")

            for src_name, dest_rel in spec.extra_files_from_zip:
                src_file = _find_file_in_zip(extract_dir, src_name)
                dest_abs = _sd_path(sd_root, dest_rel)
                if src_file:
                    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                    shutil.copy2(src_file, dest_abs)
                    installed.append(dest_rel)
                    continue
                src_dir = _find_dir_in_zip(extract_dir, src_name)
                if src_dir:
                    if os.path.isdir(dest_abs):
                        shutil.rmtree(dest_abs)
                    shutil.copytree(src_dir, dest_abs)
                    installed.append(dest_rel + "/")
        else:
            final_name = final_name or download_name
            dest_path = os.path.join(dest_dir_abs, final_name)
            shutil.copy2(dl_path, dest_path)
            installed.append(f"{spec.dest_dir}/{final_name}")

    for folder in [*spec.rom_folders, *spec.extra_root_folders]:
        os.makedirs(_sd_path(sd_root, folder), exist_ok=True)

    if spec.file_associations:
        if progress:
            progress("Aggiorno le associazioni file in _pico/settings.json...")
        _merge_file_associations(drive.pico_folder, spec.file_associations, spec.dest_dir, final_name)

    if progress:
        progress(f"{spec.name} installato.")
    return installed


def _merge_file_associations(pico_folder: str, extensions: list[str], dest_dir: str, filename: str) -> None:
    settings_path = os.path.join(pico_folder, "settings.json")
    if not os.path.isfile(settings_path):
        raise EmulatorInstallError(
            "settings.json non trovato in _pico/. Avvia almeno una volta Pico-Launcher sulla "
            "console per generarlo, poi ripeti l'installazione dell'emulatore."
        )

    with open(settings_path, "r", encoding="utf-8") as f:
        try:
            settings = json.load(f)
        except json.JSONDecodeError as exc:
            raise EmulatorInstallError(f"settings.json non è un JSON valido: {exc}") from exc

    app_path = "/" + dest_dir + "/" + filename
    file_assoc = settings.setdefault("fileAssociations", {})
    for ext in extensions:
        file_assoc[ext] = {"appPath": app_path}

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)