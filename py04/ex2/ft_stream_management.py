import sys
"""
Mission 2: Stream Management - Master the three data channels
=============================================================
"""
print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
arch_id = input("Input Stream active. Enter archivist ID: ")
status_report = input("Input Stream active. Enter status report: ")
print()
sys.stdout.write(
        f"[STANDARD] Archive status from {arch_id}: {status_report}\n")

sys.stderr.write(
        "[ALERT] System diagnostic: Communication channels verified\n"
        )

sys.stdout.write("[STANDARD] Data transmission complete\n")
print()
print("Three-channel communication test successful.")
