"""
Ephemeris dataset manifest.

Defines required Swiss Ephemeris files and download sources.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EphemerisFile:
    filename: str
    description: str


BASE_URL = "https://github.com/aloistr/swisseph/raw/master/ephe"

FILES = [
    EphemerisFile(filename="sepl_18.se1", description="Planets (1800-2400 AD)"),
    EphemerisFile(filename="semo_18.se1", description="Moon (1800-2400 AD)"),
    EphemerisFile(filename="seas_18.se1", description="Main asteroids (1800-2400 AD)"),
]
