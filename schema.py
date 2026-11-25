
from pydantic import BaseModel


class Extracted(BaseModel):
    title: str
    company: str | None = None
    location: str | None = None
    salary: int | None = None
    currency: str | None = None
    skills: list[str]
    remote: bool | None = None
    experience: str | None = None
