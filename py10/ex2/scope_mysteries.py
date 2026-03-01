"""
Exercise 2: Memory Depths - Lexical scoping and closures
"""

def mage_counter() -> callable:
    count = 0
    def counter():          # nonlocal needed -> must use def
        nonlocal count
        count += 1
        return count
    return counter



def spell_accumulator(initial_power: int) -> callable:
    total = initial_power
    def accumulate(amount):  # nonlocal needed -> must use def
        nonlocal total
        total += amount
        return total
    return accumulate

def enchantment_factory(enchantment_type: str) -> callable:
    return lambda item_name: f"{enchantment_type} {item_name}"  # only reads -> lambda works

def memory_vault() -> dict[str, callable]:
    vault = {}
    return {
        'store':  lambda key, value: vault.update({key: value}),  # mutates dict -> lambda works
        'recall': lambda key: vault.get(key, "Memory not found")
    }


if __name__ == '__main__':
    print("Testing mage counter...")
    counter = mage_counter()
    print(f"Call 1: {counter()}")
    print(f"Call 2: {counter()}")
    print(f"Call 3: {counter()}")

    print("\nTesting spell accumulator...")
    accumulate = spell_accumulator(100)
    print(f"After +50: {accumulate(50)}")
    print(f"After +30: {accumulate(30)}")
    print(f"After +20: {accumulate(20)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen  = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault['store']("spell", "fireball")
    vault['store']("power", 9000)
    print(vault['recall']("spell"))
    print(vault['recall']("power"))
    print(vault['recall']("unknown"))
