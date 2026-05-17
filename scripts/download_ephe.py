#!/usr/bin/env python3
"""
Download Swiss Ephemeris data files required for birth chart calculations.
Files are downloaded from the official Swiss Ephemeris GitHub repository.

Usage:
    uv run python scripts/download_ephe.py
    uv run python scripts/download_ephe.py --target ./custom/path
"""

import argparse
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://github.com/aloistr/swisseph/raw/master/ephe"

# Minimum files required for Kundali generation (9 planets)
# sepl = planets (Sun, Mars, Mercury, Jupiter, Venus, Saturn, Uranus, Neptune, Pluto)
# semo = Moon (separate file, larger — Moon moves fast, needs more data points)
# seas = main asteroids (Ceres, Pallas, Juno, Vesta, Chiron, Pholus) — optional but good to have
FILES = [
    ("sepl_18.se1", "Planets (1800-2400 AD)"),
    ("semo_18.se1", "Moon (1800-2400 AD)"),
    ("seas_18.se1", "Main asteroids (1800-2400 AD)"),
]


def download_file(url: str, dest: Path) -> None:
    """Download a single file with progress indication."""

    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 // total_size)
            bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
            print(f"\r  [{bar}] {percent}%", end="", flush=True)

    urllib.request.urlretrieve(url, dest, reporthook=progress)
    print()  # newline after progress bar


def download_ephe(target_dir: str = "./ephe", force: bool = False) -> None:
    """Download all required ephemeris files to target directory."""
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)

    print(f"Downloading Swiss Ephemeris files to: {target.resolve()}\n")

    success = 0
    skipped = 0
    failed = 0

    for filename, description in FILES:
        dest = target / filename
        url = f"{BASE_URL}/{filename}"

        print(f"→ {filename} ({description})")

        if dest.exists() and not force:
            print("  already exists, skipping (use --force to re-download)")
            skipped += 1
            continue

        try:
            download_file(url, dest)
            size_kb = dest.stat().st_size // 1024
            print(f"  ✓ downloaded ({size_kb} KB)")
            success += 1
        except Exception as e:
            print(f"  ✗ failed: {e}")
            if dest.exists():
                dest.unlink()  # remove partial download
            failed += 1

        print()

    print("─" * 40)
    print(f"Done: {success} downloaded, {skipped} skipped, {failed} failed")

    if failed > 0:
        print("\nSome files failed to download.")
        print("Check your internet connection and try again.")
        sys.exit(1)

    if success > 0:
        print("\nSet ephemeris path in your code:")
        print(f'  swe.set_ephe_path("{target.resolve()}")')


def main():
    parser = argparse.ArgumentParser(description="Download Swiss Ephemeris data files")
    parser.add_argument(
        "--target",
        default="./ephe",
        help="Target directory for ephemeris files (default: ./ephe)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download files even if they already exist",
    )
    args = parser.parse_args()
    download_ephe(target_dir=args.target, force=args.force)


if __name__ == "__main__":
    main()
