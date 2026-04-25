"""Shared entity helpers for Qcells Cloud."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class QcellsCoordinatorEntity(CoordinatorEntity):
    """Base entity for Qcells Cloud entities."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data
        inverter_sn = data.get("inverterSN", "unknown")
        wifi_sn = data.get("sn", "unknown")
        return DeviceInfo(
            identifiers={(DOMAIN, inverter_sn)},
            name=f"Qcells Inverter {inverter_sn}",
            manufacturer="Qcells",
            model=f"Inverter type {data.get('inverterType', 'unknown')}",
            serial_number=inverter_sn,
            hw_version=wifi_sn,
        )
