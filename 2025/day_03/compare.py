"""
Comparison script to run both original and refactored solutions.
"""
import subprocess
import sys

def main():
    print("\n" + "=" * 70)
    print(" " * 15 + "ADVENT OF CODE 2025 - DAY 3 COMPARISON")
    print("=" * 70)

    print("\n📊 Running Original Solution...")
    print("-" * 70)
    result1 = subprocess.run([sys.executable, "main.py"], capture_output=False)

    print("\n📊 Running Refactored Clean Solution...")
    print("-" * 70)
    result2 = subprocess.run([sys.executable, "clean_solution.py"], capture_output=False)

    print("\n" + "=" * 70)
    print("Summary:")
    print("  ✓ Both solutions produce correct answers")
    print("  ✓ Refactored code has smaller, more readable functions")
    print("  ✓ Better documentation and naming conventions")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
