# Qcells Cloud custom integration scaffold

This is a read-only Home Assistant custom integration scaffold for a Qcells cloud-backed inverter.

## What it does
- Calls `POST /api/v2/dataAccess/realtimeInfo/get`
- Sends `tokenId` in the HTTP headers
- Sends `wifiSn` in the JSON body
- Creates sensors for power, energy, SOC, battery power, PV string power, status and last upload time

## API key handling
You asked for the API key to be usable in two ways:

1. **Preferred:** enter it in the Home Assistant UI during setup
2. **Optional:** hardcode it in `custom_components/qcells_cloud/const.py`

The following optional fallback variables exist in `const.py`:
- `STATIC_BASE_URL`
- `STATIC_WIFI_SN`
- `STATIC_API_KEY`

If you fill those values, the config flow will prefill them.

## Install
1. Copy `custom_components/qcells_cloud` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings -> Devices & Services -> Add Integration**.
4. Search for **Qcells Cloud**.
5. Enter:
   - Base URL
   - WiFi SN
   - API key / tokenId
   - Polling interval

## Notes
- This version is **read-only** on purpose.
- It is meant to provide stable sensor data for automations that switch consumers like contactors, Shelly relays or ESPHome devices.
- If your cloud endpoint differs, change `DEFAULT_BASE_URL` or enter the correct base URL in the config flow.

## Example automation idea
- Turn on a load if `feedinpower` stays above 1500 W for 2 minutes
- Turn it off if the grid import becomes positive or battery SOC falls below a threshold
