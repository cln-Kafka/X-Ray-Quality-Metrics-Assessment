"""
Helper Functions to Compute Metrics for an ROI with Background as the Rest of the Image
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import exposure
from scipy.ndimage import gaussian_filter
import ipywidgets as widgets
from ipywidgets import interact


def compute_roi_snr(signal_roi, background_pixels):
    """
    Compute SNR as the ratio of the mean signal in the signal ROI
    to the standard deviation of the background (all pixels outside the ROI).
    """
    mean_signal = np.mean(signal_roi)
    std_background = np.std(background_pixels)
    return mean_signal / std_background if std_background != 0 else np.nan


def compute_roi_cnr(signal_roi, background_pixels):
    """
    Compute CNR as the difference between the signal and background means,
    divided by the standard deviation of the background.
    """
    mean_signal = np.mean(signal_roi)
    mean_background = np.mean(background_pixels)
    std_background = np.std(background_pixels)
    return (
        (mean_signal - mean_background) / std_background
        if std_background != 0
        else np.nan
    )


def compute_roi_resolution(signal_roi):
    """
    Compute a global measure of spatial resolution via Fourier analysis on the signal ROI.
    A sharper image tends to have more high-frequency content.
    Here we use the mean magnitude of the shifted Fourier spectrum as a rough indicator.
    """
    fft_image = np.fft.fft2(signal_roi)
    fft_shifted = np.fft.fftshift(fft_image)
    magnitude_spectrum = np.abs(fft_shifted)
    return np.mean(magnitude_spectrum)


# ----- Load and Normalize the Image -----
img = Image.open(
    "/home/kareem-noureddine/Work/GitHub_Repos/X-Ray-Task/testing_environment/assets/data/person1000_bacteria_2931.jpeg"
).convert("L")
image = np.array(img, dtype=np.float32)
image_norm = exposure.rescale_intensity(image, out_range=(0, 1))
rows, cols = image_norm.shape


def update_simulation(
    noise_level=0.1,
    blur_sigma=3,
    contrast_factor=1.0,
    signal_x=50,
    signal_y=50,
    signal_width=200,
    signal_height=200,
):
    # --- Apply simulation to the entire image ---
    # Step 1: Add synthetic Gaussian noise
    noisy_image = image_norm + np.random.normal(0, noise_level, image_norm.shape)
    noisy_image = np.clip(noisy_image, 0, 1)

    # Step 2: Apply Gaussian blur
    blurred_image = gaussian_filter(noisy_image, sigma=blur_sigma)

    # Step 3: Adjust contrast (scaling differences from the mean intensity)
    mean_val = np.mean(blurred_image)
    adjusted_image = mean_val + contrast_factor * (blurred_image - mean_val)
    adjusted_image = np.clip(adjusted_image, 0, 1)

    # --- Extract Signal ROI ---
    signal_x = int(np.clip(signal_x, 0, cols - 1))
    signal_y = int(np.clip(signal_y, 0, rows - 1))
    signal_width = int(np.clip(signal_width, 10, cols - signal_x))
    signal_height = int(np.clip(signal_height, 10, rows - signal_y))

    signal_roi = adjusted_image[
        signal_y : signal_y + signal_height, signal_x : signal_x + signal_width
    ]

    # Define background as all pixels outside the signal ROI
    mask = np.ones_like(adjusted_image, dtype=bool)
    mask[signal_y : signal_y + signal_height, signal_x : signal_x + signal_width] = (
        False
    )
    background_pixels = adjusted_image[mask]

    # Compute metrics
    snr = compute_roi_snr(signal_roi, background_pixels)
    cnr = compute_roi_cnr(signal_roi, background_pixels)
    resolution = compute_roi_resolution(signal_roi)

    # --- Visualization ---
    fig, ax = plt.subplots(2, 2, figsize=(18, 12))

    # Show full original image with signal ROI overlay
    ax[0, 0].imshow(image_norm, cmap="gray")
    ax[0, 0].set_title("Original Normalized Image")
    rect_orig = plt.Rectangle(
        (signal_x, signal_y),
        signal_width,
        signal_height,
        edgecolor="red",
        facecolor="none",
        linewidth=2,
        label="Signal ROI",
    )
    ax[0, 0].add_patch(rect_orig)
    ax[0, 0].legend()
    ax[0, 0].axis("off")

    # Show full simulated image with signal ROI overlay
    ax[0, 1].imshow(adjusted_image, cmap="gray")
    ax[0, 1].set_title(
        f"Simulated Image\nNoise: {noise_level}, Blur: {blur_sigma}, Contrast: {contrast_factor}"
    )
    rect_sim = plt.Rectangle(
        (signal_x, signal_y),
        signal_width,
        signal_height,
        edgecolor="red",
        facecolor="none",
        linewidth=2,
    )
    ax[0, 1].add_patch(rect_sim)
    ax[0, 1].axis("off")

    # Zoom-in on Signal ROI from simulated image
    ax[1, 0].imshow(signal_roi, cmap="gray")
    ax[1, 0].set_title("Signal ROI (Simulated)")
    ax[1, 0].axis("off")

    # Zoom-in on Background: Display the background mask overlay on the simulated image
    # (Here we show the simulated image with the signal ROI masked out)
    background_image = adjusted_image.copy()
    background_image[~mask] = 0  # set signal ROI area to 0 for visualization
    ax[1, 1].imshow(background_image, cmap="gray")
    ax[1, 1].set_title("Background (Rest of Image)")
    ax[1, 1].axis("off")

    plt.tight_layout()
    plt.show()

    # Print computed metrics for the Signal ROI with background as the rest of the image
    print("Computed Metrics on Signal ROI (Background = rest of image):")
    print(f"  SNR: {snr:.2f}")
    print(f"  CNR: {cnr:.2f}")
    print(f"  Spatial Resolution (mean FT magnitude): {resolution:.2f}")