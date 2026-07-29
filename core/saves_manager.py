import os
import zipfile
import shutil
import tempfile
from typing import Callable

def backup_saves(sd_root: str, zip_path: str, progress: Callable[[str], None] = None) -> int:
    count = 0
    if progress: progress("Scansione dei file .sav in corso...")
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(sd_root):
                                                                         
            if "/_pico/.backup" in root.replace('\\', '/') or "$RECYCLE.BIN" in root:
                continue
            for f in files:
                if f.lower().endswith('.sav'):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, sd_root)
                    zf.write(full_path, rel_path)
                    count += 1
    return count

def restore_saves(sd_root: str, zip_path: str, is_twl: bool, progress: Callable[[str], None] = None) -> tuple[int, int]:
                                                                
    rom_extensions = ('.nds', '.gba', '.gb', '.gbc', '.nes', '.sfc', '.smc', '.gen', '.md')
    rom_map = {}
    
    if progress: progress("Indicizzazione delle ROM presenti sulla SD...")
        
    for root, dirs, files in os.walk(sd_root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in rom_extensions:
                base = os.path.splitext(f)[0].lower()
                rom_map[base] = root

    restored = 0
    orphaned = 0
    
    with tempfile.TemporaryDirectory() as tmp:
        if progress: progress("Estrazione del backup in corso...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmp)
        
        if progress: progress("Ripristino intelligente dei salvataggi...")
            
        for root, dirs, files in os.walk(tmp):
            for f in files:
                if not f.lower().endswith('.sav'):
                    continue
                
                base = os.path.splitext(f)[0].lower()
                src_path = os.path.join(root, f)
                
                if base in rom_map:
                    rom_dir = rom_map[base]
                                   
                    if is_twl:
                        dest_dir = os.path.join(rom_dir, "saves")
                    else:
                        dest_dir = rom_dir
                        
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, f)
                    shutil.copy2(src_path, dest_path)
                    restored += 1
                else:
                                                                                            
                    dest_dir = os.path.join(sd_root, "Salvataggi_Orfani")
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, f)
                    shutil.copy2(src_path, dest_path)
                    orphaned += 1
                    
    return restored, orphaned