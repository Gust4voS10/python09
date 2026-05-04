try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError:
    print("Use pip intall pydantic")
    exit(1)

from datetime import datetime
from enum import Enum


def ft_len(lst: list) -> int:
    count: int = 0
    for _ in lst:
        count += 1
    return (count)


class Rank(Enum):
    commander = 1
    captain = 2
    lieutenant = 3
    officer = 4
    cadet = 5


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=50)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=2, max_length=50)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode='after')
    def validation(self) -> 'SpaceMission':
        if (self.mission_id[0] != 'M'):
            raise ValueError("Invalid Mission ID")
        for crew_member in self.crew:
            if (crew_member.is_active is False):
                raise ValueError(f"{crew_member.name} is inactive")
        valid_crew: bool = False
        for crew_member in self.crew:
            if ((crew_member.rank.name == "commander") or
                    (crew_member.rank.name == "captain")):
                valid_crew = True
        if (valid_crew is False):
            raise ValueError("A mission must have at least one"
                             " Commander or Captain")
        if (self.duration_days > 365):
            for crew_member in self.crew:
                if (crew_member.years_experience < 5):
                    raise ValueError(f"{crew_member.name} is too unexperienced"
                                     " for this mission")
        return (self)


def main() -> None:
    print("=============================")
    crew1: list = [CrewMember(member_id="C2026A",
                              name="Ana Silva",
                              rank=Rank.commander,
                              age=42,
                              specialization="Pilot",
                              years_experience=20),
                   CrewMember(member_id="C2026B",
                              name="Lucas Santos",
                              rank=Rank.captain,
                              age=35,
                              specialization="Systems Engineer",
                              years_experience=12),
                   CrewMember(member_id="C2026C",
                              name="Marta Lima",
                              rank=Rank.officer,
                              age=29,
                              specialization="Medical Officer",
                              years_experience=7)]
    mission1 = SpaceMission(mission_id="M3001A",
                            mission_name="Aurora Expedition",
                            destination="Estação Orbital Aurora",
                            launch_date="2026-06-10T09:00:00",
                            duration_days=180,
                            crew=crew1,
                            budget_millions=1200)
    print("Valid mission created:")
    print(f"Mission: {mission1.mission_name}")
    print(f"ID: {mission1.mission_id}")
    print(f"Destination: {mission1.destination}")
    print(f"Duration: {mission1.duration_days} days")
    print(f"Budget: ${mission1.budget_millions:.2f}M")
    print(f"Crew size: {ft_len(mission1.crew)}")
    print("Crew members:")
    for member in mission1.crew:
        name: str = member.name
        rank: str = member.rank.name.capitalize()
        spec: str = member.specialization
        print(f" - {name} ({rank}) - {spec}")
    print("\n=============================")
    try:
        crew2: list = [CrewMember(member_id="C3002A",
                                  name="Carlos Mendonça",
                                  rank=Rank.captain,
                                  age=39,
                                  specialization="Navigation",
                                  years_experience=15),
                       CrewMember(member_id="C3002B",
                                  name="Rafaela Costa",
                                  rank=Rank.lieutenant,
                                  age=31,
                                  specialization="Communications",
                                  years_experience=9),
                       CrewMember(member_id="C3002C",
                                  name="Thiago Nunes",
                                  rank=Rank.officer,
                                  age=28,
                                  specialization="Life Support",
                                  years_experience=6)]
        mission2 = SpaceMission(mission_id="M3002B",
                                mission_name="Lunar Resource Survey",
                                destination="Base Lunar Delta",
                                launch_date="2026-07-21T14:45:00",
                                duration_days=90,
                                crew=crew2,
                                budget_millions=450)
        print(f"Mission: {mission2.mission_name}")
        print(f"ID: {mission2.mission_id}")
        print(f"Destination: {mission2.destination}")
        print(f"Duration: {mission2.duration_days} days")
        print(f"Budget: ${mission2.budget_millions:.2f}M")
        print(f"Crew size: {ft_len(mission2.crew)}")
        print("Crew members:")
        for member in mission2.crew:
            name: str = member.name
            rank: str = member.rank.name.capitalize()
            spec: str = member.specialization
            print(f" - {name} ({rank}) - {spec}")
    except Exception as e:
        print(e)


if (__name__ == "__main__"):
    print("Space Mission Crew Validation")
    main()