"""
This is your last chance. After this, there is no going back. You
take the blue pill; the story ends, you wake up in your bed and
believe whatever you want to believe. You take the red pill; you
stay in Wonderland, and I show you how deep the rabbit hole goes.

"""
import sys
import os
import site


def main() -> None:
    """
    What is real? How do you define (real)?
    """
    if (sys.prefix != sys.base_prefix or
            os.environ.get('VIRTUAL_ENV') is not None):

        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting the global system.")
        print()
        print(f"Package installation path:\n{site.getsitepackages()[0]}")
    else:
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print()
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\nScripts\nactivate       # On Windows")
        print()
        print("Then run this program again.")


main()
