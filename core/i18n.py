              

LANGUAGES = {
    "it": {
        "app_title": "DSPico Toolbox",
        "app_subtitle": "Un Tool All-in-one per la tua scheda DSPico",
        "tab_setup": "Setup",
        "tab_install": "Installa / Aggiorna",
        "tab_emulators": "Emulatori",
        "tab_covers": "Copertine",
        "tab_themes": "Temi",
        "tab_dsi": "DSi",
        "tab_extra": "Extra & Salvataggi",
        "tab_credits": "Credits",
        "select_drive": "Seleziona prima un'unità dall'elenco in alto.",
        "sd_label": "Scheda SD:",
        "rescan_btn": "Rileva di nuovo",
        "status_scanning": "Cerco unità collegate...",
        "status_error_drive": "Errore rilevamento unità: {msg}",
        "status_no_drive": "Nessuna unità esterna rilevata. Collega la SD e riprova.",
        "status_found_drives": "Trovate {count} unità. ",
        "status_dspico_ok": "Scheda DSPico riconosciuta.",
        "status_dspico_no": "Nessuna delle unità sembra una scheda DSPico valida.",
        "status_ready": "Pronto.",
        "drive_none": "Nessuna unità trovata",
        "hw_searching": "Ricerco...",

                                
        "init_title": "Inizializza SD",
        "init_text": (
            "Stai per inizializzare l'unità \"{label}\" per l'uso con DSPico.\n\n"
            "Vuoi anche FORMATTARE l'unità in FAT32 cancellando tutti i dati?\n\n"
            "💡 Consigliamo di formattare SOLO se è la prima volta che usi questa MicroSD "
            "con la DSPico o se riscontri problemi di lettura con la cartuccia."
        ),
        "btn_format": "Formatta e Inizializza",
        "btn_no_format": "Inizializza senza formattare",
        "btn_cancel": "Annulla",

                    
        "ak_title": "AkMenuNext",
        "ak_text": (
            "Stai per installare AkMenuNext su \"{label}\".\n\n"
            "Verranno scaricati:\n"
            "  • akmenu-next-pico.zip → root della SD\n"
            "  • Pico_Loader_DSPICO.zip → _pico/\n\n"
            "Vuoi anche FORMATTARE l'unità in FAT32 cancellando tutti i dati prima di procedere?\n\n"
            "💡 Consigliamo di formattare SOLO se è la prima volta che usi questa MicroSD "
            "con la DSPico o se riscontri problemi di lettura con la cartuccia."
        ),
        "btn_ak_format": "Formatta e Installa",
        "btn_ak_nofmt": "Installa senza formattare",
        "ak_desc": (
            "Installa AkMenuNext come menu alternativo per la tua DSPico.\n"
            "Verrà scaricato l'archivio nella root della SD e Pico Loader "
            "verrà copiato nella cartella _pico/."
        ),
        "ak_install_btn": "Installa AkMenuNext",
        "ak_installing": "Installazione AkMenuNext in corso...",
        "ak_fmt_installing": "Formattazione e installazione AkMenuNext in corso...",

                       
        "nds_title": "nds-bootstrap",
        "nds_q": (
            "Vuoi installare anche nds-bootstrap come loader aggiuntivo?\n\n"
            "Verrà scaricato e copiato nella cartella _nds/ della SD."
        ),
        "nds_ok": "AkMenuNext e nds-bootstrap installati con successo!",

                        
        "twl_title": "TWiLightMenu++",
        "twl_text": (
            "Stai per installare TWiLightMenu++ su \"{label}\".\n\n"
            "Vuoi FORMATTARE l'unità in FAT32 prima di procedere?\n\n"
            "💡 ATTENZIONE: Se scegli di formattare, TWiLightMenu++ verrà impostato "
            "automaticamente come kernel primario (autoboot) e cancellerà tutti i dati preesistenti!"
        ),
        "twl_kernel_q": "Kernel Primario",
        "twl_kernel_text": (
            "Vuoi impostare TWiLightMenu++ come kernel primario?\n\n"
            "Scegli 'Sì' se vuoi che si avvii automaticamente come menu principale "
            "(verrà sovrascritto il file di boot)."
        ),
        "twl_desc": (
            "Installa TWiLightMenu++ come menu alternativo per la tua DSPico.\n"
            "Verranno scaricati e copiati i file necessari (_nds, roms, BOOT_ALT.NDS)."
        ),
        "twl_install_btn": "Installa TWiLightMenu++",
        "twl_installing": "Installazione TWiLightMenu++ in corso...",
        "twl_fmt_installing": "Formattazione e installazione TWiLightMenu++ in corso...",

                          
        "backup_title": "Backup Salvataggi",
        "backup_file_dlg": "Salva Backup Salvataggi",
        "backup_done": "Backup completato: {count} salvataggi archiviati.",
        "backup_btn": "Fai Backup (.zip)",
        "backup_in_progress": "Backup dei salvataggi in corso...",
        "restore_title": "Ripristino Salvataggi",
        "restore_btn": "Ripristina (.zip)",
        "restore_q": (
            "Usi TWiLightMenu++ come menu principale per avviare i giochi?\n\n"
            "Scegli 'Sì' per estrarre i salvataggi nella sottocartella 'saves' (stile TWL).\n"
            "Scegli 'No' per metterli nella stessa cartella della ROM (stile AkMenu/Pico)."
        ),
        "restore_done": (
            "Ripristino completato!\nSalvataggi accoppiati alle ROM: {restored}\n"
            "Salvataggi non ripristinati (messi in 'no-restore-saves'): {orphaned}"
        ),
        "restore_in_progress": "Ripristino dei salvataggi in corso...",
        "saves_title": "Backup & Ripristino Salvataggi",
        "saves_desc": (
            "Esegui il backup di tutti i file .sav della SD in un archivio ZIP sul tuo PC. "
            "Al ripristino, il tool troverà automaticamente le ROM corrispondenti e "
            "posizionerà i salvataggi correttamente."
        ),
        "extra_subtitle": "Installa menu alternativi, loader aggiuntivi e gestisci i tuoi salvataggi.",

                              
        "install_subtitle": "Installa o aggiorna i componenti firmware della tua DSPico.",
        "install_init_desc": (
            "Prepara una nuova MicroSD per l'uso con DSPico: scarica e installa "
            "automaticamente Pico Loader e Pico Launcher."
        ),
        "install_check_btn": "Controlla aggiornamenti",
        "install_checking": "Controllo aggiornamenti in corso...",
        "install_check_done": "Controllo completato.",
        "install_check_error": "Errore durante il controllo: {msg}",
        "install_check_first": "Controlla prima",
        "install_check_first_msg": "Esegui prima il controllo aggiornamenti.",
        "install_no_sd": "Nessuna SD DSPico selezionata.",
        "install_unknown": "Sconosciuta",
        "install_up_to_date": "Aggiornato",
        "install_update_available": "Aggiornamento disponibile",
        "install_version": "Versione installata: {ver}",
        "install_version_ok": "Versione: {ver} (aggiornato al {date})",
        "install_version_diff": "Installata: {ver}  •  Disponibile: {latest}",
        "install_btn_update": "Aggiorna",
        "install_in_progress": "Installazione {kind} in corso...",
        "install_failed_msg": "Installazione fallita: {msg}",
        "install_select_sd": "Seleziona una scheda DSPico valida prima di procedere.",
        "install_fmt_progress": "Formattazione e inizializzazione di {label} in corso...",
        "install_nofmt_progress": "Inizializzazione di {label} in corso...",
        "install_sd_ok": "SD inizializzata con successo.",
        "install_sd_ok_text": "SD pronta!\n\nLoader: {loader}\nLauncher: {launcher}",
        "install_sd_fail": "Errore inizializzazione SD: {msg}",
        "install_sd_fail_msg": "Impossibile inizializzare la SD:\n{msg}",

                   
        "setup_instructions": (
            "Collega la tua DSPico al PC tramite USB tenendo premuto il tasto BOOTSEL, "
            "poi clicca 'Rileva DSPico' per individuarla e flashare il firmware.\n\n"
            "Consulta le guide per preparare il CFW del DSi o gli hack per 3DS."
        ),
        "btn_dsi_guide": "Guida CFW DSi",
        "btn_3ds_guide": "Hack 3DS",
        "btn_fw_guide": "Guida Firmware",
        "setup_flash_title": "Flash Firmware DSPico",
        "btn_scan_dspico": "Rileva DSPico",
        "btn_flash_fw": "Flasha Firmware",
        "setup_detect_default": "Nessun dispositivo DSPico in modalità BOOTSEL rilevato.",
        "setup_scanning": "Ricerca dispositivo in corso...",
        "setup_found": "DSPico trovata in modalità BOOTSEL su {mp}. Pronta per il flash.",
        "setup_scan_error": "Errore durante la ricerca: {msg}",
        "setup_flash_ok": "Firmware {tag} installato con successo!",
        "setup_flash_done_title": "Flash completato",
        "setup_flash_done_text": "Il firmware {tag} è stato installato correttamente.\nLa DSPico si riavvierà automaticamente.",
        "setup_flash_error": "Errore durante il flash: {msg}",
        "setup_flash_err_title": "Errore Flash",

                 
        "dsi_instructions": (
            "Prepara la tua MicroSD per eseguire titoli DSiWare tramite DSPico.\n\n"
            "Verranno creati i file e le cartelle necessarie per avviare il menu DSi. "
            "Consulta la guida completa per i dettagli su come procedere."
        ),
        "btn_dsi_guide_full": "Guida DSiWare",
        "btn_prepare_dsi": "Prepara SD per DSi",
        "dsi_select_sd": "Seleziona prima una scheda DSPico valida.",
        "dsi_preparing": "Preparazione SD per DSi in corso...",
        "dsi_done": "SD preparata per DSi con successo!",
        "dsi_failed": "Preparazione fallita. Controlla il log per i dettagli.",

                       
        "emu_subtitle": "Installa emulatori homebrew direttamente sulla tua MicroSD DSPico.",
        "btn_emu_guide": "Guida Emulatori",
        "btn_emu_install": "Installa",
        "emu_select_sd": "Seleziona prima una scheda DSPico valida.",
        "emu_installing": "Installazione in corso...",
        "emu_installed": "Installati {count} file.",
        "emu_failed": "Installazione fallita.",
        "emu_failed_msg": "Errore durante l'installazione di {name}:\n{msg}",

                    
        "covers_text": (
            "Scarica e installa copertine per i tuoi giochi tramite PicoCover, "
            "il tool ufficiale per la gestione delle copertine su DSPico."
        ),
        "btn_open_picocover": "Apri sito Copertine",
        "covers_choose_title": "Scegli il sito per le copertine",
        "covers_choose_text": (
            "Per quale launcher vuoi cercare le copertine?"
        ),
        "covers_btn_picolauncher": "Pico Launcher",
        "covers_btn_twl": "TWiLightMenu++",
        "covers_disclaimer_title": "Link esterno",
        "covers_disclaimer_picocover": (
            "Stai per aprire PicoCover nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),
        "covers_disclaimer_twl": (
            "Stai per aprire TwilightBoxart nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),
        "covers_disclaimer": (
            "Stai per aprire PicoCover nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),

                    
        "themes_archive_text": (
            "Sfoglia l'archivio ufficiale dei temi per TWiLightMenu++ e AkMenuNext. "
            "Scarica il tema che preferisci e copialo nella cartella apposita sulla SD."
        ),
        "btn_themes_archive": "Apri Archivio Temi",
        "themes_choose_title": "Scegli l'archivio temi",
        "themes_choose_text": "Per quale launcher vuoi cercare i temi?",
        "themes_btn_picolauncher": "Pico Launcher",
        "themes_btn_twl": "TWiLightMenu++",
        "themes_btn_akmenu": "AkMenuNext",
        "themes_disclaimer_title": "Link esterno",
        "themes_disclaimer_pico": (
            "Stai per aprire l'archivio temi per Pico Launcher nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),
        "themes_disclaimer_twl": (
            "Stai per aprire Twilight Skin nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),
        "themes_disclaimer_ak": (
            "Stai per aprire l'archivio temi AkMenu nel tuo browser.\n"
            "Si tratta di un sito esterno non gestito da questo tool."
        ),
        "themes_switcher_text": (
            "Installa Theme Switcher sulla tua DSPico per cambiare tema direttamente "
            "dal menu senza dover collegare la SD al PC.\n"
            "⚠️ Pico Theme Switcher funziona solo con Pico Launcher."
        ),
        "btn_themes_switcher": "Installa Theme Switcher",
        "themes_select_sd": "Seleziona prima una scheda DSPico valida.",
        "themes_installing": "Installazione Theme Switcher in corso...",
        "themes_installed": "Theme Switcher {tag} installato con successo!",
        "themes_failed": "Installazione fallita.",

                     
        "credits_intro": (
            "DSPico Toolbox è un progetto open source creato dalla community.\n"
            "Un ringraziamento speciale a tutti i dev che hanno reso possibile questo tool:"
        ),
        "credits_html": (
            "<b>LNH Team</b> — DSPico, Pico Loader, Pico Launcher<br>"
            "<b>Sanrax &amp; coderkei</b> — DSPico Hybrid FW, AkMenuNext<br>"
            "<b>RocketRobz &amp; DS-Homebrew</b> — TWiLightMenu++, nds-bootstrap<br>"
            "<b>Scaletta</b> — PicoCover<br>"
            "<b>Tutti i dev della scena homebrew DS e degli emulatori!</b>"
        ),
        "credits_outro": "Grazie per usare DSPico Toolbox. Buon divertimento! 🎮",

                         
        "bye_title": "Arrivederci!",
        "bye_text": (
            "Grazie per aver usato DSPico Toolbox!\n\n"
            "Un ringraziamento speciale ai dev che hanno reso possibile tutto questo:\n"
            "• LNH Team (DSPico, Pico Loader, Pico Launcher)\n"
            "• Sanrax e coderkei (DSPico Hybrid FW, AkMenuNext)\n"
            "• RocketRobz e DS-Homebrew (TWiLightMenu++, nds-bootstrap)\n"
            "• Scaletta (PicoCover)\n"
            "• Nogamiux (DSPico Toolbox, Pico Theme Switcher)\n"
            "• Tutti i dev della scena homebrew DS e degli emulatori!\n\n"
            "A presto e buon divertimento!"
        ),

                           
        "lang_switch_tooltip": "Cambia lingua / Switch language",
    },
    "en": {
        "app_title": "DSPico Toolbox",
        "app_subtitle": "An All-in-one Tool for your DSPico card",
        "tab_setup": "Setup",
        "tab_install": "Install / Update",
        "tab_emulators": "Emulators",
        "tab_covers": "Covers",
        "tab_themes": "Themes",
        "tab_dsi": "DSi",
        "tab_extra": "Extra & Saves",
        "tab_credits": "Credits",
        "select_drive": "Please select a drive from the list above first.",
        "sd_label": "SD Card:",
        "rescan_btn": "Rescan",
        "status_scanning": "Scanning for connected drives...",
        "status_error_drive": "Drive detection error: {msg}",
        "status_no_drive": "No external drive detected. Plug in the SD and try again.",
        "status_found_drives": "Found {count} drive(s). ",
        "status_dspico_ok": "DSPico card recognised.",
        "status_dspico_no": "None of the drives looks like a valid DSPico card.",
        "status_ready": "Ready.",
        "drive_none": "No drive found",
        "hw_searching": "Searching...",

                                
        "init_title": "Initialize SD",
        "init_text": (
            "You are about to initialize drive \"{label}\" for use with DSPico.\n\n"
            "Do you also want to FORMAT the drive to FAT32, erasing all data?\n\n"
            "💡 We recommend formatting ONLY if this is the first time you use this MicroSD "
            "with DSPico or if you are experiencing cartridge read issues."
        ),
        "btn_format": "Format and Initialize",
        "btn_no_format": "Initialize without formatting",
        "btn_cancel": "Cancel",

                    
        "ak_title": "AkMenuNext",
        "ak_text": (
            "You are about to install AkMenuNext on \"{label}\".\n\n"
            "The following will be downloaded:\n"
            "  • akmenu-next-pico.zip → SD root\n"
            "  • Pico_Loader_DSPICO.zip → _pico/\n\n"
            "Do you also want to FORMAT the drive to FAT32, erasing all data before proceeding?\n\n"
            "💡 We recommend formatting ONLY if this is the first time you use this MicroSD "
            "with DSPico or if you are experiencing cartridge read issues."
        ),
        "btn_ak_format": "Format and Install",
        "btn_ak_nofmt": "Install without formatting",
        "ak_desc": (
            "Install AkMenuNext as an alternative menu for your DSPico.\n"
            "The archive will be downloaded to the SD root and Pico Loader "
            "will be copied to the _pico/ folder."
        ),
        "ak_install_btn": "Install AkMenuNext",
        "ak_installing": "Installing AkMenuNext...",
        "ak_fmt_installing": "Formatting and installing AkMenuNext...",

                       
        "nds_title": "nds-bootstrap",
        "nds_q": (
            "Do you also want to install nds-bootstrap as an additional loader?\n\n"
            "It will be downloaded and copied to the _nds/ folder on the SD."
        ),
        "nds_ok": "AkMenuNext and nds-bootstrap installed successfully!",

                        
        "twl_title": "TWiLightMenu++",
        "twl_text": (
            "You are about to install TWiLightMenu++ on \"{label}\".\n\n"
            "Do you want to FORMAT the drive to FAT32 before proceeding?\n\n"
            "💡 WARNING: If you choose to format, TWiLightMenu++ will be automatically set "
            "as the primary kernel (autoboot) and all pre-existing data will be erased!"
        ),
        "twl_kernel_q": "Primary Kernel",
        "twl_kernel_text": (
            "Do you want to set TWiLightMenu++ as your primary kernel?\n\n"
            "Choose 'Yes' if you want it to boot automatically as the main menu "
            "(the boot file will be overwritten)."
        ),
        "twl_desc": (
            "Install TWiLightMenu++ as an alternative menu for your DSPico.\n"
            "The required files (_nds, roms, BOOT_ALT.NDS) will be downloaded and copied."
        ),
        "twl_install_btn": "Install TWiLightMenu++",
        "twl_installing": "Installing TWiLightMenu++...",
        "twl_fmt_installing": "Formatting and installing TWiLightMenu++...",

                          
        "backup_title": "Saves Backup",
        "backup_file_dlg": "Save Saves Backup",
        "backup_done": "Backup completed: {count} saves archived.",
        "backup_btn": "Backup (.zip)",
        "backup_in_progress": "Backing up saves...",
        "restore_title": "Saves Restore",
        "restore_btn": "Restore (.zip)",
        "restore_q": (
            "Do you use TWiLightMenu++ as your main menu to launch games?\n\n"
            "Choose 'Yes' to extract saves into the 'saves' subfolder (TWL style).\n"
            "Choose 'No' to put them in the same folder as the ROM (AkMenu/Pico style)."
        ),
        "restore_done": (
            "Restore completed!\nSaves matched to ROMs: {restored}\n"
            "Saves not restored (placed in 'no-restore-saves'): {orphaned}"
        ),
        "restore_in_progress": "Restoring saves...",
        "saves_title": "Backup & Restore Saves",
        "saves_desc": (
            "Back up all .sav files from the SD into a ZIP archive on your PC. "
            "On restore, the tool will automatically match ROMs and place saves correctly."
        ),
        "extra_subtitle": "Install alternative menus, extra loaders and manage your saves.",

                              
        "install_subtitle": "Install or update firmware components for your DSPico.",
        "install_init_desc": (
            "Prepare a new MicroSD for use with DSPico: automatically downloads and installs "
            "Pico Loader and Pico Launcher."
        ),
        "install_check_btn": "Check for updates",
        "install_checking": "Checking for updates...",
        "install_check_done": "Check completed.",
        "install_check_error": "Error during check: {msg}",
        "install_check_first": "Check first",
        "install_check_first_msg": "Please run the update check first.",
        "install_no_sd": "No DSPico SD selected.",
        "install_unknown": "Unknown",
        "install_up_to_date": "Up to date",
        "install_update_available": "Update available",
        "install_version": "Installed version: {ver}",
        "install_version_ok": "Version: {ver} (up to date as of {date})",
        "install_version_diff": "Installed: {ver}  •  Available: {latest}",
        "install_btn_update": "Update",
        "install_in_progress": "Installing {kind}...",
        "install_failed_msg": "Installation failed: {msg}",
        "install_select_sd": "Please select a valid DSPico card before proceeding.",
        "install_fmt_progress": "Formatting and initializing {label}...",
        "install_nofmt_progress": "Initializing {label}...",
        "install_sd_ok": "SD initialized successfully.",
        "install_sd_ok_text": "SD ready!\n\nLoader: {loader}\nLauncher: {launcher}",
        "install_sd_fail": "SD initialization error: {msg}",
        "install_sd_fail_msg": "Could not initialize the SD:\n{msg}",

                   
        "setup_instructions": (
            "Connect your DSPico to the PC via USB while holding the BOOTSEL button, "
            "then click 'Detect DSPico' to find it and flash the firmware.\n\n"
            "Check the guides to prepare DSi CFW or 3DS hacks."
        ),
        "btn_dsi_guide": "DSi CFW Guide",
        "btn_3ds_guide": "3DS Hacks",
        "btn_fw_guide": "Firmware Guide",
        "setup_flash_title": "Flash DSPico Firmware",
        "btn_scan_dspico": "Detect DSPico",
        "btn_flash_fw": "Flash Firmware",
        "setup_detect_default": "No DSPico device in BOOTSEL mode detected.",
        "setup_scanning": "Searching for device...",
        "setup_found": "DSPico found in BOOTSEL mode at {mp}. Ready to flash.",
        "setup_scan_error": "Error during detection: {msg}",
        "setup_flash_ok": "Firmware {tag} installed successfully!",
        "setup_flash_done_title": "Flash complete",
        "setup_flash_done_text": "Firmware {tag} was installed correctly.\nThe DSPico will reboot automatically.",
        "setup_flash_error": "Error during flash: {msg}",
        "setup_flash_err_title": "Flash Error",

                 
        "dsi_instructions": (
            "Prepare your MicroSD to run DSiWare titles via DSPico.\n\n"
            "The necessary files and folders for the DSi menu will be created. "
            "Check the full guide for details on how to proceed."
        ),
        "btn_dsi_guide_full": "DSiWare Guide",
        "btn_prepare_dsi": "Prepare SD for DSi",
        "dsi_select_sd": "Please select a valid DSPico card first.",
        "dsi_preparing": "Preparing SD for DSi...",
        "dsi_done": "SD prepared for DSi successfully!",
        "dsi_failed": "Preparation failed. Check the log for details.",

                       
        "emu_subtitle": "Install homebrew emulators directly onto your DSPico MicroSD.",
        "btn_emu_guide": "Emulators Guide",
        "btn_emu_install": "Install",
        "emu_select_sd": "Please select a valid DSPico card first.",
        "emu_installing": "Installing...",
        "emu_installed": "{count} file(s) installed.",
        "emu_failed": "Installation failed.",
        "emu_failed_msg": "Error installing {name}:\n{msg}",

                    
        "covers_text": (
            "Download and install covers for your games using PicoCover, "
            "the official tool for managing covers on DSPico."
        ),
        "btn_open_picocover": "Open Covers Site",
        "covers_choose_title": "Choose covers site",
        "covers_choose_text": (
            "Which launcher do you want to find covers for?"
        ),
        "covers_btn_picolauncher": "Pico Launcher",
        "covers_btn_twl": "TWiLightMenu++",
        "covers_disclaimer_title": "External link",
        "covers_disclaimer_picocover": (
            "You are about to open PicoCover in your browser.\n"
            "This is an external site not managed by this tool."
        ),
        "covers_disclaimer_twl": (
            "You are about to open TwilightBoxart in your browser.\n"
            "This is an external site not managed by this tool."
        ),
        "covers_disclaimer": (
            "You are about to open PicoCover in your browser.\n"
            "This is an external site not managed by this tool."
        ),

                    
        "themes_archive_text": (
            "Browse the official theme archive for TWiLightMenu++ and AkMenuNext. "
            "Download your preferred theme and copy it to the appropriate folder on the SD."
        ),
        "btn_themes_archive": "Open Theme Archive",
        "themes_choose_title": "Choose theme archive",
        "themes_choose_text": "Which launcher do you want to find themes for?",
        "themes_btn_picolauncher": "Pico Launcher",
        "themes_btn_twl": "TWiLightMenu++",
        "themes_btn_akmenu": "AkMenuNext",
        "themes_disclaimer_title": "External link",
        "themes_disclaimer_pico": (
            "You are about to open the Pico Launcher theme archive in your browser.\n"
            "This is an external site not managed by this tool."
        ),
        "themes_disclaimer_twl": (
            "You are about to open Twilight Skin in your browser.\n"
            "This is an external site not managed by this tool."
        ),
        "themes_disclaimer_ak": (
            "You are about to open the AkMenu theme archive in your browser.\n"
            "This is an external site not managed by this tool."
        ),
        "themes_switcher_text": (
            "Install Theme Switcher on your DSPico to change themes directly "
            "from the menu without having to plug the SD into your PC.\n"
            "⚠️ Pico Theme Switcher works only with Pico Launcher."
        ),
        "btn_themes_switcher": "Install Theme Switcher",
        "themes_select_sd": "Please select a valid DSPico card first.",
        "themes_installing": "Installing Theme Switcher...",
        "themes_installed": "Theme Switcher {tag} installed successfully!",
        "themes_failed": "Installation failed.",

                     
        "credits_intro": (
            "DSPico Toolbox is an open source project created by the community.\n"
            "A special thanks to all the devs who made this tool possible:"
        ),
        "credits_html": (
            "<b>LNH Team</b> — DSPico, Pico Loader, Pico Launcher<br>"
            "<b>Sanrax &amp; coderkei</b> — DSPico Hybrid FW, AkMenuNext<br>"
            "<b>RocketRobz &amp; DS-Homebrew</b> — TWiLightMenu++, nds-bootstrap<br>"
            "<b>Scaletta</b> — PicoCover<br>"
            "<b>All DS homebrew and emulator developers!</b>"
        ),
        "credits_outro": "Thanks for using DSPico Toolbox. Have fun! 🎮",

                         
        "bye_title": "Goodbye!",
        "bye_text": (
            "Thanks for using DSPico Toolbox!\n\n"
            "A special thanks to the devs who made all of this possible:\n"
            "• LNH Team (DSPico, Pico Loader, Pico Launcher)\n"
            "• Sanrax & coderkei (DSPico Hybrid FW, AkMenuNext)\n"
            "• RocketRobz & DS-Homebrew (TWiLightMenu++, nds-bootstrap)\n"
            "• Scaletta (PicoCover)\n"
            "• Nogamiux (DSPico Toolbox, Pico Theme Switcher)\n"
            "• All DS homebrew and emulator developers!\n\n"
            "See you soon and have fun!"
        ),

                           
        "lang_switch_tooltip": "Cambia lingua / Switch language",
    }
}

current_lang = "it"


def set_lang(lang_code: str):
    global current_lang
    if lang_code in LANGUAGES:
        current_lang = lang_code


def t(key: str, **kwargs) -> str:
    lang_dict = LANGUAGES.get(current_lang, LANGUAGES["it"])
    text = lang_dict.get(key, LANGUAGES["it"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

