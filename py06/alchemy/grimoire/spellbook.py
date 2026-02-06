""" Records spells and their effects """

def record_spell(spell_name: str, ingredients: str) -> str:
    """ record spell a b c """

    from alchemy.grimoire.validator import validate_ingredients
    res = validate_ingredients(ingredients)
    if "VALID" in res:
        return f"Spell recorded: {spell_name} ({res})"
    else:
        return f"Spell rejected: {spell_name} ({res})"
