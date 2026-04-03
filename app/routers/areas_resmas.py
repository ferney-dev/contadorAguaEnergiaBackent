from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.area_resmas import AreaResmas
from app.models.resmas import Resmas

router = APIRouter(prefix="/areas-resmas", tags=["Areas Resmas"])


# =======================
# ✅ CREAR AREA
# =======================
@router.post("/")
def crear_area(data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        nombre = (data.get("nombre") or "").strip()

        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre es obligatorio")

        existe = db.query(AreaResmas).filter(AreaResmas.nombre == nombre).first()
        if existe:
            raise HTTPException(status_code=400, detail="El área ya existe")

        nueva = AreaResmas(nombre=nombre)

        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        return {
            "id": nueva.id,
            "nombre": nueva.nombre,
            "mensaje": "Área creada correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creando área: {str(e)}")


# =======================
# 📄 LISTAR AREAS
# =======================
@router.get("/")
def listar_areas(db: Session = Depends(get_db)):
    try:
        areas = db.query(AreaResmas).order_by(AreaResmas.nombre.asc()).all()

        return [
            {
                "id": a.id,
                "nombre": a.nombre
            }
            for a in areas
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando áreas: {str(e)}")


# =======================
# 🔍 OBTENER AREA
# =======================
@router.get("/{id}")
def obtener_area(id: int, db: Session = Depends(get_db)):
    try:
        area = db.query(AreaResmas).filter(AreaResmas.id == id).first()

        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")

        return {
            "id": area.id,
            "nombre": area.nombre
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo área: {str(e)}")


# =======================
# ✏️ ACTUALIZAR AREA
# =======================
@router.put("/{id}")
def actualizar_area(id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        area = db.query(AreaResmas).filter(AreaResmas.id == id).first()

        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")

        nombre = (data.get("nombre") or "").strip()

        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre es obligatorio")

        existe = db.query(AreaResmas).filter(
            AreaResmas.nombre == nombre,
            AreaResmas.id != id
        ).first()

        if existe:
            raise HTTPException(status_code=400, detail="Ya existe otra área con ese nombre")

        area.nombre = nombre

        db.commit()
        db.refresh(area)

        return {
            "id": area.id,
            "nombre": area.nombre,
            "mensaje": "Área actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando área: {str(e)}")


# =======================
# ❌ ELIMINAR AREA
# =======================
@router.delete("/{id}")
def eliminar_area(id: int, db: Session = Depends(get_db)):
    try:
        area = db.query(AreaResmas).filter(AreaResmas.id == id).first()

        if not area:
            raise HTTPException(status_code=404, detail="Área no encontrada")

        # 🔥 ELIMINAR RESMAS RELACIONADAS
        db.query(Resmas).filter(Resmas.area_id == id).delete()

        db.delete(area)
        db.commit()

        return {
            "mensaje": "Área eliminada correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error eliminando área: {str(e)}")