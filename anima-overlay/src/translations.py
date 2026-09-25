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
            "tray_quit": "Esci",
            
            # Launcher window
            "launcher_title": "Aura Layer - Launcher",
            "launcher_characters": "Personaggi",
            "launcher_settings": "Impostazioni",
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
            "behavior_random_edge": "Bordo Casuale",
            "behavior_gravity": "Gravità",
            
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
            "info_version": "Versione: 1.0.0",
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
            "behavior_random_edge": "Bordi casuali",
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
            "dialog_remove_confirm": "Vuoi rimuovere definitivamente",
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
        },
        "en": {
            # Main application
            "app_name": "Aura Layer",
            "app_description": "Desktop character overlay application",
            
            # Tray menu
            "tray_open_launcher": "Open Launcher",
            "tray_toggle_all": "Show/Hide All",
            "tray_quit": "Quit",
            
            # Launcher window
            "launcher_title": "Aura Layer - Launcher",
            "launcher_characters": "Characters",
            "launcher_settings": "Settings",
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
            "behavior_random_edge": "Random Edge",
            "behavior_gravity": "Gravity",
            
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
            "info_version": "Version: 1.0.0",
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
            "behavior_random_edge": "Random edges",
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
            "dialog_remove_confirm": "Do you want to permanently remove",
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
    if _translation_instance is None:
        _translation_instance = Translations("it")
    return _translation_instance

def t(key: str, default: str = None) -> str:
    """Global translation function."""
    return get_translations().get(key, default)