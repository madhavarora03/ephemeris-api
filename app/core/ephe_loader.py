import urllib.request
from pathlib import Path

from app.core.ephe_manifest import BASE_URL, FILES


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


def download_ephe(target_dir: Path, force: bool = False) -> None:
    """Download all required ephemeris files to target directory."""
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading Swiss Ephemeris files to: {target_dir.resolve()}\n")

    success = 0
    skipped = 0
    failed = 0

    for file in FILES:
        filename, description = file.filename, file.description
        dest = target_dir / filename
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
        raise RuntimeError(
            f"Ephemeris download failed. "
            f"{failed} file(s) could not be downloaded. "
            f"System initialization aborted."
        )
