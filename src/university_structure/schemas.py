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
    ...


class OutProfession(OutEntity):
    ...


class InSpecialization(InEntity):
    ...


class OutSpecialization(OutEntity):
    ...
