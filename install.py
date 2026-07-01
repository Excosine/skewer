"""One-click install dependencies for all services."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

steps = [
    ("backend", ["uv", "sync"], ROOT / "backend"),
    ("admin",   ["npm", "install"], ROOT / "admin"),
    ("waiter",  ["npm", "install"], ROOT / "waiter"),
]

def run(name: str, args: list[str], cwd: Path):
    print(f"\n{'='*50}")
    print(f"  Installing {name}...")
    print(f"{'='*50}")
    # npm needs shell on Windows, uv doesn't
    use_shell = sys.platform == "win32" and name != "backend"
    r = subprocess.run(args, cwd=str(cwd), shell=use_shell)
    if r.returncode != 0:
        print(f"  {name} install FAILED")
        return False
    print(f"  {name} install DONE")
    return True

def main():
    ok = True
    for name, args, cwd in steps:
        if not run(name, args, cwd):
            ok = False
    if ok:
        print(f"\n{'='*50}")
        print("  All dependencies installed.")
        print(f"{'='*50}")
    else:
        print("\nSome installs failed, check output above.")

if __name__ == "__main__":
    main()
