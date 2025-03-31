import math
import json
import os
from collections import deque
from jinja2 import Template
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
# --- Multipliers and Bitmask Mappings ---
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
effect_to_bit = {eff: 1 << i for i, eff in enumerate(multipliers)}
bit_to_effect = {v: k for k, v in effect_to_bit.items()}
bit_to_multiplier = {effect_to_bit[k]: v for k, v in multipliers.items()}

def bitmask_to_effects(mask):
    return [bit_to_effect[b] for b in bit_to_effect if mask & b]

def compute_multiplier(mask):
    total = 0.0
    while mask:
        b = mask & -mask
        total += bit_to_multiplier[b]
        mask -= b
    return total

class Rule:
    def __init__(self, conditions, not_conditions, action, target, new_effect):
        self.cond_mask = sum(effect_to_bit[c] for c in conditions)
        self.not_cond_mask = sum(effect_to_bit[nc] for nc in not_conditions)
        self.action = action
        self.target_bit = effect_to_bit.get(target, 0)
        self.new_effect_bit = effect_to_bit[new_effect]

class Product:
    def __init__(self, name, default_effect, rules, default_effect_position="after", price=0):
        self.name = name
        self.default_effect = default_effect
        self.rules = [Rule(**r) for r in rules]
        self.default_effect_position = default_effect_position
        self.price = price

    def process(self, effects, max_effects=8, debug=False):
        result = effects
        if self.default_effect and self.default_effect_position == "before":
            result |= effect_to_bit[self.default_effect]
            if result.bit_count() >= max_effects:
                return result
        for rule in self.rules:
            if (result & rule.cond_mask) == rule.cond_mask and (result & rule.not_cond_mask) == 0:
                if rule.action == "replace":
                    candidate = (result & ~rule.target_bit) | rule.new_effect_bit
                elif rule.action == "add":
                    candidate = result | rule.new_effect_bit
                else:
                    continue
                if candidate.bit_count() <= max_effects:
                    result = candidate
        if self.default_effect and self.default_effect_position == "after":
            candidate = result | effect_to_bit[self.default_effect]
            if candidate.bit_count() <= max_effects:
                result = candidate
        return result

memo_process_product = {}
def process_product_cached(effects, product):
    key = (effects, id(product))
    if key in memo_process_product:
        return memo_process_product[key]
    res = product.process(effects)
    memo_process_product[key] = res
    return res

def make_rules(rules_tuples):
    result = []
    for tup in rules_tuples:
        if tup[2] == "+":
            conds, not_conds, _, new_eff = tup
            result.append({
                "conditions": list(conds) if isinstance(conds, (list, tuple)) else [conds],
                "not_conditions": list(not_conds) if isinstance(not_conds, (list, tuple)) else [not_conds] if not_conds else [],
                "action": "add",
                "target": None,
                "new_effect": new_eff
            })
        else:
            conds, not_conds, target, new_eff = tup
            result.append({
                "conditions": list(conds) if isinstance(conds, (list, tuple)) else [conds],
                "not_conditions": list(not_conds) if isinstance(not_conds, (list, tuple)) else [not_conds] if not_conds else [],
                "action": "replace",
                "target": target,
                "new_effect": new_eff
            })
    return result

