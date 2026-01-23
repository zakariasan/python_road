import sys
"""
Level 4: Inventory Master - Build complex systems with dictionaries
"""

my_dict = dict()

for arg in sys.argv:
    if ':' in arg:
        try:
            parts = arg.split(':')
            item_name = parts[0]
            quantity = int(parts[1])
            my_dict[item_name] = quantity
        except: # noqa
            print("Error: invalid literal for int()", end="")
            print(f" with base 10: '{parts[1]}' ")

print("=== Inventory System Analysis ===")

total_items = 0
for quantity in my_dict.values():
    total_items += quantity

print(f"Total items in my_dict: {total_items}")
print(f"Unique item types: {len(my_dict)}")

print("\n=== Current Inventory ===")

new_dict = dict()
for g_item, g_quantity in my_dict.items():
    m_key = None
    m_value = 0
    for item, quantity in my_dict.items():
        if item not in new_dict and quantity > m_value:
            m_key = item
            m_value = quantity
    new_dict[m_key] = m_value

for item, quantity in new_dict.items():
    percentage = (quantity / total_items) * 100
    unit_text = "unit" if quantity == 1 else "units"
    print(f"{item}: {quantity} {unit_text} ({percentage:.1f}%)")

print("\n=== Inventory Statistics ===")

most_item = ""
most_qty = 0
least_item = ""
least_qty = total_items + 1

for item, quantity in my_dict.items():
    if quantity > most_qty:
        most_qty = quantity
        most_item = item
    if quantity < least_qty:
        least_qty = quantity
        least_item = item

txt = "unit" if least_qty == 1 else "units"
print(f"Most abundant: {most_item} ({most_qty} units)")
print(f"Least abundant: {least_item} ({least_qty} {txt})")

print("\n=== Item Categories ===")

moderate = dict()
scarce = dict()

for item, quantity in my_dict.items():
    if quantity >= 5:
        moderate[item] = quantity
    else:
        scarce[item] = quantity

print(f"Moderate: {moderate}")
print(f"Scarce: {scarce}")

print("\n=== Management Suggestions ===")

restor = []
for item, quantity in my_dict.items():
    if quantity < 2:
        restor += [item]

print(f"Restock needed: {restor}")

print("\n=== Dictionary Properties Demo ===")

keys_list = []
for key in my_dict.keys():
    keys_list += [key]

values_list = []
for value in my_dict.values():
    values_list += [value]

print(f"Dictionary keys: {keys_list}")
print(f"Dictionary values: {values_list}")

sample_item = 'sword'
has_item = my_dict.get(sample_item) is not None
print(f"Sample lookup - '{sample_item}' in my_dict: {has_item}")
