# --- Global Game Data ---
BASE_PRODUCT_NAMES = [
    "OG Kush", "Sour Diesel", "Green Crack", "Grandaddy purple", "Meth", "Cocaine"
]

product_unlock_levels = [
    "Street Rat I",   # 0 - Cuke
    "Hoodlum IV",     # 1 - Flu Medicine
    "Hoodlum V",      # 2 - Gasoline
    "Street Rat I",   # 3 - Donut
    "Peddler I",      # 4 - Energy Drink
    "Hoodlum III",    # 5 - Mouth Wash
    "Peddler II",     # 6 - Motor Oil
    "Street Rat I",   # 7 - Banana
    "Peddler IV",     # 8 - Chili
    "Hustler I",      # 9 - Iodine
    "Street Rat I",   # 10 - Paracetamol
    "Hoodlum II",     # 11 - Viagra
    "Hustler III",    # 12 - Horse Semen
    "Peddler III",    # 13 - Mega Bean
    "Hustler II",     # 14 - Addy
    "Peddler V",      # 15 - Battery
]

AVAILABLE_LEVELS = [
    "Street Rat I", "Street Rat II", "Street Rat III", "Street Rat IV", "Street Rat V",
    "Hoodlum I", "Hoodlum II", "Hoodlum III", "Hoodlum IV", "Hoodlum V",
    "Peddler I", "Peddler II", "Peddler III", "Peddler IV", "Peddler V",
    "Hustler I", "Hustler II", "Hustler III", "Hustler IV", "Hustler V",
    "Bagman I", "Bagman II", "Bagman III", "Bagman IV", "Bagman V",
    "Enforcer I", "Enforcer II", "Enforcer III", "Enforcer IV", "Enforcer V",
    "Shot Caller I", "Shot Caller II", "Shot Caller III", "Shot Caller IV", "Shot Caller V",
    "Block Boss I", "Block Boss II", "Block Boss III", "Block Boss IV", "Block Boss V",
    "Underlord I", "Underlord II", "Underlord III", "Underlord IV", "Underlord V",
    "Baron I", "Baron II", "Baron III", "Baron IV", "Baron V",
    "Kingpin I++"
]

# --- Multipliers and Effect Mappings ---
multipliers = {
    "Disorienting": 0.00, "Laxative": 0.00, "Paranoia": 0.00, "Schizophrenia": 0.00,
    "Seizure-Inducing": 0.00, "Smelly": 0.00, "Toxic": 0.00, "Explosive": 0.00,
    "Calming": 0.10, "Munchies": 0.12, "Refreshing": 0.14, "Focused": 0.16,
    "Euphoric": 0.18, "Gingeritis": 0.20, "Energizing": 0.22, "Sneaky": 0.24,
    "Sedating": 0.26, "Calorie-Dense": 0.28, "Balding": 0.30, "Athletic": 0.32,
    "Slippery": 0.34, "Foggy": 0.36, "Spicy": 0.38, "Bright-Eyed": 0.40,
    "Jennerising": 0.42, "Thought-Provoking": 0.44, "Tropic Thunder": 0.46,
    "Glowing": 0.48, "Electrifying": 0.50, "Long Faced": 0.52, "Anti-Gravity": 0.54,
    "Cyclopean": 0.56, "Zombifying": 0.58, "Shrinking": 0.60
}

# Filenames for outputs and precomputed results
PRECOMPUTED_FILE = "precomputed_results.json"
OUTPUT_HTML_FILE = "index.html"
