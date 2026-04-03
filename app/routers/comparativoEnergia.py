from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.comparativo_energia import ComparativoEnergia

router = APIRouter(prefix="/comparativoEnergia", tags=["Comparativo Energía"])


# ==========================================================
# CREAR
# ==========================================================
@router.post("/")
def guardar_comparativo_energia(
    nombre: str = Body(...),
    ubicacion: str = Body(...),
    cuenta: str = Body(...),
    anio: int = Body(...),
    mes: int = Body(...),
    kw_consumidos: float = Body(None),
    valor_consumo_energia: float = Body(None),
    cumple: bool = Body(True),
    db: Session = Depends(get_db)
):
    try:

        # 🔥 BUSCAR SI YA EXISTE
        registro = db.query(ComparativoEnergia).filter(
            ComparativoEnergia.nombre == nombre,
            ComparativoEnergia.anio == anio,
            ComparativoEnergia.mes == mes
        ).first()

        if registro:
            # 🔥 UPDATE
            registro.ubicacion = ubicacion
            registro.cuenta = cuenta
            registro.kw_consumidos = kw_consumidos
            registro.valor_consumo_energia = valor_consumo_energia
            registro.cumple = cumple

            db.commit()
            db.refresh(registro)

            return {"mensaje": "Actualizado"}

        else:
            # 🔥 CREATE
            nuevo = ComparativoEnergia(
                nombre=nombre,
                ubicacion=ubicacion,
                cuenta=cuenta,
                anio=anio,
                mes=mes,
                kw_consumidos=kw_consumidos,
                valor_consumo_energia=valor_consumo_energia,
                cumple=cumple
            )

            db.add(nuevo)
            db.commit()
            db.refresh(nuevo)

            return {"mensaje": "Creado"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


# ==========================================================
# ACTUALIZAR (🔥 POR ID)
# ==========================================================
@router.put("/")
def actualizar_comparativo_energia(
    id: int = Body(...),
    nombre: str = Body(...),
    ubicacion: str = Body(...),
    cuenta: str = Body(...),
    anio: int = Body(...),
    mes: int = Body(...),
    kw_consumidos: float = Body(None),
    valor_consumo_energia: float = Body(None),
    cumple: bool = Body(True),
    db: Session = Depends(get_db)
):
    try:
        registro = db.query(ComparativoEnergia).filter(
            ComparativoEnergia.id == id
        ).first()

        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        registro.nombre = nombre
        registro.ubicacion = ubicacion
        registro.cuenta = cuenta
        registro.kw_consumidos = kw_consumidos
        registro.valor_consumo_energia = valor_consumo_energia
        registro.cumple = cumple

        db.commit()
        db.refresh(registro)

        return {"mensaje": "Registro actualizado", "data": registro}

    except Exception as e:
        db.rollback()
        raise HTTPException(
    status_code=500,
    detail=f"Error interno: {str(e) or 'Error desconocido'}"
)


# ==========================================================
# LISTAR
# ==========================================================
@router.get("/")
def listar_comparativos_energia(db: Session = Depends(get_db)):
    return db.query(ComparativoEnergia).order_by(
        ComparativoEnergia.anio.asc(),
        ComparativoEnergia.mes.asc(),
        ComparativoEnergia.id.asc()
    ).all()


# ==========================================================
# OBTENER POR ID
# ==========================================================
@router.get("/{comparativo_id}")
def obtener_comparativo_energia(comparativo_id: int, db: Session = Depends(get_db)):

    registro = db.query(ComparativoEnergia).filter(
        ComparativoEnergia.id == comparativo_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Comparativo no encontrado")

    return registro


# ==========================================================
# ELIMINAR (🔥 POR ID)
# ==========================================================
@router.delete("/{comparativo_id}")
def eliminar_comparativo_energia(comparativo_id: int, db: Session = Depends(get_db)):

    try:
        registro = db.query(ComparativoEnergia).filter(
            ComparativoEnergia.id == comparativo_id
        ).first()

        if not registro:
            raise HTTPException(status_code=404, detail="Comparativo no encontrado")

        db.delete(registro)
        db.commit()

        return {"mensaje": "Registro eliminado", "id": comparativo_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
    status_code=500,
    detail=f"Error interno: {str(e) or 'Error desconocido'}"
)