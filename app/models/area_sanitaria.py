from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class AreaSanitaria(Base):
    __tablename__ = "areas_sanitarias"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(150), nullable=False, unique=True)

    # 🔗 RELACIÓN CON INSPECCIONES
    inspecciones = relationship(
        "InspeccionSanitaria",
        back_populates="area",
        cascade="all, delete"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )