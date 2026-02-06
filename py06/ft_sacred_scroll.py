import alchemy.elements
import alchemy

"""
here when you can see the art of the __init file
"""
fire = alchemy.elements.create_fire()
water = alchemy.elements.create_water()
earth = alchemy.elements.create_earth()
air = alchemy.elements.create_air()


print("=== Sacred Scroll Mastery ===")
print("\nTesting direct module access:")
print(f"alchemy.elements.create_fire(): {fire}")
print(f"alchemy.elements.create_water(): {water}")
print(f"alchemy.elements.create_earth(): {earth}")
print(f"alchemy.elements.create_air(): {air}")
print()

print("Testing package-level access (controlled by __init__.py):")

print("\nTesting direct module access:")
print(f"alchemy.elements.create_fire(): {alchemy.create_fire()}")
print(f"alchemy.elements.create_water(): {alchemy.create_water()}")
try:
    print(f"alchemy.elements.create_earth(): {alchemy.create_earth()}")
    print(f"alchemy.elements.create_air(): {alchemy.create_air()}")
except: # noqa
    print("alchemy.create_earth(): AttributeError - not exposed")
    print("alchemy.create_air(): AttributeError - not exposed")

print("\nPackage metadata:")
print(alchemy.__version__)
print(alchemy.__author__)
