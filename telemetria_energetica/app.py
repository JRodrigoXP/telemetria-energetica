from fastapi import FastAPI

from telemetria_energetica.database import Base, engine
from telemetria_energetica.models import Medicao  # noqa: F401
from telemetria_energetica.routers.telemetria import router as telemetria_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telemetria Energética")
app.include_router(telemetria_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "API de Telemetria Energética Ativa"}
