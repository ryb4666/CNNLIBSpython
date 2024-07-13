import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks


class FitGaussian(object):# Fungsi Gaussian
    def gaussian(x, amp, cen, wid):
        return amp * np.exp(-(x - cen) ** 2 / (2 * wid ** 2))

    def read_asc_file(file_path):
        data = np.loadtxt(file_path, skiprows=1)  # Membaca file ASC, melewati baris pertama jika perlu
        wavelength = data[:, 0]
        intensity = data[:, 1]
        return wavelength, intensity
    def estimate_noise(intensity):
        noise = np.std(intensity)
        return noise

    # Fungsi untuk melakukan fitting pada rentang tertentu
    def fit_gaussian_peak(wavelength, intensity, peak_index, window=5, maxfev=5000):
        # Tentukan rentang di sekitar puncak
        start = max(0, peak_index - window)
        end = min(len(wavelength), peak_index + window + 1)

        x = wavelength[start:end]
        y = intensity[start:end]

        # Inisialisasi parameter fitting
        amp_init = max(y)
        cen_init = wavelength[peak_index]
        wid_init = np.std(x)

        # Melakukan fitting dengan Gaussian
        try:
            popt_gaussian, _ = curve_fit(FitGaussian.gaussian, x, y, p0=[amp_init, cen_init, wid_init],
                                         bounds=([0, min(x), 0], [np.inf, max(x), np.inf]), maxfev=maxfev)
        except RuntimeError as e:
            print(f"Fitting gagal untuk puncak di {cen_init:.2f} nm: {e}")
            return x, y, None, None

        fit_gaussian_curve = FitGaussian.gaussian(x, *popt_gaussian)

        return x, y, fit_gaussian_curve, popt_gaussian
    def fit_contoh_gaussian(wavelength, intensity, peak_index, window=5, maxfev=5000):
        if highest_peak_index != -1:
            x_zoom, y_zoom, fit_gaussian_curve_zoom, _ = FitGaussian.fit_gaussian_peak(wavelength, intensity, highest_peak_index)

            plt.figure(figsize=(10, 6))
            plt.plot(x_zoom, y_zoom, 'o', label=f'Data Puncak {wavelength[highest_peak_index]:.2f} nm')
            plt.plot(x_zoom, fit_gaussian_curve_zoom, label=f'Gaussian Fit {wavelength[highest_peak_index]:.2f} nm',
                     color='red')
            plt.xlabel('Panjang Gelombang (nm)')
            plt.ylabel('Intensitas')
            plt.legend()
            plt.title(f'Zoom pada Puncak Tertinggi di {wavelength[highest_peak_index]:.2f} nm')
            plt.xlim(min(x_zoom), max(x_zoom))  # Batasi rentang sumbu x pada plot
            plt.ylim(min(y_zoom), max(y_zoom))  # Batasi rentang sumbu y pada plot
            plt.show()

# File ASC yang akan dibaca
file_path = 'Data/Cu plate_skala 5_D 1 us_1.asc'
# Membaca data spektral dari file ASC
wavelength, intensity = FitGaussian.read_asc_file(file_path)

# Estimasi noise
noise = FitGaussian.estimate_noise(intensity)

# Temukan puncak-puncak dalam spektrum
peaks, properties = find_peaks(intensity, height=noise * 3)  # Hanya puncak dengan S/N >= 3

# Inisialisasi variabel untuk menyimpan puncak tertinggi
highest_peak_intensity = 0
highest_peak_index = -1

plt.figure(figsize=(10, 6))
plt.plot(wavelength, intensity, label='Spektrum LIBS Asli', color='black')

# Lakukan fitting Gaussian untuk setiap puncak yang ditemukan
for peak_index in peaks:
    x, y, fit_gaussian_curve, popt_gaussian = FitGaussian.fit_gaussian_peak(wavelength, intensity, peak_index)

    if fit_gaussian_curve is not None:
        plt.plot(x, y, 'o', label=f'Data Puncak {wavelength[peak_index]:.2f} nm')
        plt.plot(x, fit_gaussian_curve, label=f'Gaussian Fit {wavelength[peak_index]:.2f} nm')

        # Perbarui puncak tertinggi jika intensitas lebih tinggi ditemukan
        if max(y) > highest_peak_intensity:
            highest_peak_intensity = max(y)
            highest_peak_index = peak_index

plt.xlabel('Panjang Gelombang (nm)')
plt.ylabel('Intensitas')
plt.legend()
plt.title('Fitting Gaussian untuk Setiap Puncak dengan S/N >= 3')
plt.show()

# Plot zoom pada puncak tertinggi


FitGaussian.fit_contoh_gaussian(wavelength, intensity, peak_index, window=5, maxfev=5000)