import cv2
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

    cnr_value = (
        abs(mean_signal - mean_background) / std_background
        if std_background != 0
        else np.nan
    )

    return cnr_value


def compute_roi_resolution(signal_roi):
    """
    Compute spatial resolution using edge detection and frequency analysis.
    This method uses the Edge Spread Function (ESF) and estimates resolution based on frequency content.
    """
    # Apply Sobel filter to detect edges
    edges = cv2.Sobel(signal_roi, cv2.CV_64F, 1, 0, ksize=5)

    # Convert to 1D edge profile by summing along columns
    edge_profile = np.mean(edges, axis=0)

    # Compute Line Spread Function (LSF) using the derivative of ESF
    lsf = np.gradient(edge_profile)

    # Find peak frequencies in the LSF (higher frequencies -> better resolution)
    fft_lsf = np.fft.fft(lsf)
    fft_freqs = np.fft.fftfreq(len(lsf))

    # Find the highest frequency component
    resolution_frequency = np.max(np.abs(fft_lsf))

    return resolution_frequency
