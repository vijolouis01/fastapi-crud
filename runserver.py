import os
import subprocess
import sys


def _base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("HOST", "0.0.0.0")
    env.setdefault("PORT", "8000")
    return env


def dev() -> None:
    env = _base_env()
    subprocess.run(
        [sys.executable, "-m", "fastapi", "dev", "main.py"],
        env=env,
        check=False,
    )


def pro() -> None:
    env = _base_env()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            env["HOST"],
            "--port",
            env["PORT"],
        ],
        env=env,
        check=False,
    )


if __name__ == "__main__":
    dev()
