from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Chronicle(Base):
    __tablename__ = "chronicles"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(255), nullable=False)
    description = Column(Text)

    files = relationship("File", back_populates="chronicle")
    compositions = relationship("Composition", back_populates="chronicle")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    name = Column(String(128), nullable=False)
    path = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    mime = Column(String(64), nullable=False)
    thumb_name = Column(String(128), nullable=False)
    thumb_path = Column(String(255), nullable=False)
    thumb_url = Column(String(255), nullable=False)
    chronicle_id = Column(Integer, ForeignKey("chronicles.id"), nullable=False)

    chronicle = relationship("chronicle", back_populates="files")


class Composition(Base):
    __tablename__ = "compositions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(255), nullable=False)
    is_ready = Column(Boolean(255), nullable=False, default=False)
    data = Column(LargeBinary)
    chronicle_id = Column(Integer, ForeignKey("chronicles.id"), nullable=False)

    chronicle = relationship("chronicle", back_populates="compositions")
