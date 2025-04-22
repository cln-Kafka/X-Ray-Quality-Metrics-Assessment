import numpy as np
import cv2


def add_noise(image, noise_type="poisson", noise_factor=0.1):
    """
    Add noise to an image in grayscale
    Returns: (numpy.ndarray) Noisy image
    """
    # Convert image to grayscale if it's a color image
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    # Convert to float
    gray_image_float = gray_image.astype(np.float32) / 255.0

    # Add noise based on type
    if noise_type.lower() == "gaussian":
        # Generate Gaussian noise
        gaussian_noise = np.random.normal(0, noise_factor, gray_image.shape).astype(
            np.float32
        )
        noisy_image = gray_image_float + gaussian_noise

    elif noise_type.lower() == "poisson":
        # Generate Poisson noise
        noisy_image = np.random.poisson(gray_image_float * (1 / noise_factor)) / (
            1 / noise_factor
        )

    else:
        raise ValueError("Noise type must be 'gaussian' or 'poisson'")

    # Clip values to valid range and convert back to original image type
    noisy_image = np.clip(noisy_image, 0, 1)
    noisy_image = (noisy_image * 255).astype(np.uint8)

    return noisy_image


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
