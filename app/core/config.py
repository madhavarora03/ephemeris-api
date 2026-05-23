import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    ephe_path: Path = Path(os.getenv("EPHE_PATH", "./ephe")).resolve()


config = Config()
