from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class MedicaoSchema(BaseModel):
    maquina_id: int
    consumo_kwh: float
    status: Literal["operando", "manutencao", "desligado"]


class MedicaoPublic(MedicaoSchema):
    id: int
    data_hora: datetime

    model_config = ConfigDict(from_attributes=True)


MedicaoList = list[MedicaoPublic]


class KPIsPublic(BaseModel):
    consumo_total_kwh: float
    consumo_medio_kwh: float
    maquinas_operando: int
