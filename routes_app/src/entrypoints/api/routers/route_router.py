from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_route_use_case,
    build_list_routes_use_case,
    build_reset_routes_use_case,
)
from domain.models.route import Route
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas import RouteCreateRequest
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError

router = APIRouter(prefix="/routes")


def _require_auth(authorization: Optional[str]):
    if not authorization:
        raise HTTPException(status_code=403, detail="Missing authorization header")


def _serialize(route: Route) -> dict:
    return {
        "id": route.id,
        "flightId": route.flight_id,
        "sourceAirportCode": route.source_airport_code,
        "sourceCountry": route.source_country,
        "destinyAirportCode": route.destiny_airport_code,
        "destinyCountry": route.destiny_country,
        "bagCost": route.bag_cost,
        "plannedStartDate": route.planned_start_date.isoformat(),
        "plannedEndDate": route.planned_end_date.isoformat(),
        "createdAt": route.created_at.isoformat(),
    }


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.get("/count")
def count_routes(use_case: BaseUseCase = Depends(build_count_routes_use_case)):
    """Count stored routes."""
    return {"count": use_case.execute()}


@router.post("/reset")
def reset_routes(use_case: BaseUseCase = Depends(build_reset_routes_use_case)):
    """Delete all routes."""
    use_case.execute()
    return {"msg": "Todos los datos fueron eliminados"}


@router.post(
    "",
    status_code=201,
    responses={
        403: {"description": "Missing authorization header"},
        412: {"description": "Invalid dates or flightId already exists"},
    },
)
def create_route(
    payload: RouteCreateRequest,
    authorization: Optional[str] = Header(default=None),
    use_case: BaseUseCase = Depends(build_create_route_use_case),
):
    """Create a new route."""
    _require_auth(authorization)

    route = Route(
        flight_id=payload.flightId,
        source_airport_code=payload.sourceAirportCode,
        source_country=payload.sourceCountry,
        destiny_airport_code=payload.destinyAirportCode,
        destiny_country=payload.destinyCountry,
        bag_cost=payload.bagCost,
        planned_start_date=payload.plannedStartDate,
        planned_end_date=payload.plannedEndDate,
    )
    try:
        created = use_case.execute(route)
    except InvalidRouteDatesError as err:
        raise HTTPException(status_code=412, detail=str(err))
    except RouteAlreadyExistsError as err:
        raise HTTPException(status_code=412, detail=str(err))
    return {"id": created.id, "createdAt": created.created_at.isoformat()}


@router.get("", responses={403: {"description": "Missing authorization header"}})
def list_routes(
    flight: Optional[str] = None,
    authorization: Optional[str] = Header(default=None),
    use_case: BaseUseCase = Depends(build_list_routes_use_case),
):
    """List/filter routes."""
    _require_auth(authorization)
    routes = use_case.execute(flight_id=flight)
    return [_serialize(r) for r in routes]


@router.get(
    "/{route_id}",
    responses={
        403: {"description": "Missing authorization header"},
        404: {"description": "Route not found"},
    },
)
def get_route(
    route_id: str,
    authorization: Optional[str] = Header(default=None),
    use_case: BaseUseCase = Depends(build_get_route_use_case),
):
    """Get a route by id."""
    _require_auth(authorization)
    try:
        route = use_case.execute(route_id)
    except RouteNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return _serialize(route)


@router.delete(
    "/{route_id}",
    responses={
        403: {"description": "Missing authorization header"},
        404: {"description": "Route not found"},
    },
)
def delete_route(
    route_id: str,
    authorization: Optional[str] = Header(default=None),
    use_case: BaseUseCase = Depends(build_delete_route_use_case),
):
    """Delete a route by id."""
    _require_auth(authorization)
    try:
        use_case.execute(route_id)
    except RouteNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return {"msg": "el trayecto fue eliminado"}
