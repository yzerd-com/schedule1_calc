from config import multipliers

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
        self.not_cond_mask = sum(effect_to_bit[nc] for nc in not_conditions) if not_conditions else 0
        self.action = action
        self.target_bit = effect_to_bit.get(target, 0) if target else 0
        self.new_effect_bit = effect_to_bit[new_effect]

class Product:
    def __init__(self, name, default_effect, rules, default_effect_position="after", price=0):
        self.name = name
        self.default_effect = default_effect
        self.rules = [Rule(**r) for r in rules]
        self.default_effect_position = default_effect_position
        self.price = price

    def process(self, effects, max_effects=8):
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