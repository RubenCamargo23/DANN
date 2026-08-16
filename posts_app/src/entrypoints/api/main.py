from fastapi import FastAPI

from adapters.database import session as db_session
from config import Settings
from entrypoints.api.routers.post_router import router as post_router

app = FastAPI(title=Settings.app_name)
app.include_router(post_router)


@app.on_event("startup")
def on_startup():
    db_session.Base.metadata.create_all(bind=db_session.engine)
