import numpy as np
import cv2

from core.metrics_calculation import (
    compute_roi_cnr,
    compute_roi_resolution,
    compute_roi_snr,
)


def add_noise(image, noise_type="poisson"):
    """
    Simulate noise due to reduced dose or low kVp. Lower dose means more noise (Poisson/Gaussian)
    - "poisson" simulates quantum noise (low-dose X-rays).
    - "gaussian" simulates electronic noise.
    """
    noisy_image = image.copy().astype(np.float32)

    if noise_type == "poisson":
        noisy_image = np.random.poisson(noisy_image)  # Poisson noise
    elif noise_type == "gaussian":
        noise = np.random.normal(0, 10, image.shape)  # Gaussian noise
        noisy_image += noise

    return np.clip(noisy_image, 0, 255).astype(np.uint8)


def adjust_contrast(image, factor=1.2):
    """
    Simulates contrast change by adjusting gamma correction.
    - factor > 1 increases contrast (low kVp effect)
    - factor < 1 decreases contrast (high kVp effect)
    """
    img_float = image / 255.0
    adjusted = np.power(img_float, factor)
    return (adjusted * 255).astype(np.uint8)


def add_motion_blur(image, kernel_size=15, angle=0):
    """
    Simulates patient movement by applying directional motion blur.
    """
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel = cv2.warpAffine(
        kernel,
        cv2.getRotationMatrix2D((kernel_size / 2, kernel_size / 2), angle, 1.0),
        (kernel_size, kernel_size),
    )
    kernel /= kernel_size
    return cv2.filter2D(image, -1, kernel)


def apply_highpass_filter(image):
    """
    Simulates high-pass filtering (removing low frequencies) to mimic X-ray filtering.
    Higher kVp reduces beam hardening artifacts.
    """
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    r = 30  # Radius of low frequencies to remove
    mask[crow - r : crow + r, ccol - r : ccol + r] = 0  # Block low frequencies

    dft_shift *= mask
    dft = np.fft.ifftshift(dft_shift)
    filtered_image = np.abs(np.fft.ifft2(dft))

    return np.clip(filtered_image, 0, 255).astype(np.uint8)
