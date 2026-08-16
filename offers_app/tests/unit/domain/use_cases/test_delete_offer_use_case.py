import pytest

from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from errors import OfferNotFoundError


def test_delete_offer_success(mocker, stored_offer):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_offer

    use_case = DeleteOfferUseCase(repository)
    use_case.execute(stored_offer.id)

    repository.delete.assert_called_once_with(stored_offer.id)


def test_delete_offer_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = DeleteOfferUseCase(repository)

    with pytest.raises(OfferNotFoundError):
        use_case.execute("missing-id")

    repository.delete.assert_not_called()
