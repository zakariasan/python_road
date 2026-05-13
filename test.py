def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"

    d = 0
    number = number.upper()
    for item in number:
        if item not in digits:
            return 'ERROR'
        v = digits.index(item)
        if v >= from_base:
            return 'ERROR'
        d = d * from_base + v
    if d == 0:
        return '0'
    res = 0
    while d > 0:
        res = digits[d % to_base] + res
        d //= to_base
    return res


def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    for item in matrix:
        item.reverse()
    return matrix


def echo_validator(text: str) -> bool:
    if str == '':
        return False
    lower_text = text.lower().split()
    lower_text = ''.join(lower_text)
    lower_rev = ''.join(reversed(lower_text))

    if len(lower_rev) != len(lower_text):
        return False
    else:
        for i in range(len(lower_rev)):
            if lower_text[i] != lower_rev[i]:
                return False
    return True


def whisper_cipher(text: str, shift: int) -> str:
    stt = ''
    if text == '':
        return ""
    for item in text:
        if (item.isalpha()):
            start = ord('A') if item.isupper() else ord('a')
            nbr = (ord(item) - start + shift) % 26
            stt += chr(nbr + start)
        else:
            stt += item
    return stt


def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    res = list1 + list2
    res.sort()
    return res


print(shadow_merge([1, 3, 5], [2, 4, 6]))
print(shadow_merge([1, 2, 3], [4, 5, 6]))
print(shadow_merge([1], [2, 3, 4]))
print(shadow_merge([1, 1, 2], [1, 3, 3]))
