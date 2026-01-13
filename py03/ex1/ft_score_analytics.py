#!/usr/bin/env python3

import sys
"""
Create custom plant alerts, and keep your digital
greenhouse thriving even when things go wrong.
"""


def ft_score_analytics(av):
    """
    Build a simple command interpreter that shows you’ve mastered the art
    of receiving external data.
    """
    print("=== Player Score Analytics ===")
    if (len(av) == 1):
        print("No scores provided.", end="")
        print(f"Usage: python3 {av[0]} <score1> <score2> ...")
        return
    count = 0
    table = []
    for nbr in av:
        if (count != 0):
            try:
                table.append(int(nbr))
            except Exception as e:
                print(f"Error: {e}")
        count += 1
    print(f"Scores processed: {table}")
    print(f"Total players: {count - 1}")
    print(f"Total score: {sum(table)}")
    print(f"Average score: {sum(table) / len(table)}")
    print(f"High score: {max(table)}")
    print(f"Low score: {min(table)}")
    print(f"Score range: {max(table) - min(table)}")


# This line means: "If someone runs this file directly, call main()"
if __name__ == "__main__":
    ft_score_analytics(sys.argv)
