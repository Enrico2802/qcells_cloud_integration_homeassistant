"""Sensor platform for Qcells Cloud."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfEnergy, UnitOfPower, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, STATUS_MAP
from .entity import QcellsCoordinatorEntity


@dataclass(frozen=True, kw_only=True)
class QcellsSensorDescription(SensorEntityDescription):
    """Description of a Qcells sensor."""

    value_key: str
    suggested_display_precision: int | None = None


SENSORS: tuple[QcellsSensorDescription, ...] = (
    QcellsSensorDescription(
        key="acpower",
        value_key="acpower",
        name="AC power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="feedinpower",
        value_key="feedinpower",
        name="Feed-in power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="batPower",
        value_key="batPower",
        name="Battery power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="powerdc1",
        value_key="powerdc1",
        name="PV1 power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="powerdc2",
        value_key="powerdc2",
        name="PV2 power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="powerdc3",
        value_key="powerdc3",
        name="PV3 power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="powerdc4",
        value_key="powerdc4",
        name="PV4 power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="pv_power_total",
        value_key="pv_power_total",
        name="Total PV power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="soc",
        value_key="soc",
        name="Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.BATTERY,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="yieldtoday",
        value_key="yieldtoday",
        name="Yield today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        suggested_display_precision=1,
    ),
    QcellsSensorDescription(
        key="yieldtotal",
        value_key="yieldtotal",
        name="Yield total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        suggested_display_precision=1,
    ),
    QcellsSensorDescription(
        key="feedinenergy",
        value_key="feedinenergy",
        name="Feed-in energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        suggested_display_precision=1,
    ),
    QcellsSensorDescription(
        key="consumeenergy",
        value_key="consumeenergy",
        name="Grid import energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        suggested_display_precision=1,
    ),
    QcellsSensorDescription(
        key="feedinpowerM2",
        value_key="feedinpowerM2",
        name="Extra inverter power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="peps1",
        value_key="peps1",
        name="EPS phase A power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="peps2",
        value_key="peps2",
        name="EPS phase B power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
    QcellsSensorDescription(
        key="peps3",
        value_key="peps3",
        name="EPS phase C power",
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        suggested_display_precision=0,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [QcellsRealtimeSensor(coordinator, description) for description in SENSORS]
    entities.append(QcellsStatusSensor(coordinator))
    entities.append(QcellsUploadTimeSensor(coordinator))
    async_add_entities(entities)


class QcellsRealtimeSensor(QcellsCoordinatorEntity, SensorEntity):
    """Simple realtime sensor."""

    entity_description: QcellsSensorDescription

    def __init__(self, coordinator, description: QcellsSensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        inverter_sn = coordinator.data.get("inverterSN", "unknown")
        self._attr_unique_id = f"{inverter_sn}_{description.key}"
        self._attr_suggested_display_precision = description.suggested_display_precision

    @property
    def native_value(self) -> Any:
        if self.entity_description.value_key == "pv_power_total":
            values = [
                self.coordinator.data.get("powerdc1"),
                self.coordinator.data.get("powerdc2"),
                self.coordinator.data.get("powerdc3"),
                self.coordinator.data.get("powerdc4"),
                self.coordinator.data.get("feedinpowerM2"),
            ]
            total = 0.0
            for value in values:
                if value is None:
                    continue
                try:
                    total += float(value)
                except (TypeError, ValueError):
                    continue
            return total
        return self.coordinator.data.get(self.entity_description.value_key)


class QcellsStatusSensor(QcellsCoordinatorEntity, SensorEntity):
    """Human-readable inverter status."""

    _attr_name = "Inverter status"
    _attr_icon = "mdi:solar-power"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        inverter_sn = coordinator.data.get("inverterSN", "unknown")
        self._attr_unique_id = f"{inverter_sn}_status"

    @property
    def native_value(self) -> str | None:
        status_code = self.coordinator.data.get("inverterStatus")
        if status_code is None:
            return None
        return STATUS_MAP.get(str(status_code), f"Unknown ({status_code})")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"status_code": self.coordinator.data.get("inverterStatus")}


class QcellsUploadTimeSensor(QcellsCoordinatorEntity, SensorEntity):
    """Last upload timestamp from the inverter/cloud."""

    _attr_name = "Last upload time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        inverter_sn = coordinator.data.get("inverterSN", "unknown")
        self._attr_unique_id = f"{inverter_sn}_upload_time"

    @property
    def native_value(self) -> datetime | None:
        value = self.coordinator.data.get("uploadTime")
        if not value:
            return None
        dt_value = dt_util.parse_datetime(str(value).replace(" ", "T"))
        if dt_value is None:
            return None
        if dt_value.tzinfo is None:
            return dt_util.as_local(dt_value.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE))
        return dt_util.as_local(dt_value)
