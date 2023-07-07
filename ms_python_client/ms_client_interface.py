import logging
from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional

import requests

logger = logging.getLogger("ms_python_client")


class MSClientInterface(ABC):
    @abstractmethod
    def make_get_request(
        self, api_path: str, parameters: Optional[Mapping[str, str]] = None
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError

    @abstractmethod
    def make_post_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError

    @abstractmethod
    def make_patch_request(
        self, api_path: str, data: Mapping[str, Any]
    ) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError

    @abstractmethod
    def make_delete_request(self, api_path: str) -> requests.Response:
        logger.warning("Method not implemented")
        raise NotImplementedError
