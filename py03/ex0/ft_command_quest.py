import sys
"""
Build a simple command interpreter that shows you’ve mastered the art
of receiving external data.
"""

print("=== Command Quest ===")
av = sys.argv
size = len(av)
if (size == 1):
    print(f"No arguments provided!\nProgram name: {av[0]}")
else:
    count = 1
    print(f"Program name: {av[0]}\nArguments received: {size - 1}")
    for arg in av[1:]:
        print(f"Argument {count}: {arg}")
        count += 1
print(f"Total arguments: {len(av)}")
