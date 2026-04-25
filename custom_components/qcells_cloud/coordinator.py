"""Data update coordinator for Qcells Cloud."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import QcellsApiAuthError, QcellsApiClient, QcellsApiError

_LOGGER = logging.getLogger(__name__)


class QcellsDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch realtime data from Qcells."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: QcellsApiClient,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Qcells Cloud",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.async_get_realtime_data()
        except QcellsApiAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except QcellsApiError as err:
            raise UpdateFailed(str(err)) from err
