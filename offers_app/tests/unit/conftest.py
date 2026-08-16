from datetime import datetime

import pytest

from domain.models.offer import Offer, PackageSize


@pytest.fixture
def valid_offer_data():
    """Fixture providing valid offer creation data."""
    return {
        "post_id": "post-1",
        "user_id": "user-1",
        "description": "Paquete de prueba",
        "size": PackageSize.MEDIUM,
        "fragile": False,
        "offer": 100.0,
    }


@pytest.fixture
def stored_offer(valid_offer_data):
    """Fixture providing a persisted offer."""
    return Offer(id="offer-1", created_at=datetime.utcnow(), **valid_offer_data)
