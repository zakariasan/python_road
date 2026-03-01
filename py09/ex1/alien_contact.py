"""
Alien Contacts: Custom validation rules and logic
"""
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    """
    Define contact types: radio, visual, physical, telepathic
    """
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    """
    Create a Pydantic model with these fields:
    """
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def custum_validation_rules(self) -> 'AlienContact':
        """
        Custom Validation Rules
        """
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if (self.contact_type == ContactType.physical and not
                self.is_verified):
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type == ContactType.telepathic and
                self.witness_count < 3):
            raise ValueError(
                    "Telepathic contact requires at least 3 witnesses")

        if (self.signal_strength > 7.0 and not
                self.message_received):
            raise ValueError(
                    "Strong signals (> 7.0) should include "
                    +
                    "received messages")

        return self


def main():
    """
    Show valid and invalid contact reports with clear error messages.
    """
    print("Alien Contact Log Validation")
    print("======================================")

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-02-01",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )

    print("Valid contact report:")
    print(f"  ID: {contact.contact_id}")
    print(f"  Type: {contact.contact_type.value}")
    print(f"  Location: {contact.location}")
    print(f"  Signal: {contact.signal_strength}/10")
    print(f"  Duration: {contact.duration_minutes} minutes")
    print(f"  Witnesses: {contact.witness_count}")
    print(f"  Message: '{contact.message_received}'")
    print("======================================")
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-02-01",
            location="Roswell, New Mexico",
            contact_type=ContactType.telepathic,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=1,
            is_verified=False,
        )
    except Exception as e:
        err = e.errors()[0]['msg']
        print(err)


if __name__ == "__main__":
    main()
