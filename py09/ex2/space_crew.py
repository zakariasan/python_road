from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class Rank(Enum):
    """
    Define crew ranks
    """
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    """
    Individual crew member with these fields
    """
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """
    Mission with crew list and these fields
    """
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(
            ...,
            min_length=1,
            max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_senior = False
        for member in self.crew:
            if member.rank in (Rank.commander, Rank.captain):
                has_senior = True
                break
        if not has_senior:
            raise ValueError(
                    "Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced_count = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_count += 1

            check = experienced_count / len(self.crew)
            if check < 0.5:
                raise ValueError(
                        "Long missions require 50% experienced "
                        +
                        "crew (5+ years). "
                        +
                        f"Currently {check:.0%} experienced.")

        inactive = []
        for member in self.crew:
            if not member.is_active:
                inactive.append(member.name)

        if inactive:
            raise ValueError(
                "All crew members must be active. Inactive: "
                +
                f"{', '.join(inactive)}"
            )

        return self


def main():
    print("Space Mission Crew Validation")
    print("=========================================")

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2026-02-01",
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=42,
                specialization="Mission Command",
                years_experience=20,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=35,
                specialization="Navigation",
                years_experience=10,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=6,
                is_active=True,
            ),
        ],
    )

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
                f"- {member.name} ({member.rank.value}) "
                +
                f"- {member.specialization}")

    print("=========================================")
    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Doomed Mission",
            destination="Venus",
            launch_date="2026-02-28",
            duration_days=180,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="CM010",
                    name="Bob Junior",
                    rank=Rank.cadet,
                    age=22,
                    specialization="Cleaning",
                    years_experience=0,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM011",
                    name="Jane Doe",
                    rank=Rank.officer,
                    age=28,
                    specialization="Science",
                    years_experience=3,
                    is_active=True,
                ),
            ],
        )
    except Exception as e:
        err = e.errors()[0]['msg']
        print(err)


if __name__ == "__main__":
    main()
