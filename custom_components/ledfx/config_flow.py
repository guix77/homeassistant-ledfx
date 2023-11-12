"""Adds config flow for Ledfx."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    LedfxApiClient,
    LedfxApiClientAuthenticationError,
    LedfxApiClientCommunicationError,
    LedfxApiClientError,
)
from .const import DOMAIN, LOGGER


class LedfxFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Ledfx."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_ledfx_api_connection(
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                )
            except LedfxApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except LedfxApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except LedfxApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default="localhost"
                    ): str,
                    vol.Required(
                        CONF_PORT,
                        default=8888
                    ): int,
                }
            ),
            errors=_errors,
        )

    async def _test_ledfx_api_connection(self, host: str, port: int) -> None:
        """Validate LedFX API connection."""
        client = LedfxApiClient(
            host=host,
            port=port,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
