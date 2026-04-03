from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.session import Base


class AreaResmas(Base):
    __tablename__ = "areas_resmas"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(150), nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    