from pydantic import BaseModel


class ChronicleIn(BaseModel):
    title: str
    description: str


class Chronicle(ChronicleIn, BaseModel):
    id: int

    class Config:
        orm_mode = True


class FileIn(BaseModel):
    mime: str
    name: str
    path: str
    url: str
    thumb_name: str
    thumb_path: str
    thumb_url: str


class File(FileIn, BaseModel):
    id: int

    class Config:
        orm_mode = True
