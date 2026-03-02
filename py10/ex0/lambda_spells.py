"""
Exercise 0: Lambda Sanctum - Master anonymous functions and lambda expressions
"""


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """ Sort magical artifacts. """
    return list(sorted(artifacts, key=lambda art: art['power'], reverse=True))


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """ Filter mages by power """
    return list(filter(lambda mag: mag['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """ Transform spell names """
    return list(map(lambda spe: f"* {spe} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """ Calculate statistics """
    max_power: int = max(mages, key=lambda ma: ma['power'])
    min_power: int = min(mages, key=lambda ma: ma['power'])
    avg_power: float = round(
            sum(map(lambda ma: ma['power'], mages)) / len(mages), 2)

    return {
            'max_power': max_power,
            'min_power': min_power,
            'avg_power': avg_power
            }


if __name__ == '__main__':
    artifacts = [
        {'name': 'Light Prism', 'power': 84, 'type': 'relic'},
        {'name': 'Wind Cloak', 'power': 91, 'type': 'armor'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'weapon'},
        {'name': 'Crystal Orb', 'power': 85, 'type': 'relic'},
        {'name': 'Earth Shield', 'power': 100, 'type': 'relic'}
        ]
    mages = [
        {'name': 'Sage', 'power': 63, 'element': 'ice'},
        {'name': 'Jordan', 'power': 71, 'element': 'lightning'},
        {'name': 'Kai', 'power': 84, 'element': 'ice'},
        {'name': 'Storm', 'power': 77, 'element': 'water'},
        {'name': 'Nova', 'power': 72, 'element': 'wind'}
    ]
    spells = ['fireball', 'heal', 'shield']

    try:
        print("Testing artifact sorter...")
        sorted_artifacts = artifact_sorter(artifacts)
        print(
                f"{sorted_artifacts[0]['name']}"
                " ({sorted_artifacts[0]['power']}"
                " power) comes before "
                f"{sorted_artifacts[1]['name']}"
                " ({sorted_artifacts[1]['power']}"
                " power)")

        print("\nTesting power filter...")
        filtered = power_filter(mages, 72)
        print(f"Mages with power >= 72: {[m['name'] for m in filtered]}")

        print("\nTesting spell transformer...")
        for spell in spell_transformer(spells):
            print(spell, end=' ')

        print("\n\nTesting mage stats...")
        stats = mage_stats(mages)
        print(stats)
    except Exception as e:
        print(f"Error: {str(e)}")
