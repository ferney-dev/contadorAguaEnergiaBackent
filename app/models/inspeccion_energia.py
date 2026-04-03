from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class InspeccionEnergia(Base):
    __tablename__ = "inspecciones_energia"

    id = Column(Integer, primary_key=True, index=True)

    # Datos principales
    fecha = Column(DateTime, nullable=False)
    responsable = Column(String(150), nullable=False)

    # 🔥 RELACIÓN CON ÁREA
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=False)
    area = relationship("Area")

    # ⚡ CAMPOS DE ENERGÍA

    # Bombillas
    bombillas_c = Column(Integer, default=0)
    bombillas_nc = Column(Integer, default=0)

    # Reflectores
    reflectores_c = Column(Integer, default=0)
    reflectores_nc = Column(Integer, default=0)

    # Lámparas de piso
    lamparas_c = Column(Integer, default=0)
    lamparas_nc = Column(Integer, default=0)

    # Aires acondicionados
    aires_c = Column(Integer, default=0)
    aires_nc = Column(Integer, default=0)

    # Observaciones
    observacion = Column(String(500), nullable=True)

    # Total
    total = Column(Integer, default=0)

    # Auditoría
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )