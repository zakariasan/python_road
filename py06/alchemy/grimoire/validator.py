"""Validates spell ingredients"""


def validate_ingredients(ingredients: str) -> str:
    """ validate the ingredients send """
    valid_elements = ["fire", "water", "earth", "air"]
    is_valid = False
    for element in valid_elements:
        if element in ingredients.lower():
            is_valid = True
            break
    if is_valid:
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