cuke_rules = make_rules([
    ("Munchies", "Athletic", "Munchies", "Athletic"),
    ("Slippery", "Munchies", "Slippery", "Munchies"),
    ("Slippery", None, "Slippery", "Athletic"),
    ("Euphoric", None, "Euphoric", "Laxative"),
    ("Toxic", None, "Toxic", "Euphoric"),
    ("Sneaky", None, "Sneaky", "Paranoia"),
    ("Foggy", None, "Foggy", "Cyclopean"),
    ("Gingeritis", None, "Gingeritis", "Thought-Provoking"),
])
flu_medicine_rules = make_rules([
    ("Calming", None, "Calming", "Bright-Eyed"),
    ("Athletic", None, "Athletic", "Munchies"),
    ("Thought-Provoking", None, "Thought-Provoking", "Gingeritis"),
    ("Cyclopean", None, "Cyclopean", "Foggy"),
    ("Munchies", None, "Munchies", "Slippery"),
    ("Laxative", None, "Laxative", "Euphoric"),
    ("Euphoric", None, "Euphoric", "Toxic"),
    ("Focused", None, "Focused", "Calming"),
    ("Electrifying", None, "Electrifying", "Refreshing"),
    ("Shrinking", None, "Shrinking", "Paranoia"),
])
gasoline_rules = make_rules([
    (["Euphoric"], ["Energizing"], "Euphoric", "Spicy"),
    ("Energizing", None, "Energizing", "Euphoric"),
    ("Gingeritis", None, "Gingeritis", "Smelly"),
    ("Jennerising", None, "Jennerising", "Sneaky"),
    ("Sneaky", None, "Sneaky", "Tropic Thunder"),
    ("Munchies", None, "Munchies", "Sedating"),
    ("Laxative", None, "Laxative", "Foggy"),
    ("Disorienting", None, "Disorienting", "Glowing"),
    ("Paranoia", None, "Paranoia", "Calming"),
    ("Electrifying", None, "Electrifying", "Disorienting"),
    ("Shrinking", None, "Shrinking", "Focused"),
])
donut_rules = make_rules([
    (["Calorie-Dense"], ["Explosive"], "+", "Explosive"),
    ("Balding", None, "Balding", "Sneaky"),
    ("Anti-Gravity", None, "Anti-Gravity", "Slippery"),
    ("Jennerising", None, "Jennerising", "Gingeritis"),
    ("Focused", None, "Focused", "Euphoric"),
    ("Shrinking", None, "Shrinking", "Energizing"),
])
energy_drink_rules = make_rules([
    ("Sedating", None, "Sedating", "Munchies"),
    ("Euphoric", None, "Euphoric", "Energizing"),
    ("Spicy", None, "Spicy", "Euphoric"),
    ("Tropic Thunder", None, "Tropic Thunder", "Sneaky"),
    ("Glowing", None, "Glowing", "Disorienting"),
    ("Foggy", None, "Foggy", "Laxative"),
    ("Disorienting", None, "Disorienting", "Electrifying"),
    ("Schizophrenia", None, "Schizophrenia", "Balding"),
    ("Focused", None, "Focused", "Shrinking"),
])
mouth_wash_rules = make_rules([
    ("Calming", None, "Calming", "Anti-Gravity"),
    ("Calorie-Dense", None, "Calorie-Dense", "Sneaky"),
    ("Explosive", None, "Explosive", "Sedating"),
    ("Focused", None, "Focused", "Jennerising"),
])
motor_oil_rules = make_rules([
    ("Energizing", None, "Energizing", "Munchies"),
    ("Foggy", None, "Foggy", "Toxic"),
    ("Energizing", None, "Energizing", "Schizophrenia"),
    ("Euphoric", None, "Euphoric", "Sedating"),
    ("Paranoia", None, "Paranoia", "Anti-Gravity"),
    (["Munchies"], ["Energizing"], "Munchies", "Schizophrenia"),
])
banana_rules = make_rules([
    (["Energizing"], ["Cyclopean"], "Energizing", "Thought-Provoking"),
    (["Smelly"], ["Anti-Gravity"], "Smelly", "Anti-Gravity"),
    ("Calming", None, "Calming", "Sneaky"),
    ("Toxic", None, "Toxic", "Smelly"),
    ("Long Faced", None, "Long Faced", "Refreshing"),
    ("Cyclopean", None, "Cyclopean", "Thought-Provoking"),
    ("Disorienting", None, "Disorienting", "Focused"),
    ("Focused", None, "Focused", "Seizure-Inducing"),
])
chili_rules = make_rules([
    ("Athletic", None, "Athletic", "Euphoric"),
    ("Anti-Gravity", None, "Anti-Gravity", "Tropic Thunder"),
    ("Sneaky", None, "Sneaky", "Bright-Eyed"),
    ("Munchies", None, "Munchies", "Toxic"),
    ("Laxative", None, "Laxative", "Long Faced"),
    ("Shrinking", None, "Shrinking", "Refreshing"),
])
iodine_rules = make_rules([
    ("Calming", None, "Calming", "Balding"),
    ("Toxic", None, "Toxic", "Sneaky"),
    ("Foggy", None, "Foggy", "Paranoia"),
    ("Calorie-Dense", None, "Calorie-Dense", "Gingeritis"),
    ("Euphoric", None, "Euphoric", "Seizure-Inducing"),
    ("Refreshing", None, "Refreshing", "Thought-Provoking"),
])
paracetamol_rules = make_rules([
    ("Munchies", None, "Munchies", "Anti-Gravity"),
    ("Calming", None, "Calming", "Slippery"),
    ("Toxic", None, "Toxic", "Tropic Thunder"),
    ("Spicy", None, "Spicy", "Bright-Eyed"),
    ("Glowing", None, "Glowing", "Toxic"),
    ("Foggy", None, "Foggy", "Calming"),
    ("Munchies", None, "Munchies", "Anti-Gravity"),
    (["Energizing", "Paranoia"], None, "Energizing", "Balding"),
    ("Electrifying", None, "Electrifying", "Athletic"),
    (["Energizing"], ["Munchies"], "Energizing", "Paranoia"),
])
viagra_rules = make_rules([
    ("Athletic", None, "Athletic", "Sneaky"),
    ("Euphoric", None, "Euphoric", "Bright-Eyed"),
    ("Laxative", None, "Laxative", "Calming"),
    ("Disorienting", None, "Disorienting", "Toxic"),
])
horse_semen_rules = make_rules([
    ("Anti-Gravity", None, "Anti-Gravity", "Calming"),
    ("Gingeritis", None, "Gingeritis", "Refreshing"),
    (["Thought-Provoking"], ["Seizure-Inducing"], "Thought-Provoking", "Electrifying"),
])
mega_bean_rules = make_rules([
    (["Energizing"], ["Thought-Provoking"], "Energizing", "Cyclopean"),
    ("Calming", None, "Calming", "Glowing"),
    ("Sneaky", None, "Sneaky", "Calming"),
    ("Jennerising", None, "Jennerising", "Paranoia"),
    ("Slippery", None, "Slippery", "Toxic"),
    ("Thought-Provoking", None, "Thought-Provoking", "Energizing"),
    ("Seizure-Inducing", None, "Seizure-Inducing", "Focused"),
    ("Focused", None, "Focused", "Disorienting"),
    ("Sneaky", None, "Sneaky", "Glowing"),
    ("Thought-Provoking", None, "Thought-Provoking", "Cyclopean"),
    ("Shrinking", None, "Shrinking", "Electrifying"),
    ("Athletic", None, "Athletic", "Laxative"),
])
battery_rules = make_rules([
    ("Munchies", None, "Munchies", "Tropic Thunder"),
    (["Euphoric"], "Electrifying", "Euphoric", "Zombifying"),
    (["Electrifying"], "Zombifying", "Electrifying", "Euphoric"),
    ("Laxative", None, "Laxative", "Calorie-Dense"),
    ("Electrifying", None, "Electrifying", "Euphoric"),
    ("Shrinking", None, "Shrinking", "Munchies"),
    ("Cyclopean", "Glowing", "Cyclopean", "Glowing"),
])
addy_rules = make_rules([
    ("Sedating", None, "Sedating", "Gingeritis"),
    ("Long Faced", None, "Long Faced", "Electrifying"),
    ("Glowing", None, "Glowing", "Refreshing"),
    ("Foggy", None, "Foggy", "Energizing"),
    ("Explosive", None, "Explosive", "Euphoric"),
])

