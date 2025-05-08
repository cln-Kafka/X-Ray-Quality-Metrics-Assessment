# Parameters

**Noise Level (Dose, kVp, mA)**
- Increasing dose (mA/kVp) reduces noise; decreasing dose increases noise
- Add Poisson noise (quantum noise) or Gaussian noise

**kVp (X-ray Energy)**
- Higher kVp reduces contrast but improves penetration
- Apply a histogram flattening or gamma correction to simulate contrast change

**mA (Tube Current)**
- Higher mA increases signal intensity (less noise)
- Adjust image brightness

**Blurring (Patient Motion, Focal Spot Size, Scattering)**
- Reduces spatial resolution
- Apply motion blur, Gaussian blur, or PSF-based blurring

**Patient Movement**
- Causes motion artifacts (blurring)
- Apply directional motion blur

--------------

# Check
- Quantum noise theory in x-ray imaging: noise variance ∝ sqrt(ref_mA/mA)
- The contrast adjustment scales intensity variations around the mean by a factor of (ref_kVp/kVp), which roughly follows the inverse relationship between kVp and contrast in radiography. However, this is a simplified model that does not consider non-linear effects such as beam hardening or differential tissue attenuation. In reality, contrast in X-ray images depends on tissue attenuation and beam quality, not just the kVp ratio.
Improvement: Introduce a logarithmic attenuation model based on the Beer-Lambert law where μ is the linear attenuation coefficient.

--------------

# Potential References:

Noise: Poisson (Quantum mottle), Gaussian
    - noise factor: 
    - decreasing dose -> decreasing kVp -> increasing noise

Contrast: Gamma Correction
    - contrast factor
    - factor > 1 increases contrast (low kVp effect)
    - factor < 1 decreases contrast (high kVp effect)

Motion Blur: Directional Motion Blur


=========

case 01:
before simulating: 0.09, 1.79, 11.28
simulation (mA: 100 decreased, kVp=100 still, poisson, no motion blur): 0.09, 1.61, 22.39

case 02:
before: 0.35 1.94 10.05
after (400, 100, poisson, no blur): 0.37 1.88 21.99

==========

Apply Motion Blur (Increasing Angle or Kernel Size)
- CNR: Decreases (blurring reduces contrast between structures).
- SNR: No major effect (depends on how motion blur interacts with noise).
- Spatial Resolution: Decreases (blurring reduces sharpness).

Decrease kVp (Lower X-ray Penetration, Higher Subject Contrast)
- CNR: Increases (better tissue contrast).
- SNR: Decreases (less signal due to lower energy).
- Spatial Resolution: No change.

0.07 1.76 14.72
0.06 1.47 36.51
0.07 1.25 64.53
-------
1.32 3.04 0.62
1.33 3.06 0.45
-------
