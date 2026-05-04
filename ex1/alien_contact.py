try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError:
    print("Use pip intall pydantic")
    exit(1)

from datetime import datetime
from typing import Optional
from enum import Enum


class ContactType(Enum):
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validation(self) -> 'AlienContact':
        if (self.contact_id[0:2] != "AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if ((self.contact_type.name == "physical") and
                (self.is_verified is None)):
            raise ValueError("A physical contact must be veified")
        if ((self.contact_type.name == "telepathic") and
                (self.witness_count < 3)):
            raise ValueError("That's not enough witnesses")
        if ((self.signal_strength > 7) and (self.message_received is None)):
            raise ValueError("A strong telepathic contact like that "
                             "must have an message")
        return (self)


def main() -> None:
    print("Alien Contact Log Validation")
    print("=============================")
    house: str = "Santa Cruz da Serra, Duque de Caxias - RJ"
    try:
        contact1 = AlienContact(contact_id="AC456",
                                timestamp="2026-05-04T21:00:00",
                                location="Observatório Nacional, Rio de Janeiro - RJ",
                                contact_type=ContactType.visual,
                                signal_strength=5.2,
                                duration_minutes=15,
                                witness_count=4,
                                message_received="Objeto brilhante observado",
                                is_verified=True)
        print("Valid contact report:")
        print(f"Type: {contact1.contact_type.name.capitalize()}")
        print(f"Location: {contact1.location}")
        print(f"Signal: {contact1.signal_strength:.1f}/10")
        print(f"Duration: {contact1.duration_minutes} minutes")
        print(f"Witnesses: {contact1.witness_count}")
        if (not (contact1.message_received is None)):
            print(f"Message: {contact1.message_received}")
    except Exception as e:
        print(e)
    print("\n=============================")
    try:
        contact2 = AlienContact(contact_id="AC789",
                                timestamp="2026-05-05T03:15:00",
                                location="Ilha do Mel, Paraná",
                                contact_type=ContactType.telepathic,
                                signal_strength=8.1,
                                duration_minutes=25,
                                witness_count=5,
                                message_received="Estamos em paz",
                                is_verified=True)
        print("Valid contact report:")
        print(f"Type: {contact2.contact_type.name.capitalize()}")
        print(f"Location: {contact2.location}")
        print(f"Signal: {contact2.signal_strength:.1f}/10")
        print(f"Duration: {contact2.duration_minutes} minutes")
        print(f"Witnesses: {contact2.witness_count}")
        if (not (contact2.message_received is None)):
            print(f"Message: {contact2.message_received}")
    except Exception as e:
        print(e)


if (__name__ == "__main__"):
    main()