base_products = [
    Product("OG Kush", "Calming", [], price=35),
    Product("Sour Diesel", "Refreshing", [], price=35),
    Product("Green Crack", "Energizing", [], price=35),
    Product("Grandaddy purple", "Sedating", [], price=35),
    Product("Meth", None, [], price=70),
    Product("Cocaine", None, [], price=150)
]

products = []
products.append(Product("Cuke", "Energizing", cuke_rules, price=2))
products.append(Product("Flu Medicine", "Sedating", flu_medicine_rules, price=2))
products.append(Product("Gasoline", "Toxic", gasoline_rules, price=5))
products.append(Product("Donut", "Calorie-Dense", donut_rules, default_effect_position="after", price=2))
products.append(Product("Energy Drink", "Athletic", energy_drink_rules, price=6))
products.append(Product("Mouth Wash", "Balding", mouth_wash_rules, price=4))
products.append(Product("Motor Oil", "Slippery", motor_oil_rules, price=4))
products.append(Product("Banana", "Gingeritis", banana_rules, price=4))
products.append(Product("Chili", "Spicy", chili_rules, price=7))
products.append(Product("Iodine", "Jennerising", iodine_rules, price=6))
products.append(Product("Paracetamol", "Sneaky", paracetamol_rules, price=6))
products.append(Product("Viagra", "Tropic Thunder", viagra_rules, price=6))
products.append(Product("Horse Semen", "Long Faced", horse_semen_rules, price=8))
products.append(Product("Mega Bean", "Foggy", mega_bean_rules, price=7))
products.append(Product("Addy", "Thought-Provoking", addy_rules, price=9))
products.append(Product("Battery", "Bright-Eyed", battery_rules, price=8))

