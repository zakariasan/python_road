def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return arr
    if k % len(arr) == 0:
        return arr
    return arr[-k:] + arr[:-k]


def pattern_tracker(text: str) -> int:
    cnt = 0
    i = 0
    for item in text:
        if i < len(text) - 1 and item.isdigit():
            try:
                if int(item) + 1 == int(text[i + 1]):
                    cnt += 1
            except: # toi
                pass
        i += 1

    return cnt


def bracket_validator(s: str) -> bool:
    open_b = {')': '(', ']': '[', '}': '{'}
    stack = []
    for item in s:
        if item in open_b.values():
            stack.append(item)
        if item in open_b:
            v = stack.pop() if stack else '0'
            if open_b[item] != v:
                return False
    if len(stack) >= 1:
        return False
    return True


def string_sculptor(text: str) -> str:
    po = 0
    st = ''
    for item in text:
        if item.isalpha():
            if po % 2 == 0:
                st += item.lower()
            else:
                st += item.upper()
            po += 1
        elif item.isspace():
            po += 1
            st += item
        else:
            st += item
    return st

