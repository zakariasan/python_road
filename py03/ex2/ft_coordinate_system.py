import math

"""
Let's deep dive into tuples and coordinat Creations

Level 2: Position Tracker - Use tuples to navigate game worlds
"""

print("=== Game Coordinate System ===\n")

position = (10, 20, 5)
print(f"Position created: {position}")

origin = (0, 0, 0)
x1, y1, z1 = origin
x2, y2, z2 = position
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
print(f"Distance between {origin} and {position}: {distance:.2f}\n")

coord_string = "3,4,0"
print(f"Parsing coordinates: \"{coord_string}\"")

parts = coord_string.split(',')
try:
    x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
    parsed_pos = (x, y, z)
except: # noqa
    try:
        x, y = int(parts[0]), int(parts[1])
        parsed_pos = (x, y, 0)
    except: # noqa
        parsed_pos = (0, 0, 0)

print(f"Parsed position: {parsed_pos}")

x2, y2, z2 = parsed_pos
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
print(f"Distance between {origin} and {parsed_pos}: {distance}\n")

invalid_string = "abc,def,ghi"
print(f"Parsing invalid coordinates: \"{invalid_string}\"")
try:
    parts = invalid_string.split(',')
    x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
    invalid_pos = (x, y, z)
except Exception as e:
    print(f"Error parsing coordinates: {e}")
    print(f"Error details - Type: {type(e).__name__}, Args: {e.args}\n")

print("Unpacking demonstration:")
x, y, z = parsed_pos
print(f"Player at x={x}, y={y}, z={z}")
print(f"Coordinates: X={x}, Y={y}, Z={z}")
