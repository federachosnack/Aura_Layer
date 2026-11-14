"""
Translation system for Aura Layer.
Supports Italian and English languages.
"""

class Translations:
    """Manages translations for the application."""
    
    # Translation dictionaries
    TRANSLATIONS = {
        "it": {
            # Main application
            "app_name": "Aura Layer",
            "app_description": "Desktop character overlay application",
            
            # Tray menu
            "tray_open_launcher": "Apri Launcher",
            "tray_toggle_all": "Mostra/Nascondi Tutti",
            "tray_unlock_all": "Sblocca tutti i personaggi",
            "tray_quit": "Esci",
            
            # Launcher window
            "launcher_title": "Aura Layer - Launcher",
            "launcher_characters": "Personaggi",
            "launcher_settings": "Impostazioni",
            "page_settings_title": "Impostazioni",
            "launcher_add_character": "Aggiungi Personaggio",
            "launcher_no_characters": "Nessun personaggio disponibile",
            "launcher_create_first": "Crea il tuo primo personaggio",
            
            # Character settings
            "char_name": "Nome",
            "char_animation": "Animazione",
            "char_behavior": "Comportamento",
            "char_scale": "Scala",
            "char_fps": "FPS",
            "char_volume": "Volume",
            "char_audio": "Audio",
            "char_locked": "Bloccato",
            
            # Behaviors
            "behavior_static": "Statico",
            "behavior_free_walk": "Cammino Libero",
            "behavior_random_edge": "Sbircia dai bordi",
            "behavior_gravity": "Gravità",
            "behavior_desc_static": "Resta fermo nella posizione del desktop in cui lo trascini.",
            "behavior_desc_free_walk": "Passeggia autonomamente avanti e indietro sopra la barra delle applicazioni.",
            "behavior_desc_gravity": "Cade con la fisica verso il fondo dello schermo e compie piccoli rimbalzi elastici.",
            "behavior_desc_random_edge": "Resta nascosto e si affaccia a sorpresa dai bordi dello schermo per farti un saluto.",

            # Audio options & buttons
            "audio_play_on_startup": "Riproduci audio all'avvio",
            "btn_audio_preview": "Ascolta",
            "btn_audio_stop": "Ferma",
            "btn_audio_remove": "Rimuovi audio",
            "msg_all_unlocked": "Tutti i personaggi sono stati sbloccati.",
            
            # Buttons
            "btn_launch": "Avvia",
            "btn_stop": "Ferma",
            "btn_edit": "Modifica",
            "btn_delete": "Elimina",
            "btn_save": "Salva",
            "btn_cancel": "Annulla",
            "btn_remove_bg": "Rimuovi sfondo con AI",
            "btn_restore": "Ripristina originale",
            
            # Messages
            "msg_bg_success": "Sfondo rimosso con successo! L'animazione è stata aggiornata.",
            "msg_bg_restore": "Puoi ripristinare l'originale con il pulsante 'Ripristina originale'.",
            "msg_bg_error": "Impossibile rimuovere lo sfondo. Verifica che il file sia valido.",
            "msg_bg_gif_warning": "La rimozione dello sfondo con AI non supporta le GIF animate. L'operazione convertirà la GIF in un'immagine statica. Vuoi continuare?",
            "msg_completed": "Completato",
            "msg_error": "Errore",
            "msg_warning": "Attenzione",
            
            # Settings
            "settings_general": "Generali",
            "settings_language": "Lingua",
            "settings_start_minimized": "Avvio minimizzato",
            "settings_autostart": "Avvio automatico",
            "settings_minimize_to_tray": "Minimizza nella tray",
            "settings_fps_limit": "Limite FPS globale",
            
            # Global settings
            "global_language": "Lingua",
            "language_italian": "Italiano",
            "language_english": "English",

            # Launcher UI
            "launcher_title": "Aura Layer - Launcher",
            "launcher_settings_title": "Impostazioni dell'applicazione",
            "launcher_settings_desc": "Questa sezione è pronta per ospitare preferenze globali, avvio automatico e opzioni grafiche.",
            "launcher_coming_soon": "IN ARRIVO",
            "settings_packages_title": "Pacchetti e Libreria Personaggi",
            "settings_packages_desc": "Importa nuovi compagni desktop da pacchetti .aura o gestisci i file locali.",
            "import_aura_title": "Importa Compagno .aura",
            "import_aura_sub": "Aggiunge un personaggio preconfigurato con animazione, audio e parametri.",
            "launcher_startup_system": "Avvio e sistema",
            "launcher_appearance": "Aspetto",
            "launcher_behavior": "Comportamento overlay",
            "launcher_performance": "Prestazioni",

            # Buttons
            "btn_launch_desktop": "Avvia sul desktop",
            "btn_remove_desktop": "Rimuovi dal desktop",
            "btn_rename": "Rinomina",
            "btn_remove": "Rimuovi",
            "btn_choose": "Scegli",
            "btn_lock": "Blocca",
            "btn_add_pc": "Aggiungi da PC",

            # Settings labels
            "settings_close_behavior": "Comportamento alla chiusura:",
            "settings_minimize_tray": "Minimizza in tray",
            "settings_close_app": "Chiudi l'app",
            "settings_theme": "Tema:",
            "settings_grid_size": "Dimensione griglia:",
            "settings_fullscreen_pause": "Pausa automatica in giochi fullscreen",
            "settings_default_behavior": "Comportamento predefinito:",
            "settings_default_fps": "FPS predefinito:",
            "settings_global_fps": "Limite FPS globale:",

            # Messages
            "msg_no_backup": "Non esiste un backup dell'originale per questo personaggio.",
            "msg_backup_not_found": "Il file di backup non è stato trovato.",
            "msg_restore_confirm": "Vuoi ripristinare l'immagine originale?\n\nL'immagine senza sfondo verrà mantenuta.",
            "msg_language_restart": "Il cambio lingua richiede il riavvio dell'applicazione.",
            "msg_restart_question": "Vuoi riavviare ora?",

            # Navigation
            "nav_navigation": "NAVIGAZIONE",
            "nav_library": "Libreria",
            "nav_settings": "Impostazioni",

            # Branding
            "brand_name": "Aura Layer",
            "brand_tagline": "FEDERA PROJECT",
            "brand_library": "AURA LAYER LIBRARY",
            "brand_slogan": "Dai vita al tuo desktop",

            # Status
            "status_operational": "Launcher operativo",
            "status_version": "AURA LAYER • FEDERA PROJECT",
            "page_library_title": "Libreria",
            "page_library_subtitle": "Gestisci e avvia i personaggi del tuo desktop",
            "active_counter": "0 personaggi attivi",
            "library_title": "I tuoi personaggi",
            "library_count": "0 elementi",
            "empty_library": "La libreria è vuota",
            "no_character": "Nessun personaggio",
            "no_audio": "Nessun audio",

            # Details
            "details_eyebrow": "DETTAGLI",
            "details_not_selected": "NON SELEZIONATO",
            "details_behavior": "COMPORTAMENTO",
            "details_screen": "SCHERMO",
            "details_fps": "FPS",
            "details_size": "DIMENSIONE",
            "details_audio": "AUDIO",
            "details_volume": "VOLUME",

            # Settings sections
            "settings_grid_size": "Dimensione griglia:",
            "settings_overlay_behavior": "Comportamento overlay",
            "settings_hotkey": "Hotkey globale (mostra/nascondi):",
            "settings_default_behavior": "Comportamento predefinito:",
            "settings_default_fps": "FPS predefinito:",
            "settings_performance": "Prestazioni",
            "settings_global_fps": "Limite FPS globale (0 = nessun limite):",
            "settings_folder": "Cartella personaggi:",

            # Info
            "info_title": "Informazioni",
            "info_version": "Versione: 1.2.0",
            "info_project": "Aura Layer - Desktop Overlay",
            "info_credits": "Progettato per migliorare la tua esperienza desktop",

            # Empty states
            "empty_no_characters": "Nessun personaggio ancora",
            "empty_add_pc": "Clicca Aggiungi da PC per iniziare",
            "empty_add_first": "Aggiungi il primo personaggio",

            # Tab titles
            "tab_library": "Libreria",
            "tab_settings": "Impostazioni",

            # Page subtitles
            "page_settings_subtitle": "Personalizza il comportamento di Aura Layer",

            # Status
            "status_active": "Attivo sul desktop",
            "status_ready": "Pronto",

            # Sorting
            "sort_az": "Nome: A–Z",
            "sort_za": "Nome: Z–A",

            # Behaviors
            "behavior_static": "Statico",
            "behavior_random_edge": "Sbircia dai bordi",
            "behavior_free_walk": "Movimento libero",
            "behavior_gravity": "Gravità",

            # Grid sizes
            "grid_small": "Piccola",
            "grid_medium": "Media",
            "grid_large": "Grande",

            # Themes
            "theme_amber": "Ambra",
            "theme_blue": "Blu notte",
            "theme_purple": "Viola",

            # Buttons
            "btn_unlock": "Sblocca",
            "btn_open_folder": "Apri cartella",

            # Special values
            "no_limit": "Nessun limite",

            # Dialog messages
            "dialog_select_animation": "Seleziona animazione",
            "dialog_character_exists": "Personaggio già presente",
            "dialog_character_exists_desc": "Esiste già un personaggio con questo nome.",
            "dialog_import_failed": "Importazione non riuscita",
            "dialog_remove_character": "Rimuovi personaggio",
            "dialog_removal_failed": "Rimozione non riuscita",
            "dialog_rename_character": "Rinomina personaggio",
            "dialog_invalid_name": "Nome non valido",
            "dialog_name_used": "Nome già utilizzato",
            "dialog_name_used_desc": "Esiste già un personaggio con questo nome.",
            "dialog_rename_failed": "Rinomina non riuscita",
            "dialog_select_audio": "Seleziona file audio",
            "dialog_audio_copy_failed": "Impossibile copiare il file audio",
            "dialog_no_animation": "Nessun file di animazione trovato per questo personaggio.",
            "dialog_restore_failed": "Impossibile ripristinare l'originale",
            "dialog_restore_success": "Immagine originale ripristinata con successo!",
            "dialog_autostart_failed": "Impossibile configurare l'avvio automatico",
            "dialog_new_name": "Nuovo nome:",
            "dialog_invalid_folder_chars": "Il nome non può contenere separatori di cartella.",
            "dialog_remove_confirm": "Vuoi rimuovere definitivamente \"{name}\" dalla libreria?",
            "dialog_import_error": "Non è stato possibile aggiungere il personaggio.",
            "dialog_remove_error": "Non è stato possibile rimuovere il personaggio.",
            "dialog_rename_error": "Non è stato possibile rinominare il personaggio.",

            # Search
            "search_no_results": "Nessun risultato",
            "search_no_results_desc": "Non è stato trovato alcun personaggio per",
            "search_add_files": "Aggiungi un file GIF, PNG, WEBP o APNG per iniziare.",
            "search_results_count": "risultati su",

            # Status badges
            "status_active_desktop": "Attivo sul desktop",
            "status_ready": "Pronto",

            # Export/Import .aura
            "btn_export_aura": "Esporta .aura",
            "btn_import_aura": "Importa .aura",
            "export_title": "Esporta Personaggio",
            "export_content": "CONTENUTO",
            "export_animation": "Animazione",
            "export_audio": "Audio",
            "export_thumbnail": "Anteprima (auto)",
            "export_config": "CONFIGURAZIONE",
            "export_behavior": "Comportamento",
            "export_fps": "Frame Rate",
            "export_scale": "Dimensione",
            "export_volume": "Volume",
            "export_lock": "Stato blocco",
            "export_notes": "NOTE PERSONALIZZATE",
            "export_notes_hint": "Opzionale, visibile a chi importa",
            "export_size_estimate": "Dimensione stimata",
            "export_success": "Personaggio esportato con successo!",
            "export_failed": "Esportazione non riuscita",
            "import_title": "Importa Personaggio",
            "import_content_included": "CONTENUTO INCLUSO",
            "import_config_included": "CONFIGURAZIONE INCLUSA",
            "import_apply": "Applicare",
            "import_name": "NOME",
            "import_name_hint": "Puoi cambiare il nome prima di importare",
            "import_author_note": "Nota dell'autore",
            "import_created": "Creato il",
            "import_made_with": "Creato con Aura Layer",
            "import_success": "Personaggio importato con successo!",
            "import_failed": "Importazione .aura non riuscita",
            "import_invalid": "File .aura non valido",
            "import_invalid_desc": "Il file selezionato non è un pacchetto .aura valido.",
            "import_too_many_files": "L'archivio contiene troppi file (limite superato).",
            "import_uncompressed_size": "La dimensione dell'archivio decompresso supera il limite consentito.",
            "import_unsafe_path": "Percorso o nome del personaggio non valido o non sicuro.",
            "import_invalid_manifest": "Manifest del pacchetto .aura incompleto o non valido.",
            "import_anim_missing": "File di animazione non trovato o mancante nel pacchetto .aura.",
            "crash_critical_title": "Aura Layer - Errore Critico",
            "crash_critical_msg": "Si è verificato un errore imprevisto.\n\nI dettagli sono stati salvati in:\n{path}",
            "import_conflict_title": "Nome già esistente",
            "import_conflict_msg": "Esiste già un personaggio con il nome \"{name}\".\n\nVuoi sovrascrivere il personaggio esistente o rinominare?",
            "import_overwrite": "Sovrascrivi",
            "import_rename": "Rinomina in \"{name}\"",
            "import_select_file": "Seleziona file .aura",
            "import_deselect_hint": "Deseleziona per usare i valori predefiniti",
            "aura_filter": "Pacchetto Aura (*.aura)",

            # Multi-Monitor
            "screen_auto": "Automatico (Ricorda posizione)",
            "screen_primary": "Principale",
            "screen_secondary": "Secondario",
            "msg_screen_disconnected": "Uno schermo è stato scollegato. I personaggi sono stati riposizionati sul monitor principale.",

            # Context menu
            "ctx_play_audio": "Riproduci audio",
            "ctx_behavior": "Comportamento",
            "ctx_move_to_screen": "Sposta su Schermo",
            "ctx_lock": "Blocca sul desktop",
            "ctx_open_launcher": "Modifica nel Launcher",
            "ctx_remove_desktop": "Rimuovi dal desktop",
            "ctx_locked_notification_title": "Personaggio Bloccato",
            "ctx_locked_notification_msg": "\"{name}\" è ora trasparente ai clic.\nPuoi sbloccarlo dal Launcher.",

            # Extra UI labels & stats
            "details_ai_tools": "STRUMENTI GRAFICA & AI",
            "badge_active": "ATTIVO",
            "badge_ready": "PRONTO",
            "stats_active_single": "1 personaggio attivo",
            "stats_active_multi": "{active} personaggi attivi",
            "sidebar_active_single": "1 compagno attivo",
            "sidebar_active_multi": "{active} compagni attivi",
            "topbar_active_single": "1 attivo",
            "topbar_active_multi": "{active} attivi",
            "library_count_single": "1 elemento",
            "library_count_multi": "{total} elementi",
            "btn_processing": "Elaborazione in corso...",
            "screen_num": "Schermo {i}",
            "filter_animation_files": "File animazione (*.gif *.png *.webp *.apng)",
            "export_no_audio": "Nessun file audio associato",
            "export_thumb_auto": "Generata automaticamente (150x150)",
            "status_locked": "Bloccato",
            "status_unlocked": "Sbloccato",
        },
        "en": {
            # Main application
            "app_name": "Aura Layer",
            "app_description": "Desktop character overlay application",
            
            # Tray menu
            "tray_open_launcher": "Open Launcher",
            "tray_toggle_all": "Show/Hide All",
            "tray_unlock_all": "Unlock all characters",
            "tray_quit": "Quit",
            
            # Launcher window
            "launcher_title": "Aura Layer - Launcher",
            "launcher_characters": "Characters",
            "launcher_settings": "Settings",
            "page_settings_title": "Settings",
            "launcher_add_character": "Add Character",
            "launcher_no_characters": "No characters available",
            "launcher_create_first": "Create your first character",
            
            # Character settings
            "char_name": "Name",
            "char_animation": "Animation",
            "char_behavior": "Behavior",
            "char_scale": "Scale",
            "char_fps": "FPS",
            "char_volume": "Volume",
            "char_audio": "Audio",
            "char_locked": "Locked",
            
            # Behaviors
            "behavior_static": "Static",
            "behavior_free_walk": "Free Walk",
            "behavior_random_edge": "Peek from edges",
            "behavior_gravity": "Gravity",
            "behavior_desc_static": "Stays in the exact desktop position where you drag it.",
            "behavior_desc_free_walk": "Walks back and forth autonomously above the taskbar.",
            "behavior_desc_gravity": "Falls with physics to the bottom of the screen and gently bounces.",
            "behavior_desc_random_edge": "Stays hidden and peeks out from the screen edges as a surprise greeting.",

            # Audio options & buttons
            "audio_play_on_startup": "Play audio on startup",
            "btn_audio_preview": "Play",
            "btn_audio_stop": "Stop",
            "btn_audio_remove": "Remove audio",
            "msg_all_unlocked": "All characters have been unlocked.",
            
            # Buttons
            "btn_launch": "Launch",
            "btn_stop": "Stop",
            "btn_edit": "Edit",
            "btn_delete": "Delete",
            "btn_save": "Save",
            "btn_cancel": "Cancel",
            "btn_remove_bg": "Remove background with AI",
            "btn_restore": "Restore original",
            
            # Messages
            "msg_bg_success": "Background removed successfully! Animation has been updated.",
            "msg_bg_restore": "You can restore the original with the 'Restore original' button.",
            "msg_bg_error": "Unable to remove background. Verify that the file is valid.",
            "msg_bg_gif_warning": "AI background removal doesn't support animated GIFs. This operation will convert the GIF to a static image. Do you want to continue?",
            "msg_completed": "Completed",
            "msg_error": "Error",
            "msg_warning": "Warning",
            
            # Settings
            "settings_general": "General",
            "settings_language": "Language",
            "settings_start_minimized": "Start minimized",
            "settings_autostart": "Autostart",
            "settings_minimize_to_tray": "Minimize to tray",
            "settings_fps_limit": "Global FPS limit",
            
            # Global settings
            "global_language": "Language",
            "language_italian": "Italiano",
            "language_english": "English",

            # Launcher UI
            "launcher_title": "Aura Layer - Launcher",
            "launcher_settings_title": "Application Settings",
            "launcher_settings_desc": "This section is ready to host global preferences, autostart, and graphics options.",
            "launcher_coming_soon": "COMING SOON",
            "settings_packages_title": "Packages & Character Library",
            "settings_packages_desc": "Import new desktop companions from .aura packages or manage local files.",
            "import_aura_title": "Import .aura Companion",
            "import_aura_sub": "Adds a preconfigured character with animation, audio, and settings.",
            "launcher_startup_system": "Startup & System",
            "launcher_appearance": "Appearance",
            "launcher_behavior": "Overlay Behavior",
            "launcher_performance": "Performance",

            # Buttons
            "btn_launch_desktop": "Launch on desktop",
            "btn_remove_desktop": "Remove from desktop",
            "btn_rename": "Rename",
            "btn_remove": "Remove",
            "btn_choose": "Choose",
            "btn_lock": "Lock",
            "btn_add_pc": "Add from PC",

            # Settings labels
            "settings_close_behavior": "Close behavior:",
            "settings_minimize_tray": "Minimize to tray",
            "settings_close_app": "Close app",
            "settings_theme": "Theme:",
            "settings_grid_size": "Grid size:",
            "settings_fullscreen_pause": "Auto-pause in fullscreen games",
            "settings_default_behavior": "Default behavior:",
            "settings_default_fps": "Default FPS:",
            "settings_global_fps": "Global FPS limit:",

            # Messages
            "msg_no_backup": "No backup of the original exists for this character.",
            "msg_backup_not_found": "The backup file was not found.",
            "msg_restore_confirm": "Do you want to restore the original image?\n\nThe background-removed image will be kept.",
            "msg_language_restart": "Language change requires application restart.",
            "msg_restart_question": "Do you want to restart now?",

            # Navigation
            "nav_navigation": "NAVIGATION",
            "nav_library": "Library",
            "nav_settings": "Settings",

            # Branding
            "brand_name": "Aura Layer",
            "brand_tagline": "FEDERA PROJECT",
            "brand_library": "AURA LAYER LIBRARY",
            "brand_slogan": "Bring your desktop to life",

            # Status
            "status_operational": "Launcher operational",
            "status_version": "AURA LAYER • FEDERA PROJECT",
            "page_library_title": "Library",
            "page_library_subtitle": "Manage and launch your desktop characters",
            "active_counter": "0 active characters",
            "library_title": "Your characters",
            "library_count": "0 items",
            "empty_library": "The library is empty",
            "no_character": "No character",
            "no_audio": "No audio",

            # Details
            "details_eyebrow": "DETAILS",
            "details_not_selected": "NOT SELECTED",
            "details_behavior": "BEHAVIOR",
            "details_screen": "SCREEN",
            "details_fps": "FPS",
            "details_size": "SIZE",
            "details_audio": "AUDIO",
            "details_volume": "VOLUME",

            # Settings sections
            "settings_grid_size": "Grid size:",
            "settings_overlay_behavior": "Overlay behavior",
            "settings_hotkey": "Global hotkey (show/hide):",
            "settings_default_behavior": "Default behavior:",
            "settings_default_fps": "Default FPS:",
            "settings_performance": "Performance",
            "settings_global_fps": "Global FPS limit (0 = no limit):",
            "settings_folder": "Characters folder:",

            # Info
            "info_title": "Information",
            "info_version": "Version: 1.2.0",
            "info_project": "Aura Layer - Desktop Overlay",
            "info_credits": "Designed to enhance your desktop experience",

            # Empty states
            "empty_no_characters": "No characters yet",
            "empty_add_pc": "Click Add from PC to get started",
            "empty_add_first": "Add your first character",

            # Tab titles
            "tab_library": "Library",
            "tab_settings": "Settings",

            # Page subtitles
            "page_settings_subtitle": "Customize Aura Layer behavior",

            # Status
            "status_active": "Active on desktop",
            "status_ready": "Ready",

            # Sorting
            "sort_az": "Name: A–Z",
            "sort_za": "Name: Z–A",

            # Behaviors
            "behavior_static": "Static",
            "behavior_random_edge": "Peek from edges",
            "behavior_free_walk": "Free movement",
            "behavior_gravity": "Gravity",

            # Grid sizes
            "grid_small": "Small",
            "grid_medium": "Medium",
            "grid_large": "Large",

            # Themes
            "theme_amber": "Amber",
            "theme_blue": "Midnight blue",
            "theme_purple": "Purple",

            # Buttons
            "btn_unlock": "Unlock",
            "btn_open_folder": "Open folder",

            # Special values
            "no_limit": "No limit",

            # Dialog messages
            "dialog_select_animation": "Select animation",
            "dialog_character_exists": "Character already exists",
            "dialog_character_exists_desc": "A character with this name already exists.",
            "dialog_import_failed": "Import failed",
            "dialog_remove_character": "Remove character",
            "dialog_removal_failed": "Removal failed",
            "dialog_rename_character": "Rename character",
            "dialog_invalid_name": "Invalid name",
            "dialog_name_used": "Name already used",
            "dialog_name_used_desc": "A character with this name already exists.",
            "dialog_rename_failed": "Rename failed",
            "dialog_select_audio": "Select audio file",
            "dialog_audio_copy_failed": "Unable to copy audio file",
            "dialog_no_animation": "No animation file found for this character.",
            "dialog_restore_failed": "Unable to restore original",
            "dialog_restore_success": "Original image restored successfully!",
            "dialog_autostart_failed": "Unable to configure autostart",
            "dialog_new_name": "New name:",
            "dialog_invalid_folder_chars": "The name cannot contain folder separators.",
            "dialog_remove_confirm": "Do you want to permanently remove \"{name}\" from the library?",
            "dialog_import_error": "Unable to add character.",
            "dialog_remove_error": "Unable to remove character.",
            "dialog_rename_error": "Unable to rename character.",

            # Search
            "search_no_results": "No results",
            "search_no_results_desc": "No character found for",
            "search_add_files": "Add a GIF, PNG, WEBP or APNG file to get started.",
            "search_results_count": "results of",

            # Status badges
            "status_active_desktop": "Active on desktop",
            "status_ready": "Ready",

            # Export/Import .aura
            "btn_export_aura": "Export .aura",
            "btn_import_aura": "Import .aura",
            "export_title": "Export Character",
            "export_content": "CONTENT",
            "export_animation": "Animation",
            "export_audio": "Audio",
            "export_thumbnail": "Thumbnail (auto)",
            "export_config": "CONFIGURATION",
            "export_behavior": "Behavior",
            "export_fps": "Frame Rate",
            "export_scale": "Scale",
            "export_volume": "Volume",
            "export_lock": "Lock state",
            "export_notes": "PERSONAL NOTES",
            "export_notes_hint": "Optional, visible to the importer",
            "export_size_estimate": "Estimated size",
            "export_success": "Character exported successfully!",
            "export_failed": "Export failed",
            "import_title": "Import Character",
            "import_content_included": "CONTENT INCLUDED",
            "import_config_included": "CONFIGURATION INCLUDED",
            "import_apply": "Apply",
            "import_name": "NAME",
            "import_name_hint": "You can change the name before importing",
            "import_author_note": "Author note",
            "import_created": "Created on",
            "import_made_with": "Made with Aura Layer",
            "import_success": "Character imported successfully!",
            "import_failed": "Import .aura failed",
            "import_invalid": "Invalid .aura file",
            "import_invalid_desc": "The selected file is not a valid .aura package.",
            "import_too_many_files": "The archive contains too many files (limit exceeded).",
            "import_uncompressed_size": "The uncompressed archive size exceeds the allowed limit.",
            "import_unsafe_path": "Unsafe or invalid path or character name.",
            "import_invalid_manifest": "The .aura package manifest is incomplete or corrupted.",
            "import_anim_missing": "Animation file not found or missing in the .aura package.",
            "crash_critical_title": "Aura Layer - Critical Error",
            "crash_critical_msg": "An unexpected error occurred.\n\nDetails have been saved to:\n{path}",
            "import_conflict_title": "Name already exists",
            "import_conflict_msg": "A character named \"{name}\" already exists.\n\nDo you want to overwrite the existing character or rename?",
            "import_overwrite": "Overwrite",
            "import_rename": "Rename to \"{name}\"",
            "import_select_file": "Select .aura file",
            "import_deselect_hint": "Deselect to use default values",
            "aura_filter": "Aura Package (*.aura)",

            # Multi-Monitor
            "screen_auto": "Automatic (Remember position)",
            "screen_primary": "Primary",
            "screen_secondary": "Secondary",
            "msg_screen_disconnected": "A screen was disconnected. Characters have been repositioned to the primary monitor.",

            # Context menu
            "ctx_play_audio": "Play audio",
            "ctx_behavior": "Behavior",
            "ctx_move_to_screen": "Move to Screen",
            "ctx_lock": "Lock on desktop",
            "ctx_open_launcher": "Edit in Launcher",
            "ctx_remove_desktop": "Remove from desktop",
            "ctx_locked_notification_title": "Character Locked",
            "ctx_locked_notification_msg": "\"{name}\" is now click-through.\nYou can unlock from Launcher.",

            # Extra UI labels & stats
            "details_ai_tools": "GRAPHICS & AI TOOLS",
            "badge_active": "ACTIVE",
            "badge_ready": "READY",
            "stats_active_single": "1 active character",
            "stats_active_multi": "{active} active characters",
            "sidebar_active_single": "1 active companion",
            "sidebar_active_multi": "{active} active companions",
            "topbar_active_single": "1 active",
            "topbar_active_multi": "{active} active",
            "library_count_single": "1 item",
            "library_count_multi": "{total} items",
            "btn_processing": "Processing...",
            "screen_num": "Screen {i}",
            "filter_animation_files": "Animation files (*.gif *.png *.webp *.apng)",
            "export_no_audio": "No associated audio file",
            "export_thumb_auto": "Automatically generated (150x150)",
            "status_locked": "Locked",
            "status_unlocked": "Unlocked",
        }
    }
    
    def __init__(self, language: str = "it"):
        """Initialize translation system with specified language."""
        self.current_language = language
        if language not in self.TRANSLATIONS:
            self.current_language = "it"  # Default to Italian
    
    def set_language(self, language: str):
        """Change current language."""
        if language in self.TRANSLATIONS:
            self.current_language = language
    
    def get(self, key: str, default: str = None) -> str:
        """Get translation for a key."""
        if default is None:
            default = key
        return self.TRANSLATIONS[self.current_language].get(key, default)
    
    def t(self, key: str, default: str = None) -> str:
        """Short alias for get()."""
        return self.get(key, default)


# Global translation instance
_translation_instance = None

def init_translations(language: str = "it") -> Translations:
    """Initialize global translation instance."""
    global _translation_instance
    _translation_instance = Translations(language)
    return _translation_instance

def get_translations() -> Translations:
    """Get global translation instance."""
    global _translation_instance
    if _translation_instance is None:
        _translation_instance = Translations("it")
    return _translation_instance

def t(key: str, default: str = None) -> str:
    """Global translation function."""
    return get_translations().get(key, default)