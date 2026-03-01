"""
Exercise 1: Higher Realm - Functions operating on functions
"""


def spell_combiner(spell1: callable, spell2: callable) -> callable:
    return lambda *args, **kwargs: (
            spell1(*args, **kwargs), spell2(*args, **kwargs))


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    return lambda *args, **kwargs: base_spell(*args, **kwargs) * multiplier


def conditional_caster(condition: callable, spell: callable) -> callable:
    return lambda *args, **kwargs: (
            spell(*args, **kwargs)
            if condition(*args, **kwargs) else "Spell fizzled"
            )


def spell_sequence(spells: list[callable]) -> callable:
    return lambda *args, **kwargs: [spell(*args, **kwargs) for spell in spells]


if __name__ == '__main__':
    fireball = lambda target: f"Fireball hits {target}" # noqa
    heal     = lambda target: f"Heals {target}" # noqa
    damage   = lambda power: power * 2 # noqa
    is_enemy = lambda target: target in ['Dragon', 'Orc', 'Troll'] # noqa

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon")
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    mega_damage = power_amplifier(damage, 3)
    print(f"Original: {damage(10)}, Amplified: {mega_damage(10)}")

    print("\nTesting conditional caster...")
    guarded_fireball = conditional_caster(is_enemy, fireball)
    print(guarded_fireball("Dragon"))
    print(guarded_fireball("Villager"))

    print("\nTesting spell sequence...")
    sequence = spell_sequence([fireball, heal, fireball])
    for result in sequence("Dragon"):
        print(result)
