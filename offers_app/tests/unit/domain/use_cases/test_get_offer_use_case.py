import pytest

from domain.use_cases.get_offer_use_case import GetOfferUseCase
from errors import OfferNotFoundError


def test_get_offer_success(mocker, stored_offer):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_offer

    use_case = GetOfferUseCase(repository)
    result = use_case.execute(stored_offer.id)

    assert result.id == stored_offer.id


def test_get_offer_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = GetOfferUseCase(repository)

    with pytest.raises(OfferNotFoundError):
        use_case.execute("missing-id")
