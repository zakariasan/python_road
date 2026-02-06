"""Demonstration script """
from alchemy.grimoire import validate_ingredients, record_spell

print("\n=== Circular Curse Breaking ===\n")

print("Testing ingredient validation:")
ing: str = "fire air"
print(f'validate_ingredients("{ing}"): {validate_ingredients(ing)}')
ing = "dragon scales"
print(f'validate_ingredients("{ing}"): {validate_ingredients(ing)}')

print()
print("Testing spell recording with validation:")
print(
        'record_spell("Fireball", "fire air"): '
        +
        f"{record_spell("Fireball", "fire air")}"
        )
print(
        'record_spell("Dark Magic", "shadow"): '
        +
        f"{record_spell("Dark Magic", "shadow")}"
        )
print()
print("Testing late import technique:")
print(
        'record_spell("Lightning", "air"): '
        +
        f"{record_spell("Lightning", "air")}"
        )
print("\nCircular dependency curse avoided using late imports!")
print("All spells processed safely!")
