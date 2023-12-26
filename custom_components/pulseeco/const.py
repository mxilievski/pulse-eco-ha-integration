"""Constants for the Pulse.eco integration."""

from pulseeco import DataValueType

from homeassistant.components.sensor import SensorDeviceClass

DOMAIN = "pulseeco"


SENSOR_TYPE_MAPPING = {
    DataValueType.PM10: SensorDeviceClass.PM10,
    DataValueType.PM25: SensorDeviceClass.PM25,
    DataValueType.PRESSURE: SensorDeviceClass.PRESSURE,
    DataValueType.TEMPERATURE: SensorDeviceClass.TEMPERATURE,
    DataValueType.HUMIDITY: SensorDeviceClass.HUMIDITY,
    DataValueType.O3: SensorDeviceClass.OZONE,
    DataValueType.NOISE_DBA: SensorDeviceClass.SOUND_PRESSURE,
    DataValueType.NOISE: SensorDeviceClass.SOUND_PRESSURE,
    DataValueType.GAS_RESISTANCE: SensorDeviceClass.GAS,
    "so2": SensorDeviceClass.SULPHUR_DIOXIDE,
}
