from pydantic import BaseModel


class Chronicle(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class ChronicleCreate(BaseModel):
    title: str
    description: str
