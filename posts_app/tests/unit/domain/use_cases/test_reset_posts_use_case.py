from domain.use_cases.reset_posts_use_case import ResetPostsUseCase


def test_reset_posts(mocker):
    repository = mocker.Mock()

    use_case = ResetPostsUseCase(repository)
    use_case.execute()

    repository.reset.assert_called_once()
