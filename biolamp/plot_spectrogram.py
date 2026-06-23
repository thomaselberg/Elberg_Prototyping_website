import numpy as np
import matplotlib.pyplot as plt
import os

# Wavelengths from 300nm to 2000nm
wavelengths = np.linspace(300, 2000, 1000)
wl_m = wavelengths * 1e-9 # meters

# Constants
h = 6.626e-34
c = 3e8
k = 1.38e-23

def planck(wl, T):
    a = 2.0 * h * c**2
    b = h * c / (wl * k * T)
    return a / (np.power(wl, 5) * (np.exp(b) - 1.0))

sun_intensity = planck(wl_m, 5778)
sun_normalized = sun_intensity / np.max(sun_intensity)

halogen_intensity = planck(wl_m, 2900)
halogen_normalized = halogen_intensity / np.max(halogen_intensity)

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

led_intensity = 0.8 * gaussian(wavelengths, 450, 12) + 1.0 * gaussian(wavelengths, 560, 45)
led_intensity[wavelengths > 800] = 0
led_normalized = led_intensity / np.max(led_intensity)

# Plotting
plt.figure(figsize=(10, 6), facecolor='#101213')
ax = plt.axes()
ax.set_facecolor('#101213')

# Plot lines
plt.plot(wavelengths, sun_normalized, color='#f2cf5b', label='Sol (~5778K)', linewidth=2.5)
plt.plot(wavelengths, halogen_normalized, color='#e5b085', label='Halogen (~2900K)', linewidth=2.5)
plt.plot(wavelengths, led_normalized, color='#a0c4ff', label='Hvid LED', linewidth=2.5)

# Rainbow visible light on X-axis
vis_wavelengths = np.linspace(380, 750, 400)
def wavelength_to_rgb(wavelength):
    gamma = 0.8
    intensity_max = 255
    factor = 0.0
    R = G = B = 0

    if (wavelength >= 380) and (wavelength < 440):
        R = -(wavelength - 440) / (440 - 380); G = 0.0; B = 1.0
    elif (wavelength >= 440) and (wavelength < 490):
        R = 0.0; G = (wavelength - 440) / (490 - 440); B = 1.0
    elif (wavelength >= 490) and (wavelength < 510):
        R = 0.0; G = 1.0; B = -(wavelength - 510) / (510 - 490)
    elif (wavelength >= 510) and (wavelength < 580):
        R = (wavelength - 510) / (580 - 510); G = 1.0; B = 0.0
    elif (wavelength >= 580) and (wavelength < 645):
        R = 1.0; G = -(wavelength - 645) / (645 - 580); B = 0.0
    elif (wavelength >= 645) and (wavelength <= 780):
        R = 1.0; G = 0.0; B = 0.0

    if (wavelength >= 380) and (wavelength < 420): factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif (wavelength >= 420) and (wavelength < 700): factor = 1.0
    elif (wavelength >= 700) and (wavelength <= 780): factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    return [int(intensity_max * ((R * factor) ** gamma))/255.0, int(intensity_max * ((G * factor) ** gamma))/255.0, int(intensity_max * ((B * factor) ** gamma))/255.0]

colors = [wavelength_to_rgb(wl) for wl in vis_wavelengths]
plt.vlines(vis_wavelengths, -0.02, 0.02, colors=colors, alpha=0.8, linewidth=1.5)
plt.text(565, 0.04, 'Synligt Lys', color='#ffffff', fontsize=11, ha='center')

# Annotations for IR and NIR
plt.axvline(750, color='#333333', linestyle='--', linewidth=1)
plt.axvline(1400, color='#333333', linestyle='--', linewidth=1)
plt.text(1075, 0.5, 'Terapeutisk NIR\n(Near Infrared)', color='#ff6b6b', fontsize=11, ha='center', va='center', alpha=0.9)
plt.text(1700, 0.5, 'Terapeutisk IR\n(Infrared)', color='#ff6b6b', fontsize=11, ha='center', va='center', alpha=0.9)

# Aesthetics
plt.title('Spektral Energi Fordeling', color='#f2f2f2', fontsize=18, pad=20, fontname='sans-serif')
plt.xlabel('Bølgelængde (nm)', color='#a0a0a0', fontsize=13)
plt.ylabel('Normaliseret Intensitet', color='#a0a0a0', fontsize=13)

ax.spines['bottom'].set_color('#333333')
ax.spines['left'].set_color('#333333')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', colors='#a0a0a0')
ax.tick_params(axis='y', colors='#a0a0a0')

plt.xlim(300, 2000)
plt.ylim(-0.02, 1.05)

# Legend without the axvspan rectangles
legend = plt.legend(loc='upper right', frameon=False, labelcolor='#f2f2f2', fontsize=11)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'spectrogram.png')
plt.savefig(output_path, dpi=300, facecolor='#101213', edgecolor='none')
print(f"Successfully generated {output_path}")
