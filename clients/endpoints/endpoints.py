from clients.base_api_client import BaseRestEndpoint


class PostReq(BaseRestEndpoint):
    __path = "/save"
    json = None

    def __init__(self, path: str = __path) -> None:
        super().__init__(path)

    def send_request(
            self,
            expected_status_code: int = 500,
            json=json
    ):
        url = self.get_url()

        response = self.rest_client.send_request(
            method="POST", url=url, json=json, expected_status_code=expected_status_code
        )

        return response
