from domain.use_cases.reset_offers_use_case import ResetOffersUseCase


def test_reset_offers(mocker):
    repository = mocker.Mock()

    use_case = ResetOffersUseCase(repository)
    use_case.execute()

    repository.reset.assert_called_once()
