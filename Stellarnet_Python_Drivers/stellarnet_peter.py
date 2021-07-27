import stellarnet_driver3 as sn


class Spectrometer:
    def __init__(self):
        self.spec, self.wl_nm = sn.array_get_spec(0)

    def print_info(self):
        self.spec['device'].print_info()

    def set_config(self, int_time_ms, scans_to_avg=1, x_smooth=1):
        self.spec['device'].set_config(int_time=int_time_ms,
                                       scans_to_avg=scans_to_avg,
                                       x_smooth=x_smooth)

    def get_spectrum(self):
        return sn.array_spectrum(self.spec, self.wl_nm)[:, 1]
