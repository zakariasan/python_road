"""
Mission 3: Vault Security - Implement failsafe storage procedu
=============================================================
"""
print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===")
print()
print("Initiating secure vault access...")
print("Vault connection established with failsafe protocols")
print("\nSECURE EXTRACTION:")

with open("classified_data.txt", 'r') as o_file:
    data = o_file.read()
    print(data)
print("\nSECURE PRESERVATION:")

with open("security_log.txt", 'w') as o_file:
    o_file.write("New security protocols archived\n")
    print("[CLASSIFIED] New security protocols archived")

print("Vault automatically sealed upon completion\n")
print("All vault operations completed with maximum security.")
