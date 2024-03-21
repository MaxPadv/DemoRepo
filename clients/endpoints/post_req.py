from clients.endpoints.endpoints import PostReq


class PostAPI:
    """Класс-инициализатор объектов-endpoint'ов"""
    def __init__(self) -> None:
        self.post_req = PostReq()
