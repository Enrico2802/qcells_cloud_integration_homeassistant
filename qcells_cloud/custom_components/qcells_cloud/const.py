"""Constants for the Qcells Cloud integration."""

from __future__ import annotations

DOMAIN = "qcells_cloud"
PLATFORMS = ["sensor"]

CONF_BASE_URL = "base_url"
CONF_WIFI_SN = "wifi_sn"
CONF_API_KEY = "api_key"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_BASE_URL = "https://qhome-ess-g3.q-cells.eu"
DEFAULT_SCAN_INTERVAL = 30

# Optional hardcoded fallback values.
# If you do not want to enter values in the UI every time,
# you can fill these fields directly.
STATIC_BASE_URL = ""
STATIC_WIFI_SN = ""
STATIC_API_KEY = ""

API_PATH_REALTIME = "/api/v2/dataAccess/realtimeInfo/get"

STATUS_MAP: dict[str, str] = {
    "100": "Waiting for operation",
    "101": "Self-test",
    "102": "Normal",
    "103": "Recoverable fault",
    "104": "Permanent fault",
    "105": "Firmware upgrade",
    "106": "EPS detection",
    "107": "Off-grid",
    "108": "Self-test mode",
    "109": "Sleep mode",
    "110": "Standby mode",
    "111": "PV wake-up battery mode",
    "112": "Generator detection mode",
    "113": "Generator mode",
    "114": "Fast shutdown standby mode",
    "130": "VPP mode",
    "131": "TOU self use",
    "132": "TOU charging",
    "133": "TOU discharging",
}
