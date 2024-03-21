import allure
import pytest

from clients.endpoints.post_req import PostReq
from clients.asserts.assert_post import PostAsserts


@allure.epic("Demo Back")
@allure.feature("Back Req")
@allure.story("Post Req")
@allure.label("api")
class TestPostDemo:
    @allure.description("Post запрос")
    @pytest.mark.parametrize("json", [{"data": "<base64 string>"}, "23", "", 1])
    def test_post_req(self, json, post_api: PostReq):
        with allure.step("Отправка пост запроса"):
            r = post_api.send_request(json=json)
            PostAsserts().check_post_r_pos(r)
