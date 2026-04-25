#!/usr/bin/env python3
"""Test script for Qcells Cloud API."""

import asyncio
import sys
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try to load .env_prod first (production), then .env (development)
    # Check both in current directory and parent directories
    env_prod_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env_prod')
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')

    if os.path.exists(env_prod_path):
        load_dotenv(env_prod_path)
        print(f"Loaded environment from: {env_prod_path}")
    elif os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
    else:
        print("No .env or .env_prod file found. Using placeholder values.")
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set environment variables manually.")

# Add the custom component path to sys.path so we can import the API client
sys.path.insert(0, os.path.dirname(__file__))

import aiohttp
from api import QcellsApiClient, QcellsApiError, QcellsApiAuthError
from const import DEFAULT_BASE_URL

# Configuration - loaded from environment variables
BASE_URL = os.getenv('QCELLS_BASE_URL', DEFAULT_BASE_URL)
WIFI_SN = os.getenv('QCELLS_WIFI_SN', 'your_lan_adapter_registration_number')
API_KEY = os.getenv('QCELLS_API_KEY', 'your_api_key_here')

async def main():
    """Test the Qcells API."""
    print("Testing Qcells Cloud API...")
    print(f"Base URL: {BASE_URL}")
    print(f"WiFi SN: {WIFI_SN}")
    print(f"API Key: {'*' * len(API_KEY) if API_KEY else 'Not set'}")
    print()

    async with aiohttp.ClientSession() as session:
        api = QcellsApiClient(
            session=session,
            base_url=BASE_URL,
            wifi_sn=WIFI_SN,
            api_key=API_KEY,
        )

        try:
            data = await api.async_get_realtime_data()
            print("SUCCESS: API call successful!")
            print("Realtime data:")
            print("=" * 50)
            print(f"Total data points: {len(data)}")
            print("Available keys:")
            for i, key in enumerate(sorted(data.keys()), 1):
                print(f"  {i:2d}. {key}")
            print()
            print("Sample values:")
            for key in sorted(data.keys())[:10]:  # Show first 10 values
                value = data[key]
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value} ({type(value).__name__})")

        except QcellsApiAuthError as e:
            print(f"ERROR: Authentication error: {e}")
        except QcellsApiError as e:
            print(f"ERROR: API error: {e}")
            # Let's also print the raw response to debug
            print("\nDEBUG: Let's try a direct API call to see the raw response...")
            await debug_raw_api_call(BASE_URL, WIFI_SN, API_KEY)
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")

async def debug_raw_api_call(base_url: str, wifi_sn: str, api_key: str):
    """Make a raw API call to see the actual response."""
    from const import API_PATH_REALTIME
    from urllib.parse import urljoin

    url = urljoin(f"{base_url}/", API_PATH_REALTIME.lstrip("/"))
    params = {
        "tokenId": api_key,
        "sn": wifi_sn,
    }

    print(f"URL: {url}")
    print(f"Params: {params}")

    async with aiohttp.ClientSession() as session:
        try:
            async with asyncio.timeout(15):
                response = await session.get(url, params=params)
                print(f"HTTP Status: {response.status}")
                print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")

                text = await response.text()
                print(f"Raw Response (first 500 chars): {text[:500]}")
                if len(text) > 500:
                    print(f"... ({len(text) - 500} more characters)")

                if response.headers.get('Content-Type', '').startswith('application/json'):
                    try:
                        json_data = await response.json()
                        print("JSON Response (parsed):")
                        import json
                        print(json.dumps(json_data, indent=2))
                    except Exception as e:
                        print(f"ERROR: Could not parse JSON: {e}")
        except Exception as e:
            print(f"ERROR: Raw API call failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())