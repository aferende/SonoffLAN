from homeassistant.components.sensor import SensorEntity, \
    STATE_CLASS_MEASUREMENT
from homeassistant.const import *

from .core.const import DOMAIN
from .core.entity import XEntity
from .core.ewelink import XRegistry, SIGNAL_ADD_ENTITIES


async def async_setup_entry(hass, config_entry, add_entities):
    ewelink: XRegistry = hass.data[DOMAIN][config_entry.entry_id]
    ewelink.dispatcher_connect(
        SIGNAL_ADD_ENTITIES,
        lambda x: add_entities([e for e in x if isinstance(e, SensorEntity)])
    )


UNITS = {
    "battery": PERCENTAGE,
    "current": ELECTRIC_CURRENT_AMPERE,
    "humidity": PERCENTAGE,
    "power": POWER_WATT,
    "rssi": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    "temperature": TEMP_CELSIUS,
    "voltage": ELECTRIC_POTENTIAL_VOLT,
}


class XSensor(XEntity, SensorEntity):
    def __init__(self, ewelink: XRegistry, device: dict):
        super().__init__(ewelink, device)

        if self.param in UNITS:
            # by default all sensors with units is measurement sensors
            self._attr_state_class = STATE_CLASS_MEASUREMENT
            self._attr_native_unit_of_measurement = UNITS[self.param]

    def set_state(self, params: dict):
        value = params[self.param]
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                value = None
        self._attr_native_value = value


class XSensor100(XSensor):
    def set_state(self, params: dict):
        self._attr_native_value = round(params[self.param] * 0.01, 2)
