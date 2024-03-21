from hamcrest import assert_that, is_
from requests import Response


class PostAsserts:
    """Выражения для Post запроса"""

    @staticmethod
    def check_post_r_pos(result: Response) -> None:
        r_body = result.json()
        assert_that(result.status_code, is_(500))
        assert_that(r_body["status"], is_("FAILED"))
        assert_that(r_body["description"], is_("unknown error"))
