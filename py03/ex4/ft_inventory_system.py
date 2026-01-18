import sys

# Create inventory dictionary from command line arguments
# Format: item:quantity (e.g., sword:1 potion:5)
inventory = dict()

# Parse arguments
for arg in sys.argv:
    if ':' in arg:
        parts = arg.split(':')
        item_name = parts[0]
        quantity = int(parts[1])
        inventory.update({item_name: quantity})

print("=== Inventory System Analysis ===")

# Calculate total items
total_items = 0
for quantity in inventory.values():
    total_items = total_items + quantity

print(f"Total items in inventory: {total_items}")
print(f"Unique item types: {len(inventory)}")

print("\n=== Current Inventory ===")

# Create list of items for sorting
sorted_items = []
for item, quantity in inventory.items():
    sorted_items.append((item, quantity))

# Manual bubble sort (descending by quantity)
swapped = True
while swapped:
    swapped = False
    i = 0
    for item1, qty1 in sorted_items:
        try:
            item2, qty2 = sorted_items[i + 1]
            if qty1 < qty2:
                sorted_items[i] = (item2, qty2)
                sorted_items[i + 1] = (item1, qty1)
                swapped = True
            i = i + 1
        except:
            break

# Display sorted inventory with percentages
for item, quantity in sorted_items:
    percentage = (quantity / total_items) * 100
    unit_text = "unit" if quantity == 1 else "units"
    print(f"{item}: {quantity} {unit_text} ({percentage:.1f}%)")

print("\n=== Inventory Statistics ===")

# Find most and least abundant
most_abundant_item = ""
most_abundant_qty = 0
least_abundant_item = ""
least_abundant_qty = total_items + 1

for item, quantity in inventory.items():
    if quantity > most_abundant_qty:
        most_abundant_qty = quantity
        most_abundant_item = item
    if quantity < least_abundant_qty:
        least_abundant_qty = quantity
        least_abundant_item = item

print(f"Most abundant: {most_abundant_item} ({most_abundant_qty} units)")
print(f"Least abundant: {least_abundant_item} ({least_abundant_qty} unit{'s' if least_abundant_qty > 1 else ''})")

print("\n=== Item Categories ===")

# Categorize items: Moderate (>= 5), Scarce (< 5)
moderate = dict()
scarce = dict()

for item, quantity in inventory.items():
    if quantity >= 5:
        moderate.update({item: quantity})
    else:
        scarce.update({item: quantity})

print(f"Moderate: {moderate}")
print(f"Scarce: {scarce}")

print("\n=== Management Suggestions ===")

# Items that need restocking (quantity <= 2)
restock_needed = []
for item, quantity in inventory.items():
    if quantity <= 2:
        restock_needed.append(item)

print(f"Restock needed: {restock_needed}")

print("\n=== Dictionary Properties Demo ===")

# Convert keys and values to lists for display
keys_list = []
for key in inventory.keys():
    keys_list.append(key)

values_list = []
for value in inventory.values():
    values_list.append(value)

print(f"Dictionary keys: {keys_list}")
print(f"Dictionary values: {values_list}")

# Sample lookup using get()
sample_item = 'sword'
has_item = inventory.get(sample_item) is not None
print(f"Sample lookup - '{sample_item}' in inventory: {has_item}")
