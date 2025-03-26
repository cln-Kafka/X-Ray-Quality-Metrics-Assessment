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

**Exposure Time**
- Affects noise (longer time = less noise)
- Same as noise simulation

**Filters (Beam Hardening, Grid, Post-Processing)**
- Reduces scatter, affects contrast
- Apply high-pass or low-pass filters

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