all_products = base_products + products
def find_best_sequences_by_length_for_base_cost(base, supplemental_products, max_length=10, max_effects=8, debug=False):
    stats = {k: 0 for k in [
        "states_popped", "states_added", "pruned_delta", "pruned_length",
        "pruned_effects", "pruned_back_to_back", "pruned_drop", "pruned_visited"
    ]}
    best_by_length = {}
    all_candidates = []
    initial_effects = process_product_cached(0, base)
    initial_state = (initial_effects, (base,), 0, base.price * compute_multiplier(initial_effects), 0, -1)
    queue = deque([initial_state])
    visited = {(initial_effects, -1, 0): 0}
    global_best_net = initial_state[3]
    global_best_total_value = math.ceil(base.price * (1 + compute_multiplier(initial_effects)))
    delta_max = max(base.price * compute_multiplier(process_product_cached(0, p)) - p.price for p in supplemental_products)
    while queue:
        stats["states_popped"] += 1
        effects, seq, cost, net, drop_count, last_index = queue.popleft()
        seq_names = [p.name for p in seq]
        length = len(seq)
        multiplier = compute_multiplier(effects)
        current_net = base.price * multiplier - cost
        total_value = math.ceil(base.price * (1 + multiplier))
        all_candidates.append({
            "sequence": seq_names,
            "effects": bitmask_to_effects(effects),
            "total_multiplier": multiplier,
            "cost": cost,
            "net_benefit": current_net,
            "expected_total_value": total_value
        })
        if length not in best_by_length or current_net > best_by_length[length]["net_benefit"]:
            best_by_length[length] = {
                "sequence": seq_names,
                "effects": bitmask_to_effects(effects),
                "total_multiplier": multiplier,
                "cost": cost,
                "net_benefit": current_net,
                "expected_total_value": total_value
            }
            global_best_net = max(global_best_net, current_net)
            if total_value > global_best_total_value:
                global_best_total_value = total_value
        if length >= max_length or effects.bit_count() >= max_effects or current_net + (max_length - length) * delta_max < global_best_net:
            continue
        for i, prod in enumerate(supplemental_products):
            if i == last_index:
                continue
            new_effects = process_product_cached(effects, prod)
            if new_effects.bit_count() > max_effects:
                continue
            new_cost = cost + prod.price
            new_multiplier = compute_multiplier(new_effects)
            new_drop = drop_count + 1 if new_multiplier < multiplier else drop_count
            if new_drop >= 3:
                continue
            new_net = base.price * new_multiplier - new_cost
            key = (new_effects, i, new_drop)
            if key in visited and visited[key] <= new_cost:

                continue
            visited[key] = new_cost
            queue.append((new_effects, seq + (prod,), new_cost, new_net, new_drop, i))

    best_total_value = max(all_candidates, key=lambda x: (x["expected_total_value"], -x["cost"]))
    best_net = max(all_candidates, key=lambda x: x["net_benefit"])
    return {
        "best_value": best_total_value,
        "best_net": best_net,
        "by_length": best_by_length
    }
