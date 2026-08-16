from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.database import session as db_session
from config import Settings
from entrypoints.api.routers.route_router import router as route_router

app = FastAPI(title=Settings.app_name)
app.include_router(route_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.on_event("startup")
def on_startup():
    db_session.Base.metadata.create_all(bind=db_session.engine)
