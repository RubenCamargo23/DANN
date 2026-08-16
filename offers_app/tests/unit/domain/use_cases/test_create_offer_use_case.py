from domain.models.offer import Offer
from domain.use_cases.create_offer_use_case import CreateOfferUseCase


def test_create_offer_success(mocker, valid_offer_data):
    repository = mocker.Mock()
    repository.create.side_effect = lambda offer: offer

    use_case = CreateOfferUseCase(repository)
    result = use_case.execute(Offer(**valid_offer_data))

    assert result.post_id == "post-1"
    assert result.created_at is not None
    repository.create.assert_called_once()
