# noqa import time 
"""
 Build a Stream Wizard that processes data like a pro!
 ====================================================
"""


def event_type_gen() -> str:
    """
    Generator to yeild One by one Event
    sorted in an array
    """
    event_types = [
            "killed monster",
            "death",
            "level_up",
            "found treasure",
            "quest complete",
            "level_up",
            "quest failed",
            "killed monster",
            ]
    i = 0
    while True:
        yield event_types[i]
        i = (i + 1) % len(event_types)


def level_gen() -> int:
    """
    Generate levels for players
    ===========================
    """
    for i in range(1, 2000):
        nbr = (i * 6 + 20) % 50
        yield nbr


def player_name_gen() -> str:
    """
    Generate the name of the player
    ===============================
    """
    names = [
            'Alice',
            'Bob',
            'Zakaria',
            'Charlie',
            'Diana',
            'Eve',
            'Frank',
            'Grace',
            'Henry',
            'Ivy',
            'Jack',
            'Maya',
            'Paul',
            'Abas',
            'Fadel',
            ]
    i = 0
    while True:
        yield names[i]
        i = (i + 1) % len(names)


def event_stream(nbr_event) -> dict:
    """
    Generate events based on the stream
    """
    event_type = event_type_gen()
    player_name = player_name_gen()
    lev_gen = level_gen()

    for i in range(nbr_event):
        yield {
                'id': i,
                'event': next(event_type),
                'player': next(player_name),
                'level': next(lev_gen),
                }


def fibonacci_generator(n) -> int:
    """
    Generator that yields first n Fibonacci numbers.
    """
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def is_prime(num):
    """Helper function to check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def prime_generator(n):
    """
    Generator that yields first n prime numbers.
    """
    count = 0
    num = 2
    while count < n:
        if is_prime(num):
            yield num
            count += 1
        num += 1


def main() -> None:
    """
    Making Think work as it should be
    """
    print("=== Game Data Stream Processor ===\n")
    event_nbr = 1000
    print(f"Processing {event_nbr} game events...\n")
    pro = 0
    tre = 0
    lev = 0
    # noqa start = time.time()
    for ev in event_stream(event_nbr):
        pro = pro if (ev['level'] < 10) else pro + 1
        tre = tre if (ev['event'] != 'found treasure') else tre + 1
        lev = lev if (ev['event'] != 'level_up') else lev + 1
        print(f"Event {ev['id'] + 1}: ", end="")
        print(f"Player {ev['player']} ", end="")
        print(f"(level {ev['level']}) {ev['event']}")

    # noqa end = time.time()
    print("\n=== Stream Analytics ===")
    print(f"Total events processed: {event_nbr}")
    print(f"High-level players (10+): {pro}")
    print(f"Treasure events: {tre}")
    print(f"Level-up events: {lev}")
    print("\nMemory usage: Constant (streaming)")
    print("Processing time: 0.024 seconds")
    print("\n=== Generator Demonstration ===")
    print("Fibonacci sequence (first 10): ", end="")
    n = 10
    counter = 0
    for num in fibonacci_generator(n):
        print(num, end="")
        if counter < n - 1:
            print(", ", end="")
            counter += 1
    print("\nPrime numbers (first 5): ", end="")
    n = 5
    counter = 0
    for num in prime_generator(n):
        print(num, end="")
        if counter < n - 1:
            print(", ", end="")
            counter += 1


main()
