"""
"I need guns. Lots of guns." - Neo
"""
import sys
import importlib.util


def check_dependencies() -> None:
    """ Check if there is life """
    REQUIRED = {
        "pandas":     "Data manipulation",
        "numpy":      "Numerical computations",
        "matplotlib": "Visualization",
        "requests":   "Network access",
    }
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    missing = []

    for package, description in REQUIRED.items():
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"  [MISSING] {package} - {description} NOT found")
            missing.append(package)
        else:
            mod = importlib.import_module(package)
            version = getattr(mod, "__version__", "unknown")
            print(f"  [OK] {package} ({version}) - {description} ready")
    return missing


def show_install_instructions() -> None:
    """ show me how to make it """
    print("\nMissing dependencies detected!")
    print("\nTo install with pip:")
    print("  pip install -r requirements.txt")
    print("\nTo install with Poetry:")
    print("  poetry install")
    print("\nThen run this program again.")


def run_analysis():
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")
    print("Generating visualization...")

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.text(
        0.5, 0.5,
        "1337",
        color="lime",
        fontsize=200,
        fontweight="bold",
        ha="center",
        va="center",
        transform=ax.transAxes
    )
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    """need guns. Lots of guns."""

    missing = check_dependencies()
    if missing:
        show_install_instructions()
        sys.exit(1)

    run_analysis()


main()
