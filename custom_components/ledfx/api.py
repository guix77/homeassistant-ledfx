"""LedFx API Client."""
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
    """LedFx API Client."""

    def __init__(
        self,
        host: str,
        port: int,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize."""
        self._host = host
        self._port = port
        self._session = session

    def _url(self, path: str) -> str:
        return f"http://{self._host}:{self._port}{path}"

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return {
            "info": await self._api_wrapper(method="get", url=self._url("/api/info")),
            "scenes": await self._api_wrapper(method="get", url=self._url("/api/scenes")),
        }

    async def async_activate_device(self, virtual_id: str) -> any:
        """Trigger resolve_address + activate on a device."""
        return await self._api_wrapper(
            method="post",
            url=self._url(f"/api/devices/{virtual_id}"),
            data={},
        )

    async def async_activate_scene(self, scene_id: str) -> any:
        """Activate a scene."""
        return await self._api_wrapper(
            method="put",
            url=self._url("/api/scenes"),
            data={"id": scene_id, "action": "activate"},
        )

    async def async_deactivate_scene(self, scene_id: str) -> any:
        """Deactivate a scene."""
        return await self._api_wrapper(
            method="put",
            url=self._url("/api/scenes"),
            data={"id": scene_id, "action": "deactivate"},
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
