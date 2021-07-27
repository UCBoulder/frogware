import stellarnet_peter as snp
import matplotlib.pyplot as plt

spec = snp.Spectrometer()
plt.figure()
plt.plot(spec.wl_nm, spec.get_spectrum())
