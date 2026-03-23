from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.comparativo_agua import ComparativoAgua

router = APIRouter(prefix="/comparativoAgua", tags=["Comparativo Agua"])


# ==========================================================
# CREAR O ACTUALIZAR (UPSERT)
# ==========================================================
@router.post("/")
def crear_o_actualizar_comparativo_agua(
    nombre: str = Body(...),
    ubicacion: str = Body(...),
    cuenta: str = Body(...),
    anio: int = Body(...),
    mes: int = Body(...),
    m3_consumidos: float = Body(...),
    valor_consumo_agua: float = Body(...),
    cumple: bool = Body(None),
    db: Session = Depends(get_db)
):

    # buscar si ya existe el registro
    registro = db.query(ComparativoAgua).filter(
        ComparativoAgua.nombre == nombre,
        ComparativoAgua.anio == anio,
        ComparativoAgua.mes == mes
    ).first()

    # SI EXISTE → actualizar
    if registro:

        registro.ubicacion = ubicacion
        registro.cuenta = cuenta
        registro.m3_consumidos = m3_consumidos
        registro.valor_consumo_agua = valor_consumo_agua
        registro.cumple = cumple

        db.commit()
        db.refresh(registro)

        return {
            "mensaje": "Registro actualizado",
            "data": registro
        }

    # SI NO EXISTE → crear
    nuevo = ComparativoAgua(
        nombre=nombre,
        ubicacion=ubicacion,
        cuenta=cuenta,
        anio=anio,
        mes=mes,
        m3_consumidos=m3_consumidos,
        valor_consumo_agua=valor_consumo_agua,
        cumple=cumple,
       
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Registro creado",
        "data": nuevo
    }


# ==========================================================
# LISTAR
# ==========================================================
@router.get("/")
def listar_comparativos_agua(db: Session = Depends(get_db)):

    return (
        db.query(ComparativoAgua)
        .order_by(
            ComparativoAgua.anio.asc(),
            ComparativoAgua.mes.asc(),
            ComparativoAgua.id.asc()
        )
        .all()
    )


# ==========================================================
# OBTENER POR ID
# ==========================================================
@router.get("/{comparativo_id}")
def obtener_comparativo_agua(comparativo_id: int, db: Session = Depends(get_db)):

    registro = db.query(ComparativoAgua).filter(
        ComparativoAgua.id == comparativo_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Comparativo no encontrado")

    return registro


# ==========================================================
# ELIMINAR
# ==========================================================
@router.delete("/{comparativo_id}")
def eliminar_comparativo_agua(comparativo_id: int, db: Session = Depends(get_db)):

    registro = db.query(ComparativoAgua).filter(
        ComparativoAgua.id == comparativo_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Comparativo no encontrado")

    db.delete(registro)
    db.commit()

    return {"deleted": comparativo_id}