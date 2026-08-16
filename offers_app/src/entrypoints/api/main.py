from fastapi import FastAPI

from adapters.database import session as db_session
from config import Settings
from entrypoints.api.routers.offer_router import router as offer_router

app = FastAPI(title=Settings.app_name)
app.include_router(offer_router)


@app.on_event("startup")
def on_startup():
    db_session.Base.metadata.create_all(bind=db_session.engine)
