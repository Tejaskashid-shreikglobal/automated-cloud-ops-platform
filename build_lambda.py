
"""Build a clean AWS Lambda deployment ZIP locally."""

from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
BUILD = ROOT / "build" / "lambda"
ZIP_FILE = ROOT / "terraform" / "lambda_package.zip"

APP_FILES = (
    "lambda_handler.py",
    "incident_engine.py",
)


def main():
    # Start with a clean build directory.
    if BUILD.exists():
        shutil.rmtree(BUILD)

    BUILD.mkdir(parents=True)

    # Copy only the required application modules.
    for filename in APP_FILES:
        source = SRC / filename
        if not source.is_file():
            raise FileNotFoundError(source)

        shutil.copy2(source, BUILD / filename)

    # Install runtime dependencies into the package.
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--target",
            str(BUILD),
            "--no-compile",
            "--no-warn-script-location",
            "boto3",
        ],
        check=True,
    )

    # Remove unnecessary caches and command-line scripts.
    for path in BUILD.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)

    for path in BUILD.rglob("*.pyc"):
        if path.is_file():
            path.unlink()

    bin_dir = BUILD / "bin"
    if bin_dir.exists():
        shutil.rmtree(bin_dir)

    ZIP_FILE.parent.mkdir(parents=True, exist_ok=True)

    if ZIP_FILE.exists():
        ZIP_FILE.unlink()

    archive_base = str(ZIP_FILE.with_suffix(""))
    shutil.make_archive(archive_base, "zip", BUILD)

    # Verify the essential files are at the ZIP root.
    with zipfile.ZipFile(ZIP_FILE, "r") as archive:
        names = set(archive.namelist())

    required = {
        "lambda_handler.py",
        "incident_engine.py",
        "boto3/__init__.py",
    }

    missing = required - names
    if missing:
        raise RuntimeError(
            f"Package is missing required files: {sorted(missing)}"
        )

    print("PACKAGE:", ZIP_FILE)
    print("PACKAGE EXISTS:", ZIP_FILE.exists())
    print("PACKAGE SIZE:", ZIP_FILE.stat().st_size, "bytes")
    print("REQUIRED FILES: OK")


if __name__ == "__main__":
    main()
