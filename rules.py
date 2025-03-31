from products import Product

def make_rules(rules_tuples):
    result = []
    for tup in rules_tuples:
        if tup[2] == "+":
            conds, not_conds, _, new_eff = tup
            result.append({
                "conditions": list(conds) if isinstance(conds, (list, tuple)) else [conds],
                "not_conditions": [not_conds] if isinstance(not_conds, str) else list(not_conds) if not_conds else [],
                "action": "add",
                "target": None,
                "new_effect": new_eff
            })
        else:
            conds, not_conds, target, new_eff = tup
            result.append({
                "conditions": list(conds) if isinstance(conds, (list, tuple)) else [conds],
                "not_conditions": [not_conds] if isinstance(not_conds, str) else list(not_conds) if not_conds else [],
                "action": "replace",
                "target": target,
                "new_effect": new_eff
            })
    return result


# --- Rule Definitions ---
cuke_rules = make_rules([
    ("Munchies", ["Athletic"], "Munchies", "Athletic"),
    ("Slippery", ["Munchies"], "Slippery", "Munchies"),
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

from products import Product
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
