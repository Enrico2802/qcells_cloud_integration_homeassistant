"""Config flow for Qcells Cloud."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import QcellsApiAuthError, QcellsApiClient, QcellsApiError
from .const import (
    CONF_BASE_URL,
    CONF_SCAN_INTERVAL,
    CONF_WIFI_SN,
    DEFAULT_BASE_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    STATIC_API_KEY,
    STATIC_BASE_URL,
    STATIC_WIFI_SN,
)


class QcellsCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Qcells Cloud."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_WIFI_SN])
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            api = QcellsApiClient(
                session=session,
                base_url=user_input[CONF_BASE_URL],
                wifi_sn=user_input[CONF_WIFI_SN],
                api_key=user_input[CONF_API_KEY],
            )
            try:
                await api.async_get_realtime_data()
            except QcellsApiAuthError:
                errors["base"] = "invalid_auth"
            except QcellsApiError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Qcells {user_input[CONF_WIFI_SN]}",
                    data=user_input,
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_BASE_URL, default=STATIC_BASE_URL or DEFAULT_BASE_URL): str,
                vol.Required(CONF_WIFI_SN, default=STATIC_WIFI_SN): str,
                vol.Required(CONF_API_KEY, default=STATIC_API_KEY): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=10, max=600),
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return QcellsCloudOptionsFlowHandler(config_entry)


class QcellsCloudOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Qcells Cloud options."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        schema = vol.Schema(
            {
                vol.Optional(CONF_SCAN_INTERVAL, default=current_interval): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=10, max=600),
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
