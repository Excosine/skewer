"""Start all services in parallel, output to logs/ directory."""

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"

SERVICES = {
    "backend": {
        "cwd": "backend",
        "args": ["uv", "run", "python", "server.py"],
        "shell": False,
        "url": "http://localhost:8000",
    },
    "admin": {
        "cwd": "admin",
        "args": ["npm", "run", "dev"],
        "shell": True,
        "url": "http://localhost:3000",
    },
    "waiter": {
        "cwd": "waiter",
        "args": ["npm", "run", "dev"],
        "shell": True,
        "url": "http://localhost:5173",
    },
}

procs: dict[str, subprocess.Popen] = {}


def setup():
    for svc in SERVICES:
        d = LOG_DIR / svc
        d.mkdir(parents=True, exist_ok=True)


def start_svc(name: str):
    cfg = SERVICES[name]
    out = open(LOG_DIR / name / "output.log", "w")
    err = open(LOG_DIR / name / "error.log", "w")
    print(f"  {name:8s} -> logs/{name}/")

    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)

    p = subprocess.Popen(
        cfg["args"],
        cwd=str(ROOT / cfg["cwd"]),
        stdout=out,
        stderr=err,
        shell=cfg.get("shell", False),
        env=env,
    )
    procs[name] = p

    # Close in parent - child process keeps writing
    out.close()
    err.close()


def cleanup():
    print("\nStopping all services...")
    for name, p in list(procs.items()):
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
            print(f"  Stopped {name}")


def main():
    parser = argparse.ArgumentParser(description="Start dev services")
    parser.add_argument("--admin", action="store_true")
    parser.add_argument("--waiter", action="store_true")
    parser.add_argument("--backend", action="store_true")
    args = parser.parse_args()

    run_all = not (args.admin or args.waiter or args.backend)
    setup()

    print("=== Starting services ===")
    for name in ["backend", "admin", "waiter"]:
        if run_all or getattr(args, name):
            start_svc(name)

    print("=== All services started. Press Ctrl+C to stop ===\n")
    for name in ["backend", "admin", "waiter"]:
        if run_all or getattr(args, name):
            cfg = SERVICES[name]
            print(f"  {name:8s} {cfg['url']}")
    print()

    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))

    try:
        for p in procs.values():
            p.wait()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


if __name__ == "__main__":
    main()
