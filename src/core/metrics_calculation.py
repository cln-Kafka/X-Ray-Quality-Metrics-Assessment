import numpy as np


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