def get_optimal_combo_for_bitmap(primary_product, product_bitmap, max_length=9, max_effects=8, debug=False):
    allowed_products = [p for i, p in enumerate(products) if (product_bitmap >> i) & 1]
    return find_best_sequences_by_length_for_base_cost(primary_product, allowed_products, max_length, max_effects, debug)

def precompute_all():
    precomputed = {}
    # Determine the maximum required level index from product_unlock_levels.
    max_unlock_index = max(AVAILABLE_LEVELS.index(unlock) for unlock in product_unlock_levels)
    
    for bp in base_products:
        precomputed[bp.name] = {}
        # We will store the result computed at the max unlock level for reuse.
        result_at_max = None
        for lvl in AVAILABLE_LEVELS:
            lvl_index = AVAILABLE_LEVELS.index(lvl)
            if lvl_index >= max_unlock_index and result_at_max is not None:
                # For any level beyond the highest unlock, copy the result computed at max_unlock_index.
                precomputed[bp.name][lvl] = result_at_max
            else:
                bitmap = get_product_bitmap(lvl)
                result = get_optimal_combo_for_bitmap(bp, bitmap)
                # Convert integer keys in "by_length" to strings for JSON serialization.
                result["by_length"] = {str(k): v for k, v in result["by_length"].items()}
                precomputed[bp.name][lvl] = result
                # If this level is the max unlock level, store its result.
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

def get_product_bitmap(player_level: str) -> int:
    level_index = AVAILABLE_LEVELS.index(player_level)
    bitmap = 0
    for i, unlock_level in enumerate(product_unlock_levels):
        if AVAILABLE_LEVELS.index(unlock_level) <= level_index:
            bitmap |= (1 << i)
    return bitmap

def filter_duplicates(precomputed):
    """
    For each base product and level, filter out duplicate combos from the "by_length"
    dictionary. Two combos are considered duplicate if their sequence lists are identical.
    """
    filtered = {}
    for base, levels in precomputed.items():
        filtered[base] = {}
        for level, result in levels.items():
            seen = set()
            unique_by_length = {}
            # Loop through each sequence length.
            for length, combo in result["by_length"].items():
                # Convert the sequence list to a tuple so it can be used in a set.
                seq_tuple = tuple(combo["sequence"])
                if seq_tuple not in seen:
                    seen.add(seq_tuple)
                    unique_by_length[length] = combo
            new_result = dict(result)
            new_result["by_length"] = unique_by_length
            filtered[base][level] = new_result
    return filtered

