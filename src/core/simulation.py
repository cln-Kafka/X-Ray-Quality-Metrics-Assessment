import numpy as np
from scipy.ndimage import gaussian_filter


def add_noise(image, noise_level, noise_type="gaussian"):
    """Add Gaussian or Poisson noise to the image."""
    if noise_type == "gaussian":
        noisy_image = image + np.random.normal(0, noise_level, image.shape)
    elif noise_type == "poisson":
        noisy_image = np.random.poisson(image * noise_level) / noise_level
    else:
        raise ValueError("Invalid noise_type. Use 'gaussian' or 'poisson'.")

    return np.clip(noisy_image, 0, 1)


def apply_gaussian_blur(image, blur_sigma_x=1.0, blur_sigma_y=None):
    """Apply Gaussian blur with optional anisotropic control."""
    if blur_sigma_y is None:
        blur_sigma_y = blur_sigma_x

    return gaussian_filter(image, sigma=(blur_sigma_x, blur_sigma_y))


def adjust_contrast(image, contrast_factor, method="linear"):
    """Adjust contrast using either linear scaling or gamma correction."""
    if method == "linear":
        mean_value = np.mean(image)
        adjusted_image = mean_value + contrast_factor * (image - mean_value)
    elif method == "gamma":
        gamma = 1.0 / contrast_factor if contrast_factor > 0 else 1.0
        adjusted_image = np.power(image, gamma)
    else:
        raise ValueError("Invalid method. Use 'linear' or 'gamma'.")

    return np.clip(adjusted_image, 0, 1)
