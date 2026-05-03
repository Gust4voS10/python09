try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:
    print("use pip install pydantic")
    exit(1)


from datetime import datetime
from typing import Optional

class Station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime = datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None)


def main() -> None:
    print("space Station Data Validation")
    print("=============================")
    s1: Station = Station(station_id="ISS67",
                          name="Interestellar",
                          crew_size=6,
                          power_level=67.67,
                          oxygen_level=4.20,
                          last_maintenance="2023-10-25T14:30:00",
                          notes="Nada")
    print("Valid station created:")
    print(f"ID: {s1.station_id}")
    print(f"Name: {s1.name}")
    print(f"Crew: {s1.crew_size} people")
    print(f"Power: {s1.power_level}%")
    print(f"Oxygen: {s1.oxygen_level}%")
    if (s1.is_operational):
        print("Status: Operational")
    else:
        print("Status: Inactive")
    if (s1.notes):
        print(f"Notes: {s1.notes}")
    print("\n=============================")
    try:
        s2: Station = Station(station_id="ISS67",
                              name="Interestellar",
                              crew_size=30,
                              power_level=67.67,
                              oxygen_level=4.20,
                              last_maintenance="2005-11-07T18:30:00")
        print(f"ID: {s2.station_id}")
        print(f"Name: {s2.name}")
        print(f"Crew: {s2.crew_size} people")
        print(f"Power: {s2.power_level}%")
        print(f"Oxygen: {s2.oxygen_level}%")
        if (s2.is_operational):
            print("Status: Operational")
        else:
            print("Status: Inactive")
        if (s2.notes):
            print(f"Notes: {s2.notes}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()