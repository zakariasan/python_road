import sys
"""
    Build a simple command interpreter that shows you’ve mastered the art
    of receiving external data.

    Level 1: Score Cruncher - Master lists by analyzing player scores
"""

av = sys.argv
print("=== Player Score Analytics ===")

if (len(av) == 1):
    print("No scores provided. ", end="")
    print(f"Usage: python3 {av[0]} <score1> <score2> ...")
else:
    table = []
    try:
        for nbr in av[1:]:
            table += [int(nbr)]
        print(f"Scores processed: {table}")
        print(f"Total players: {len(table)}")
        print(f"Total score: {sum(table)}")
        print(f"Average score: {sum(table) / len(table)}")
        print(f"High score: {max(table)}")
        print(f"Low score: {min(table)}")
        print(f"Score range: {max(table) - min(table)}")
    except: # noqa
        print(f"Error: invalid literal for int() with base 10: '{nbr}'")
