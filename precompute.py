import os
import json
from config import PRECOMPUTED_FILE, AVAILABLE_LEVELS, product_unlock_levels
from optimizer import get_optimal_combo_for_bitmap
from rules import base_products

def get_product_bitmap(player_level: str) -> int:
    level_index = AVAILABLE_LEVELS.index(player_level)
    bitmap = 0
    for i, unlock_level in enumerate(product_unlock_levels):
        if AVAILABLE_LEVELS.index(unlock_level) <= level_index:
            bitmap |= (1 << i)
    return bitmap

def precompute_all():
    precomputed = {}
    max_unlock_index = max(AVAILABLE_LEVELS.index(unlock) for unlock in product_unlock_levels)
    
    for bp in base_products:
        precomputed[bp.name] = {}
        result_at_max = None
        for lvl in AVAILABLE_LEVELS:
            lvl_index = AVAILABLE_LEVELS.index(lvl)
            if lvl_index >= max_unlock_index and result_at_max is not None:
                precomputed[bp.name][lvl] = result_at_max
            else:
                bitmap = get_product_bitmap(lvl)
                result = get_optimal_combo_for_bitmap(bp, bitmap)
                result["by_length"] = {str(k): v for k, v in result["by_length"].items()}
                precomputed[bp.name][lvl] = result
                if lvl_index == max_unlock_index:
                    result_at_max = result
    with open(PRECOMPUTED_FILE, "w") as f:
        json.dump(precomputed, f)
    return precomputed

def load_precomputed():
    if os.path.exists(PRECOMPUTED_FILE):
        with open(PRECOMPUTED_FILE, "r") as f:
            return json.load(f)
    else:
        return precompute_all()

def filter_duplicates(precomputed):
    """
    For each base product and level, filter out duplicate combos from the "by_length"
    dictionary.
    """
    filtered = {}
    for base, levels in precomputed.items():
        filtered[base] = {}
        for level, result in levels.items():
            seen = set()
            unique_by_length = {}
            for length, combo in result["by_length"].items():
                seq_tuple = tuple(combo["sequence"])
                if seq_tuple not in seen:
                    seen.add(seq_tuple)
                    unique_by_length[length] = combo
            new_result = dict(result)
            new_result["by_length"] = unique_by_length
            filtered[base][level] = new_result
    return filtered
