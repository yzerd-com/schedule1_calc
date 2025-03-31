import math
from collections import deque
from products import process_product_cached, compute_multiplier, bitmask_to_effects
from rules import products

def find_best_sequences_by_length_for_base_cost(base, supplemental_products, max_length=10, max_effects=8):
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

def get_optimal_combo_for_bitmap(primary_product, product_bitmap, max_length=9, max_effects=8):
    allowed_products = [p for i, p in enumerate(products) if (product_bitmap >> i) & 1]
    return find_best_sequences_by_length_for_base_cost(primary_product, allowed_products, max_length, max_effects)
