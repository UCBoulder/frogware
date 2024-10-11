from pylablib.devices.Thorlabs.kinesis import list_kinesis_devices
from seabreeze.spectrometers import Spectrometer as ooSpec
from .device_interfaces import LinearMotor, Spectrometer, DeviceCommsException

from .kinesis import ThorlabsKinesisMotor
from .ocean import OceanOpticsSpectrometer


def connect_devices():
    try:
        motor = ThorlabsKinesisMotor(list_kinesis_devices()[0][0])
        motor.travel_limits_um = (0, 25e6)
    except:
        raise DeviceCommsException('Motor did not connect')
    try:
        spectrometer = OceanOpticsSpectrometer(ooSpec.from_first_available())
    except:
        raise DeviceCommsException('Spectrometer did not connect')
    
    
    return motor, spectrometer
