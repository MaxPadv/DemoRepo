import allure
import pytest

from clients.post_req import PostReq
from clients.asserts.assert_post import PostAsserts


@allure.epic("Demo Back")
@allure.feature("Back Req")
@allure.story("Post Req")
@allure.label("api")
class TestPostDemo:
    @allure.description("Post запрос")
    @pytest.mark.parametrize("data", [{"data": "<base64 string>"}, "23", ""])
    def test_post_req(self, data, post_api: PostReq):
        with allure.step("Отправка пост запроса"):
            r = post_api.send_request(data=data)
            PostAsserts().check_post_r_pos(r)
