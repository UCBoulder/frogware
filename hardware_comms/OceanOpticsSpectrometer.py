from device_interfaces import Spectrometer
#TODO Literally everything
class OceanOpticsSpectrometer(Spectrometer):
    """
    This class expects a spectrometer instance. You can incorporate a
    spectrometer and pass it to here by creating a spectrometer class with
    the following attributes and methods:

    methods:

        1. spectrum(): returns wavelengths, intensities

        2. wavelengths(): returns wavelengths

        3. integration_time_micros(integration_time_micros): sets the
        integration time in microseconds


    attributes:

        1. integration_time_micros_limits: [min_int_time_us, max_int_time_us]

    """

    def __init__(self, spectrometer):
        self.spectrometer = spectrometer

        # initialize the integration time and number of scans to average to some value, and then update the actual
        # spectrometer integration time in MainWindow (so the value here doesn't matter)
        self._integration_time_micros = 30000
        self._scans_to_avg = 1

    def get_spectrum(self):
        """
        :return: wavelengths, intensities
        """
        pass
    @property
    def wavelengths(self):
        return self.spectrometer.wavelengths()

    @property
    def integration_time_micros(self):
        return self._integration_time_micros

    @integration_time_micros.setter
    def integration_time_micros(self, value):
        self._integration_time_micros = value
        self.spectrometer.integration_time_micros(self._integration_time_micros)

    @property
    def scans_to_avg(self):
        return self._scans_to_avg

    @scans_to_avg.setter
    
    def scans_to_avg(self, N):
        self._scans_to_avg = N
        self.spectrometer.set_scans_to_average(N)

    @property
    def integration_time_micros_limit(self):
        """
        The Spectrometer class already has a built in function to check that
        you don't set the integration time beyond these limits
        """
        return self.spectrometer.integration_time_micros_limitsclass 