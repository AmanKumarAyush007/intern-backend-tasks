
import logging

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class CRMClient:
    """Reusable client for the JSONPlaceholder CRM API."""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            )
        ),
        reraise=True,
    )
    def get_users(self) -> list[dict]:
        """Fetch all CRM users."""

        response = self.session.get(
            f"{self.BASE_URL}/users",
            timeout=self.timeout,
        )

        data = self._handle_response(response)

        if not isinstance(data, list):
            raise ValueError("Expected a list of users")

        return data

    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            )
        ),
        reraise=True,
    )

    def get_user(self, user_id: int) -> dict:
        """Fetch a single CRM user by ID."""

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer")

        response = self.session.get(
            f"{self.BASE_URL}/users/{user_id}",
            timeout=self.timeout,
        )

        data = self._handle_response(response)

        if not isinstance(data, dict):
            raise ValueError("Expected a user object")

        return data

    def create_post(
        self,
        title: str,
        body: str,
        user_id: int,
    ) -> dict:
        """Create a simulated CRM post."""

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title cannot be empty")

        if not isinstance(body, str) or not body.strip():
            raise ValueError("Body cannot be empty")

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be positive")

        payload = {
            "title": title,
            "body": body,
            "userId": user_id,
        }

        response = self.session.post(
            f"{self.BASE_URL}/posts",
            json=payload,
            timeout=self.timeout,
        )

        return self._handle_response(response)

    def _handle_response(self, response):
        """Raise HTTP errors and parse JSON responses."""

        try:
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            logger.exception(
                "CRM HTTP error: status=%s",
                response.status_code,
            )
            raise

        except ValueError:
            logger.exception("CRM returned invalid JSON")
            raise
