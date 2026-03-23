from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String
from sqlalchemy.sql import func
from app.database.session import Base


class ComparativoEnergia(Base):
    __tablename__ = "comparativo_energia"

    id = Column(Integer, primary_key=True, index=True)

    # Datos de la ubicación
    nombre = Column(String(150), nullable=False)
    ubicacion = Column(String(150), nullable=False)
    cuenta = Column(String(50), nullable=False)

    # Fecha del consumo
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    # Consumo de energía
    kw_consumidos = Column(Float, nullable=False)

    # Valor pagado
    valor_consumo_energia = Column(Float, nullable=False)

    # Indicador de cumplimiento
    cumple = Column(Boolean, default=None)

    # Auditoría
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )