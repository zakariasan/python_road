# Data Archivist Digital Preservation in the Cyber Archives
# Mission: Implement comprehensive crisis response with error handling

def crisis_handler(filename):
    """
    Crisis handler function for archive operations.
    Implements failsafe protocols with proper error handling.
    
    Args:
        filename: The archive file to access
    """
    print(f"CRISIS ALERT: Attempting access to '{filename}'...")
    
    try:
        # Attempt secure vault access using with statement
        with open(filename, 'r') as archive_file:
            # Read archive contents
            data = archive_file.read().strip()
            
            # Successful recovery
            print(f"SUCCESS: Archive recovered - ``{data}''")
            print("STATUS: Normal operations resumed")
        
    except FileNotFoundError:
        # Handle missing archives
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    
    except PermissionError:
        # Handle security protocol violations
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")
    
    except Exception as e:
        # Handle unexpected system anomalies
        print(f"RESPONSE: Unexpected system anomaly detected - {type(e).__name__}")
        print("STATUS: Crisis handled, diagnostics logged")


# Display system header
print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")

# Test Crisis Scenario 1: Missing archive
crisis_handler("lost_archive.txt")

print()  # Blank line for readability

# Test Crisis Scenario 2: Permission denied (if file exists with restricted access)
crisis_handler("classified_vault.txt")

print()  # Blank line for readability

# Test Crisis Scenario 3: Successful operation
print("ROUTINE ACCESS: Attempting access to 'standard_archive.txt'...")

try:
    with open("standard_archive.txt", 'r') as archive_file:
        data = archive_file.read().strip()
        print(f"SUCCESS: Archive recovered - ``{data}''")
        print("STATUS: Normal operations resumed")

except FileNotFoundError:
    print("RESPONSE: Archive not found in storage matrix")
    print("STATUS: Crisis handled, system stable")

except PermissionError:
    print("RESPONSE: Security protocols deny access")
    print("STATUS: Crisis handled, security maintained")

except Exception as e:
    print(f"RESPONSE: Unexpected system anomaly detected - {type(e).__name__}")
    print("STATUS: Crisis handled, diagnostics logged")

print()  # Blank line before final message

# Final confirmation
print("All crisis scenarios handled successfully. Archives secure.")
