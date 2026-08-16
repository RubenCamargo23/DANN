from fastapi import FastAPI

from adapters.database import session as db_session
from config import Settings
from entrypoints.api.routers.user_router import router as user_router

app = FastAPI(title=Settings.app_name)
app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    db_session.Base.metadata.create_all(bind=db_session.engine)
