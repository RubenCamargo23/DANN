import pytest
from pydantic import ValidationError

from domain.models.offer import Offer, PackageSize


def test_create_offer_with_valid_data(valid_offer_data):
    offer = Offer(**valid_offer_data)
    assert offer.size == PackageSize.MEDIUM
    assert offer.id is None


def test_offer_rejects_invalid_size(valid_offer_data):
    data = {**valid_offer_data, "size": "HUGE"}
    with pytest.raises(ValidationError):
        Offer(**data)


def test_offer_rejects_negative_amount(valid_offer_data):
    data = {**valid_offer_data, "offer": -10}
    with pytest.raises(ValidationError):
        Offer(**data)


def test_offer_rejects_description_too_long(valid_offer_data):
    data = {**valid_offer_data, "description": "x" * 141}
    with pytest.raises(ValidationError):
        Offer(**data)
