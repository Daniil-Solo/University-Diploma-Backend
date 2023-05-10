from pydantic import BaseModel


class BaseElective(BaseModel):
    title: str


class OutElective(BaseElective):
    id: int


class InAdminElective(BaseModel):
    id: int
    name: str
    type: int
    vector: dict


class ElectiveGroup(BaseModel):
    name: str
    items: list[OutElective]
