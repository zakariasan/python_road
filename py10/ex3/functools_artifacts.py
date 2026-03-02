"""
Exercise 3: Ancient Library - Functools treasures
"""
import functools


def spell_reducer(spells: list[int], operation: str) -> int:
    """ Reduce spell powers """
    op = {
            'add': lambda a, b: a + b,
            'multiply': lambda a, b: a * b,
            'max': lambda a, b: a if a > b else b,
            'min': lambda a, b: a if a < b else b
    }
    return functools.reduce(op[operation], spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    """ Create partial applications """
    return {
        'fire_enchant': functools.partial(
            base_enchantment,
            power=50, element='fire'),
        'ice_enchant': functools.partial(
            base_enchantment,
            power=50,
            element='ice'),
        'lightning_enchant': functools.partial(
            base_enchantment,
            power=50,
            element='lightning')
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """ Cached fibonacci """
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    """ Create single dispatch system: """
    @functools.singledispatch
    def dispatc(spell) -> str:
        """ spell is unknown """
        return f"Unknown spell type: {type(spell)}"

    @dispatc.register(int)
    def _(spell) -> str:
        """ damage one """
        return f"Damage spell: {spell} damage dealt"

    @dispatc.register(str)
    def _(spell) -> str:
        """ applied one """
        return f"Enchantment: {spell} applied"

    @dispatc.register(list)
    def _(spell) -> str:
        """ applied one """
        return f"Multi-cast: {len(spell)} spells cast -> {spell}"

    return dispatc


if __name__ == '__main__':
    try:
        spells = [10, 20, 30, 40]

        print("Testing spell reducer...")
        print(f"Sum: {spell_reducer(spells, 'add')}")
        print(f"Product: {spell_reducer(spells, 'multiply')}")
        print(f"Max: {spell_reducer(spells, 'max')}")
        print(f"Min: {spell_reducer(spells, 'min')}")

        print("\nTesting partial enchanter...")

        def base_enchantment(target, power, element):
            """ handler to check """
            return (
                    f"{element.capitalize()} enchantment"
                    " on {target} with power {power}")

        enchants = partial_enchanter(base_enchantment)
        print(enchants['fire_enchant'](target='Sword'))
        print(enchants['ice_enchant'](target='Shield'))
        print(enchants['lightning_enchant'](target='Staff'))

        print("\nTesting memoized fibonacci...")
        print(f"Fib(10): {memoized_fibonacci(10)}")
        print(f"Fib(15): {memoized_fibonacci(15)}")
        print(f"Fib(30): {memoized_fibonacci(30)}")

        print("\nTesting spell dispatcher...")
        dispatcher = spell_dispatcher()
        print(dispatcher(42))
        print(dispatcher("fireball"))
        print(dispatcher(["fireball", "heal", "shield"]))
    except Exception as e:
        print(f"Error {str(e)}")
