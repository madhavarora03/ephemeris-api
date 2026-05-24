from pathlib import Path

import swisseph as swe

from app.core.config import config
from app.core.ephe_loader import download_ephe
from app.core.ephe_manifest import FILES


def is_ephe_ready(path: Path) -> bool:
    return all((path / file.filename).exists() for file in FILES)


def init_engine(force_download: bool = False) -> Path:
    """
    Initialize Ephemeris Engine.

    - Ensures ephemeris data exists
    - Downloads missing data if required
    - Configures Swiss Ephemeris runtime
    """

    path = config.ephe_path
    path.mkdir(parents=True, exist_ok=True)

    if force_download or not is_ephe_ready(path):
        download_ephe(path, force=force_download)

    # safety check after download
    if not is_ephe_ready(path):
        raise RuntimeError("Ephemeris initialization failed: missing files")

    swe.set_ephe_path(str(path))

    return path
