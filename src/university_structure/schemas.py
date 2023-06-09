from pydantic import BaseModel


class InEntity(BaseModel):
    name: str


class OutEntity(BaseModel):
    value: int
    label: str


class InFaculty(InEntity):
    ...


class OutFaculty(OutEntity):
    ...


class InAdminProfession(BaseModel):
    id: int
    name: str
    specializations: list[int]
    vector: dict


class OutProfession(OutEntity):
    ...


class InSpecialization(InEntity):
    faculty_id: int


class OutSpecialization(OutEntity):
    ...