html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Optimal Combo Optimizer Results</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; }
    select { font-size: 1em; padding: 0.25em; }
    table { border-collapse: collapse; width: 100%; margin-top: 1em; }
    th, td { border: 1px solid #ccc; padding: 0.5em; text-align: center; }
    th { background-color: #f0f0f0; }
    .hidden { display: none; }
  </style>
</head>
<body>
  <h1>Optimal Combo Optimizer Results</h1>
  
  <label for="baseSelect">Select Primary Product:</label>
  <select id="baseSelect"></select>
  <br><br>
  <label for="levelSelect">Select Your Level:</label>
  <select id="levelSelect"></select>
  <br><br>
  <button id="viewButton">View Results</button>

  <div id="resultsSection" class="hidden">
    <h2>Results</h2>
    <div id="resultsContent"></div>
  </div>

  <script>
    const precomputedData = {{ precomputed|tojson }};
    const availableLevels = {{ levels|tojson }};
    const baseProductNames = {{ base_products|tojson }};
    
    const baseSelect = document.getElementById("baseSelect");
    const levelSelect = document.getElementById("levelSelect");
    const resultsSection = document.getElementById("resultsSection");
    const resultsContent = document.getElementById("resultsContent");
    
    // Populate base product dropdown in order.
    baseProductNames.forEach(base => {
      const opt = document.createElement("option");
      opt.value = base;
      opt.innerText = base;
      baseSelect.appendChild(opt);
    });
    
    // Populate level dropdown in order.
    function updateLevels() {
      const selectedBase = baseSelect.value;
      levelSelect.innerHTML = "";
      availableLevels.forEach(level => {
        if (precomputedData[selectedBase] && precomputedData[selectedBase][level]) {
          const opt = document.createElement("option");
          opt.value = level;
          opt.innerText = level;
          levelSelect.appendChild(opt);
        }
      });
    }
    
    baseSelect.addEventListener("change", updateLevels);
    updateLevels();
    
    document.getElementById("viewButton").addEventListener("click", function() {
      const selectedBase = baseSelect.value;
      const selectedLevel = levelSelect.value;
      if (!precomputedData[selectedBase] || !precomputedData[selectedBase][selectedLevel]) {
        resultsContent.innerHTML = "<p>No data available for this selection.</p>";
        resultsSection.classList.remove("hidden");
        return;
      }
      
      const result = precomputedData[selectedBase][selectedLevel];
      let html = "";
      const lengths = Object.keys(result.by_length).map(x => parseInt(x)).sort((a, b) => a - b);
      html += "<table>";
      html += "<thead><tr><th>Len</th><th>Δ Net</th><th>Net Benefit</th><th>Expected Value</th><th>Cost</th><th>Multiplier</th><th># Effects</th><th>Sequence</th><th>Effects</th></tr></thead><tbody>";
      let lastNet = null;
      lengths.forEach(len => {
        const combo = result.by_length[len.toString()];
        const net = combo.net_benefit;
        const delta = (lastNet !== null) ? (net - lastNet).toFixed(2) : "–";
        lastNet = net;
        html += `<tr>
                  <td>${len}</td>
                  <td>${delta}</td>
                  <td>${combo.net_benefit}</td>
                  <td>${combo.expected_total_value}</td>
                  <td>${combo.cost}</td>
                  <td>${combo.total_multiplier.toFixed(2)}</td>
                  <td>${combo.effects.length}</td>
                  <td>${combo.sequence.join(", ")}</td>
                  <td>${combo.effects.join(", ")}</td>
                </tr>`;
      });
      html += "</tbody></table>";
      resultsContent.innerHTML = html;
      resultsSection.classList.remove("hidden");
    });
  </script>
</body>
</html>
"""

template = Template(html_template)

def generate_static_html(precomputed):
    rendered_html = template.render(precomputed=precomputed,
                                    levels=AVAILABLE_LEVELS,
                                    base_products=BASE_PRODUCT_NAMES)
    with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"Static HTML file generated: {OUTPUT_HTML_FILE}")

PRECOMPUTED_FILE = "precomputed_results.json"
OUTPUT_HTML_FILE = "index.html"
if __name__ == "__main__":
    if os.path.exists(PRECOMPUTED_FILE):
        with open(PRECOMPUTED_FILE, "r") as f:
            precomputed = json.load(f)
    else:
        precomputed = precompute_all()
    generate_static_html(precomputed)