import os
from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_data_dir

APP_NAME = "EphemerisEngine"


@dataclass(frozen=True)
class Config:
    ephe_path: Path


def load_config() -> Config:
    env_path = os.getenv("EPHE_PATH")

    if env_path:
        return Config(ephe_path=Path(env_path))

    return Config(ephe_path=Path(user_data_dir(APP_NAME)) / "ephe")


config = load_config()
