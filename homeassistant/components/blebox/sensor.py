"""BleBox sensor entities."""
from dataclasses import dataclass

from blebox_uniapi.box import Box
import blebox_uniapi.sensor

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BleBoxEntity
from .const import DOMAIN, PRODUCT


@dataclass
class BleboxSensorEntityDescription(SensorEntityDescription):
    """Class describing Blebox sensor entities."""


SENSOR_TYPES = (
    BleboxSensorEntityDescription(
        key="pm1",
        device_class=SensorDeviceClass.PM1,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    BleboxSensorEntityDescription(
        key="pm2_5",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    BleboxSensorEntityDescription(
        key="pm10",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    BleboxSensorEntityDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a BleBox entry."""
    product: Box = hass.data[DOMAIN][config_entry.entry_id][PRODUCT]
    entities = [
        BleBoxSensorEntity(feature) for feature in product.features.get("sensors", [])
    ]
    async_add_entities(entities, True)


class BleBoxSensorEntity(BleBoxEntity[blebox_uniapi.sensor.BaseSensor], SensorEntity):
    """Representation of a BleBox sensor feature."""

    def __init__(self, feature: blebox_uniapi.sensor.BaseSensor) -> None:
        """Initialize a BleBox sensor feature."""
        super().__init__(feature)

        for description in SENSOR_TYPES:
            if description.key == feature.device_class:
                self.entity_description = description
                break

    @property
    def native_value(self):
        """Return the state."""
        return self._feature.native_value
