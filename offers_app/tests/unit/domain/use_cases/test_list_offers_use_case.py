from domain.use_cases.list_offers_use_case import ListOffersUseCase


def test_list_offers_no_filter(mocker, stored_offer):
    repository = mocker.Mock()
    repository.list.return_value = [stored_offer]

    use_case = ListOffersUseCase(repository)
    result = use_case.execute()

    assert result == [stored_offer]
    repository.list.assert_called_once_with(post_id=None, owner_id=None)


def test_list_offers_with_filters(mocker, stored_offer):
    repository = mocker.Mock()
    repository.list.return_value = [stored_offer]

    use_case = ListOffersUseCase(repository)
    use_case.execute(post_id="post-1", owner_id="user-1")

    repository.list.assert_called_once_with(post_id="post-1", owner_id="user-1")
