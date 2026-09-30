from datetime import datetime

from sqlalchemy import Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from telemetria_energetica.database import Base


class Medicao(Base):
    __tablename__ = "medicoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    maquina_id: Mapped[int] = mapped_column(Integer, nullable=False)
    consumo_kwh: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    data_hora: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
