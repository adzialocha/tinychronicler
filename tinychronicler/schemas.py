from pydantic import BaseModel


class ChronicleBase(BaseModel):
    title: str
    description: str


class ChronicleIn(ChronicleBase, BaseModel):
    pass


class Chronicle(ChronicleBase, BaseModel):
    id: int

    class Config:
        orm_mode = True


class ChronicleOut(Chronicle, BaseModel):
    pass


class FileBase(BaseModel):
    mime: str
    name: str
    url: str
    thumb_name: str
    thumb_url: str


class FileIn(FileBase, BaseModel):
    path: str
    thumb_path: str


class File(FileIn, BaseModel):
    id: int

    class Config:
        orm_mode = True


class FileOut(FileBase, BaseModel):
    pass
