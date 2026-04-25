"""API client for Qcells Cloud."""

from __future__ import annotations

import asyncio
import logging
from typing import Any
from urllib.parse import urljoin

import aiohttp

from .const import API_PATH_REALTIME, STATIC_API_KEY, STATIC_BASE_URL, STATIC_WIFI_SN

_LOGGER = logging.getLogger(__name__)


class QcellsApiError(Exception):
    """Base API error."""


class QcellsApiAuthError(QcellsApiError):
    """Authentication error."""


class QcellsApiClient:
    """Thin client for the documented Qcells realtime endpoint."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
        wifi_sn: str,
        api_key: str,
        timeout: int = 15,
    ) -> None:
        self._session = session
        self._base_url = (base_url or STATIC_BASE_URL).rstrip("/")
        self._wifi_sn = wifi_sn or STATIC_WIFI_SN
        self._api_key = api_key or STATIC_API_KEY
        self._timeout = timeout

    async def async_get_realtime_data(self) -> dict[str, Any]:
        """Fetch realtime data from the Qcells API."""
        if not self._base_url:
            raise QcellsApiError("Missing base URL")
        if not self._wifi_sn:
            raise QcellsApiError("Missing wifiSn")
        if not self._api_key:
            raise QcellsApiAuthError("Missing API key")

        url = urljoin(f"{self._base_url}/", API_PATH_REALTIME.lstrip("/"))
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "tokenId": self._api_key,
        }
        payload = {"wifiSn": self._wifi_sn}

        _LOGGER.debug("Requesting Qcells realtime data from %s for wifiSn=%s", url, self._wifi_sn)

        try:
            async with asyncio.timeout(self._timeout):
                response = await self._session.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = await response.json(content_type=None)
        except TimeoutError as err:
            raise QcellsApiError("Timeout while talking to Qcells Cloud") from err
        except aiohttp.ClientResponseError as err:
            if err.status in (401, 403):
                raise QcellsApiAuthError(f"HTTP authentication error: {err.status}") from err
            raise QcellsApiError(f"HTTP error: {err.status}") from err
        except aiohttp.ClientError as err:
            raise QcellsApiError(f"Network error: {err}") from err
        except ValueError as err:
            raise QcellsApiError("Invalid JSON response from Qcells Cloud") from err

        success = data.get("success")
        code = data.get("code")
        message = data.get("exception") or "Unknown API error"

        if success is False:
            if code == 1001:
                raise QcellsApiAuthError(message)
            raise QcellsApiError(f"Qcells API error {code}: {message}")

        result = data.get("result")
        if not isinstance(result, dict):
            raise QcellsApiError("Qcells API response did not include a result object")

        return result
