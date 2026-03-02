"""
Exercise 1: Higher Realm - Functions operating on functions
"""


def spell_combiner(spell1: callable, spell2: callable) -> callable:
    """ Combine two spells """
    return lambda *args, **kwargs: (
            spell1(*args, **kwargs), spell2(*args, **kwargs))


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    """ Amplify spell power """
    return lambda *args, **kwargs: base_spell(*args, **kwargs) * multiplier


def conditional_caster(condition: callable, spell: callable) -> callable:
    return lambda *args, **kwargs: (
            spell(*args, **kwargs)
            if condition(*args, **kwargs) else "Spell fizzled"
            )


def spell_sequence(spells: list[callable]) -> callable:
    """ Cast spell conditionally """
    return lambda *args, **kwargs: [spell(*args, **kwargs) for spell in spells]


if __name__ == '__main__':
    try:
        print("Testing spell combiner...")
        combined = spell_combiner(
                lambda target: f"Fireball hits {target}",
                lambda target: f"Heals {target}"
                )
        result = combined("Dragon")
        print(f"Combined spell result: {result[0]}, {result[1]}")

        print("\nTesting power amplifier...")
        mega_damage = power_amplifier(lambda power: power * 2, 3)
        print(f"Original: 20, Amplified: {mega_damage(10)}")

        print("\nTesting conditional caster...")
        guarded_fireball = conditional_caster(
                lambda target: target in ['Dragon', 'Orc', 'Troll'],
                lambda target: f"Fireball hits {target}")
        print(guarded_fireball("Dragon"))
        print(guarded_fireball("Villager"))

        print("\nTesting spell sequence...")
        sequence = spell_sequence(
                [lambda target: f"Fireball hits {target}",
                 lambda target: f"Heals {target}",
                 lambda target: f"Fireball hits {target}"])
        for result in sequence("Dragon"):
            print(result)
    except Exception as e:
        print(f"Error : str{e}")
