import seabreeze.cseabreeze
from .device_interfaces import Spectrometer, SpectrometerIntegrationException, SpectrometerAverageException
from seabreeze.spectrometers import Spectrometer as ooSpec
import numpy as np
import seabreeze
seabreeze.use('pyseabreeze')
class OceanOpticsSpectrometer(Spectrometer):
    def __init__(self, spectrometer: ooSpec):
        self.spectrometer = spectrometer
        # initialize the integration time and number of scans to average to some value, and then update the actual
        # spectrometer integration time in MainWindow (so the value here doesn't matter)
        self.integration_time_micros = 30000
        self.scans_to_avg = 1

    def intensities(self): 
        return self.spectrometer.intensities()

    def wavelengths(self):
        return self.spectrometer.wavelengths()
    
    def spectrum(self):
        return self.spectrometer.spectrum()

    @property
    def integration_time_micros(self):
        if self._integration_time_micros is None:
            raise SpectrometerIntegrationException('''Spectrometer integration time 
                                                   not initialized''')
        return self._integration_time_micros

    @integration_time_micros.setter
    def integration_time_micros(self, value):
        if not(self.integration_time_micros_limit[0] <= value <= self.integration_time_micros_limit[1]):
            raise SpectrometerIntegrationException('''Integration time exceeds limits''')
        else:
            self._integration_time_micros = value
            self.spectrometer.integration_time_micros(value)

    @property
    def scans_to_avg(self):
        return self._scans_to_avg

    '''
    Only works when using cseabreeze backend (provided by Ocean Optics)
    '''
    @scans_to_avg.setter
    def scans_to_avg(self, N: int):
        if N <= 0:
            raise SpectrometerAverageException("Spectrometer must average at least 1 scan")
        else:
            self._scans_to_avg = N
            #TODO doesn't work 
            # self.spectrometer.f.spectrum_processing.set_scans_to_average(N)

    @property
    def integration_time_micros_limit(self):
        return self.spectrometer.integration_time_micros_limits

        
# if __name__ == "__main__":
#     import seabreeze
#     seabreeze.use('pyseabreeze')
#     raw_spec=ooSpec.from_first_available()
#     spec = OceanOpticsSpectrometer(raw_spec)
#     print(spec.wavelengths())
#     print(spec.integration_time_micros_limit)
#     print(raw_spec.pixels)
#     print(raw_spec.intensities())
    