def string_permutation_checker(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    new_s1 = []
    new_s2 = []
    for i in s1:
        new_s1.append(i)
    for i in s2:
        new_s2.append(i)
    new_s1.sort()
    new_s2.sort()
    if new_s1 == new_s2:
        return True
    return False


def cryptic_sorter(strings: list[str]) -> list[str]:
    """
    Sorts a list of strings based on:
    1. Length (shortest first)
    2. Case-insensitive ASCII order
    3. Number of vowels (ascending)
    """

    def sorting_key(s):
        # 1. Primary: Length
        length = len(s)

        # 2. Secondary: Case-insensitive ASCII order
        case_insensitive = s.lower()

        # 3. Tertiary: Number of vowels (ascending)
        vowels = "aeiouAEIOU"
        vowel_count = sum(1 for char in s if char in vowels)

        # Return tuple for sorting: (primary, secondary, tertiary)
        return (length, case_insensitive, vowel_count)

    # Use sorted() which is stable, maintaining order for equal elements
    return sorted(strings, key=sorting_key)
