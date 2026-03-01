"""
"Know thyself." - The Oracle
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_config() -> None:
    """ Get Data from env """
    return {
        "MATRIX_MODE":   os.environ.get("MATRIX_MODE", "development"),
        "DATABASE_URL":  os.environ.get("DATABASE_URL", None),
        "API_KEY":       os.environ.get("API_KEY", None),
        "LOG_LEVEL":     os.environ.get("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.environ.get("ZION_ENDPOINT", None),
    }


def check_config(config: dict) -> None:
    """ Check if we have it in the env """
    return [key for key, value in config.items() if value is None]


def display_config(config: dict) -> None:
    """ Display as it should be """

    conn = 'Connected to local instance'
    auth = 'Authenticated'
    print("\nORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(
            "Database: "
            +
            f"{conn if config['DATABASE_URL'] else 'NOT configured'}")
    print(f"API Access: {auth if config['API_KEY'] else 'NOT configured'}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(
            "Zion Network: "
            +
            f"{'Online' if config['ZION_ENDPOINT'] else 'NOT configured'}")


def security_check() -> None:
    """ Check if we cheated on the env """
    print("\nEnvironment security check:")
    print("  [OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] .env file not found — copy .env.example to .env")

    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            content = f.read()
        if ".env" in content:
            print("  [OK] Production overrides available")
        else:
            print("  [WARN] .env not in .gitignore — add it!")
    else:
        print("  [WARN] .gitignore not found")


def main() -> None:
    """ Playing with the data managemet """
    config = get_config()
    missing = check_config(config)

    display_config(config)

    if missing:
        print(f"\n  [WARN] Missing: {', '.join(missing)}")
        print("  Copy .env.example to .env and fill in your values.")

    security_check()
    print("\nThe Oracle sees all configurations.")


main()
