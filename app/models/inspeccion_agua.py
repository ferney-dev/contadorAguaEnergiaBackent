from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class InspeccionSanitaria(Base):
    __tablename__ = "inspecciones_sanitarias"

    id = Column(Integer, primary_key=True, index=True)

    # Datos principales
    fecha = Column(DateTime, nullable=False)
    responsable = Column(String(150), nullable=False)

    # 🔥 RELACIÓN CON ÁREA SANITARIA
    area_id = Column(Integer, ForeignKey("areas_sanitarias.id"), nullable=False)
    area = relationship("AreaSanitaria", back_populates="inspecciones")

    # 🚻 Sanitarios
    sanitarios_c = Column(Integer, default=0)
    sanitarios_nc = Column(Integer, default=0)

    # 🚽 Orinales
    orinales_c = Column(Integer, default=0)
    orinales_nc = Column(Integer, default=0)

    # 🚿 Duchas
    duchas_c = Column(Integer, default=0)
    duchas_nc = Column(Integer, default=0)

    # 🚰 Lavamanos
    lavamanos_c = Column(Integer, default=0)
    lavamanos_nc = Column(Integer, default=0)

    # 🔧 Llaves
    llaves_c = Column(Integer, default=0)
    llaves_nc = Column(Integer, default=0)

    # 📝 Observaciones
    observacion = Column(String(500), nullable=True)

    # 🔢 Total
    total = Column(Integer, default=0)

    # Auditoría
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )