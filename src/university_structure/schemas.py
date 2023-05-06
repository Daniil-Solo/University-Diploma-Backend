from pydantic import BaseModel


class InEntity(BaseModel):
    name: str


class OutEntity(BaseModel):
    id: int
    name: str


class InFaculty(InEntity):
    ...


class OutFaculty(OutEntity):
    ...


class InProfession(InEntity):
    specializations: list[int]


class OutProfession(OutEntity):
    ...


class InSpecialization(InEntity):
    faculty_id: int


class OutSpecialization(OutEntity):
    ...
