from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from telemetria_energetica.database import get_session
from telemetria_energetica.models import Medicao
from telemetria_energetica.schemas import (
    KPIsPublic,
    MedicaoList,
    MedicaoPublic,
    MedicaoSchema,
)

router = APIRouter(prefix="/medicoes", tags=["telemetria"])


@router.post("/", response_model=MedicaoPublic, status_code=status.HTTP_201_CREATED)
def create_medicao(
    medicao: MedicaoSchema,
    session: Session = Depends(get_session),
) -> Medicao:
    nova_medicao = Medicao(**medicao.model_dump())
    session.add(nova_medicao)
    session.commit()
    session.refresh(nova_medicao)
    return nova_medicao


@router.get("/", response_model=MedicaoList)
def read_medicoes(session: Session = Depends(get_session)) -> list[Medicao]:
    return list(session.scalars(select(Medicao).order_by(Medicao.id)).all())


@router.put("/{medicao_id}", response_model=MedicaoPublic)
def update_medicao(
    medicao_id: int,
    medicao: MedicaoSchema,
    session: Session = Depends(get_session),
) -> Medicao:
    medicao_db = session.get(Medicao, medicao_id)
    if medicao_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medição não encontrada",
        )

    for campo, valor in medicao.model_dump().items():
        setattr(medicao_db, campo, valor)

    session.commit()
    session.refresh(medicao_db)
    return medicao_db


@router.delete("/{medicao_id}")
def delete_medicao(
    medicao_id: int,
    session: Session = Depends(get_session),
) -> dict[str, str]:
    medicao_db = session.get(Medicao, medicao_id)
    if medicao_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medição não encontrada",
        )

    session.delete(medicao_db)
    session.commit()
    return {"message": "Medição removida com sucesso"}


@router.get("/kpis", response_model=KPIsPublic)
def get_kpis(session: Session = Depends(get_session)) -> KPIsPublic:
    consumo_total, consumo_medio, maquinas_operando = session.execute(
        select(
            func.coalesce(func.sum(Medicao.consumo_kwh), 0.0),
            func.coalesce(func.avg(Medicao.consumo_kwh), 0.0),
            func.count(Medicao.id).filter(Medicao.status == "operando"),
        )
    ).one()

    return KPIsPublic(
        consumo_total_kwh=float(consumo_total),
        consumo_medio_kwh=float(consumo_medio),
        maquinas_operando=maquinas_operando,
    )
