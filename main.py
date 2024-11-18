import data
import itertools
import math

alchemy_level = 100
perk_alchemist_mult = 2
perk_benefactor_mult = 1.25
perk_poisoner_mult = 1.25

recipes = []

has_physician = True
every_recipe = itertools.combinations(data.ingredients.keys(), 3)

for ingr_1, ingr_2, ingr_3 in every_recipe:
    #if "CC" in ingr_1 or "CC" in ingr_2 or "CC" in ingr_3:
    #    continue
    effect_mgefs_1 = {effect["mgef"] for effect in data.ingredients[ingr_1]}
    effect_mgefs_2 = {effect["mgef"] for effect in data.ingredients[ingr_2]}
    effect_mgefs_3 = {effect["mgef"] for effect in data.ingredients[ingr_3]}
    list_effects = []
    for effect in data.ingredients[ingr_1]:
        if effect["mgef"] in effect_mgefs_2.union(effect_mgefs_3):
            list_effects.append(effect)
    for effect in data.ingredients[ingr_2]:
        if effect["mgef"] in effect_mgefs_3.union(effect_mgefs_1):
            list_effects.append(effect)
    for effect in data.ingredients[ingr_3]:
        if effect["mgef"] in effect_mgefs_1.union(effect_mgefs_2):
            list_effects.append(effect)
    if not list_effects:
        continue
    # print(ingr_1, "|", ingr_2, "|", ingr_3)
    effect_dict = {}
    for effect in list_effects:
        if effect["mgef"] not in effect_dict:
            effect_dict[effect["mgef"]] = effect
        else:
            if effect_dict[effect["mgef"]]["cost"] <= effect["cost"]:
                effect_dict[effect["mgef"]] = effect
    total_gold = 0
    for effect in effect_dict.values():
        if effect["mgef"].startswith("Restore") and has_physician:
            perk_physician_mult = 1.25
        else:
            perk_physician_mult = 1
        power_factor = 4 * (1 + alchemy_level / 200) * perk_physician_mult * perk_alchemist_mult
        if data.effects[effect["mgef"]]["perk_type"] == "Pos":
            power_factor *= perk_benefactor_mult
        else:
            power_factor *= perk_poisoner_mult
        magnitude = effect["magnitude"]
        duration = effect["duration"]
        if data.effects[effect["mgef"]]["bonus_type"] == "Mag":
            magnitude *= power_factor
        elif data.effects[effect["mgef"]]["bonus_type"] == "Dur":
            duration *= power_factor
        else:
            raise ValueError(f'Unknown bonus type {data.effects[effect["mgef"]]["bonus_type"]}')
        magnitude = max(round(magnitude) ** 1.1, 1)
        duration = (round(duration) // 10) ** 1.1
        if not duration:
            duration = 1
        ##
        if data.effects[effect["mgef"]]["bonus_type"] == "Mag":
            magnitude = round(effect["magnitude"] * power_factor)
            duration = effect["duration"]
        else:
            duration = round(effect["duration"] * power_factor)
            magnitude = effect["magnitude"]
        if not duration:
            duration = 1

        gold_cost = round(data.effects[effect["mgef"]]["cost"] * max(magnitude ** 1.1, 1) * (duration/10)**1.1)
        # print(effect, gold_cost)
        total_gold += gold_cost
    recipes.append((ingr_1, ingr_2, ingr_3, total_gold))

recipes.sort(key=lambda x: x[3], reverse=True)
for recipe in recipes[:50]:
    print(recipe)
