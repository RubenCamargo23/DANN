from domain.use_cases.count_posts_use_case import CountPostsUseCase


def test_count_posts(mocker):
    repository = mocker.Mock()
    repository.count.return_value = 4

    use_case = CountPostsUseCase(repository)

    assert use_case.execute() == 4
