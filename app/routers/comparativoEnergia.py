from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.comparativo_energia import ComparativoEnergia

router = APIRouter(prefix="/comparativoEnergia", tags=["Comparativo Energía"])


# ==========================================================
# CREAR O ACTUALIZAR (UPSERT)
# ==========================================================
@router.post("/")
def crear_o_actualizar_comparativo_energia(
    nombre: str = Body(...),
    ubicacion: str = Body(...),
    cuenta: str = Body(...),
    anio: int = Body(...),
    mes: int = Body(...),
    kw_consumidos: float = Body(...),
    valor_consumo_energia: float = Body(...),
    cumple: bool = Body(None),
    db: Session = Depends(get_db)
):

    # buscar si ya existe el registro
    registro = db.query(ComparativoEnergia).filter(
        ComparativoEnergia.nombre == nombre,
        ComparativoEnergia.anio == anio,
        ComparativoEnergia.mes == mes
    ).first()

    # SI EXISTE → actualizar
    if registro:

        registro.ubicacion = ubicacion
        registro.cuenta = cuenta
        registro.kw_consumidos = kw_consumidos
        registro.valor_consumo_energia = valor_consumo_energia
        registro.cumple = cumple

        db.commit()
        db.refresh(registro)

        return {
            "mensaje": "Registro actualizado",
            "data": registro
        }

    # SI NO EXISTE → crear
    nuevo = ComparativoEnergia(
        nombre=nombre,
        ubicacion=ubicacion,
        cuenta=cuenta,
        anio=anio,
        mes=mes,
        kw_consumidos=kw_consumidos,
        valor_consumo_energia=valor_consumo_energia,
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
def listar_comparativos_energia(db: Session = Depends(get_db)):

    return (
        db.query(ComparativoEnergia)
        .order_by(
            ComparativoEnergia.anio.asc(),
            ComparativoEnergia.mes.asc(),
            ComparativoEnergia.id.asc()
        )
        .all()
    )


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
# ELIMINAR
# ==========================================================
@router.delete("/{comparativo_id}")
def eliminar_comparativo_energia(comparativo_id: int, db: Session = Depends(get_db)):

    registro = db.query(ComparativoEnergia).filter(
        ComparativoEnergia.id == comparativo_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Comparativo no encontrado")

    db.delete(registro)
    db.commit()

    return {"deleted": comparativo_id}