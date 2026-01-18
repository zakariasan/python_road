print("=== Achievement Tracker System ===\n")

# Create player achievement sets directly
alice = {'first_kill', 'level_10', 'treasure_hunter', 'speed_demon'}
bob = {'first_kill', 'level_10', 'boss_slayer', 'collector'}
charlie = {
        'level_10',
        'treasure_hunter',
        'boss_slayer',
        'speed_demon',
        'perfectionist'
        }

print(f"Player alice achievements: {alice}")
print(f"Player bob achievements: {bob}")
print(f"Player charlie achievements: {charlie}")

print("\n=== Achievement Analytics ===")

# UNION: Combines all unique items from both sets (A ∪ B)
# Think: "Everything that Alice OR Bob OR Charlie has"
all_achievements = alice.union(bob).union(charlie)
print(f"All unique achievements: {all_achievements}")
print(f"Total unique achievements: {len(all_achievements)}\n")

# INTERSECTION: Only items that exist in ALL sets (A ∩ B)
# Think: "What do Alice AND Bob AND Charlie ALL have?"
common_all = alice.intersection(bob).intersection(charlie)
print(f"Common to all players: {common_all}")

# DIFFERENCE: Items in first set but NOT in second set (A - B)
# Think: "What does Alice have that Bob doesn't?"
alice_only = alice.difference(bob).difference(charlie)
bob_only = bob.difference(alice).difference(charlie)
charlie_only = charlie.difference(alice).difference(bob)
rare = alice_only.union(bob_only).union(charlie_only)
print(f"Rare achievements (1 player): {rare}\n")

# Alice vs Bob comparison
alice_bob_common = alice.intersection(bob)
print(f"Alice vs Bob common: {alice_bob_common}")

alice_unique = alice.difference(bob)
print(f"Alice unique: {alice_unique}")

bob_unique = bob.difference(alice)
print(f"Bob unique: {bob_unique}")
