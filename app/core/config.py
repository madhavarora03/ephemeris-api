import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    ephe_path: str = os.getenv("EPHE_PATH", "./ephe")


config = Config()
