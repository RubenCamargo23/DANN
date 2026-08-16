from domain.use_cases.count_offers_use_case import CountOffersUseCase


def test_count_offers(mocker):
    repository = mocker.Mock()
    repository.count.return_value = 5

    use_case = CountOffersUseCase(repository)

    assert use_case.execute() == 5
