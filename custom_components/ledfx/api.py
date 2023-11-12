"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class LedfxApiClientError(Exception):
    """Exception to indicate a general API error."""


class LedfxApiClientCommunicationError(
    LedfxApiClientError
):
    """Exception to indicate a communication error."""


class LedfxApiClientAuthenticationError(
    LedfxApiClientError
):
    """Exception to indicate an authentication error."""


class LedfxApiClient:
    """Sample API Client."""

    def __init__(
        self,
        host: str,
        port: int,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._host = host
        self._port = port
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        data = {}
        data["info"] = await self._api_wrapper(
            method="get",
            url=f"http://{self._host}:{self._port}/api/info"
        )
        data["scenes"] = await self._api_wrapper(
            method="get",
            url=f"http://{self._host}:{self._port}/api/scenes"
        )
        data["virtuals"] = await self._api_wrapper(
            method="get",
            url=f"http://{self._host}:{self._port}/api/virtuals"
        )
        return data

    async def async_get_info(self) -> any:
        """Get information about LedFx."""
        return await self._api_wrapper(
            method="get",
            url=f"http://{self._host}:{self._port}/api/info"
        )

    async def async_toggle_pause(self) -> any:
        """Toggle pause."""
        return await self._api_wrapper(
            method="put",
            url=f"http://{self._host}:{self._port}/api/virtuals"
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Make the request."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise LedfxApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise LedfxApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise LedfxApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise LedfxApiClientError(
                "Something really wrong happened!"
            ) from exception
