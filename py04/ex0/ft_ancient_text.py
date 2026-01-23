import sys
"""
Mission 0: Ancient Text Recovery - Retrieve data from old storage units
=======================================================================
"""

print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
file_name = "ancient_fragment.txt"
print(f"Accessing Storage Vault: {file_name}")

try:
    o_file = open(file_name, 'r')
    print("Connection established...")
    data = o_file.read()
    print("\nRECOVERED DATA:")
    print(data)
    o_file.close()
    print("\nData recovery complete. Storage unit disconnected.")

except: # noqa
    print("ERROR: Storage not found. Run data generator first.")
