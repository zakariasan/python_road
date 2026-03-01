"""
Space Stations: Basic data validation fundamentals
"""
from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    """
    The Cosmic Data Observatory monitors hundreds of space stations
    across the galaxy.
    """
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    """The Cosmic Data Observatory monitors hundreds of
    space stations across the galaxy."""
    print("Space Station Data Validation")
    print("========================================")

    station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size="6",
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-01-15",
            is_operational=True,
            notes="All safe.",
            )

    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print("Status: Operational")

    print("\n========================================")
    print("Expected validation error:")

    try:
        bad_station = SpaceStation( # noqa
            station_id="ISS001",
            name="International Space Station",
            crew_size=26,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-01-15",
            is_operational=True,
            notes="not safe sys.",
            )
    except Exception as e:
        err = e.errors()[0]['msg']
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
