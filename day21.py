from itertools import product
import os

lines = open("day21.input").read().split(os.linesep)

ingredient_counts = {}
allergen_ingredients = {}

for line in lines:
    ingredient_list, allergen_list = line[:-1].split("(contains ")
    ingredients = set(ingredient_list.strip().split(" "))
    allergens = set(allergen_list.split(", "))

    for ingredient in ingredients:
        ingredient_counts.setdefault(ingredient, 0)
        ingredient_counts[ingredient] += 1

    for allergen in allergens:
        allergen_ingredients.setdefault(allergen, ingredients)
        allergen_ingredients[allergen] = ingredients.intersection(allergen_ingredients[allergen])

all_ingredients = set(ingredient_counts.keys())
with_allergens = set().union(*allergen_ingredients.values())

# Part 1 answer
print(sum([ingredient_counts[i] for i in list(all_ingredients - with_allergens)]))


dangerous = {}
while len(dangerous) != len(allergen_ingredients):
    for allergen, ingredients in allergen_ingredients.items():
        if allergen in dangerous:
            continue

        if len(ingredients) == 1:
            dangerous[allergen] = list(ingredients)[0]
        else:
            allergen_ingredients[allergen] = ingredients - set(dangerous.values())

# Part 2 answer
print(",".join([dangerous[allergen] for allergen in sorted(dangerous.keys())]))