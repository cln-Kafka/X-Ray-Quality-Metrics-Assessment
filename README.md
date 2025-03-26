# X-Ray-Task

## Requirements

X-Ray Image Quality Metrics
• Compute CNR (Contrast-to-Noise Ratio), SNR (Signal-to-Noise Ratio), and spatial resolution.
• Simulate how changes in system parameters affect these metrics.

## Factors/Parameters
- CNR is affected by
    - kVp
    - ???
- SNR is affected by
- Spatial Resolution is affected by
    - Detector pixel size???

## Real Datasets
- <a href="https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia">Chest X-Ray Pneumonia</a>: JPEG
- <a href="https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation/data">SIIM ACR Pneumothorax Segmentation</a>: Can we find this data?
- <a href="https://cloud.google.com/healthcare-api/docs/resources/public-datasets/nih-chest">NIH Chest X-ray dataset</a>: PNG
- <a href="">NIH Chest</a>
- <a href="https://www.kaggle.com/datasets/nih-chest-xrays/data">NIH Chest X-rays</a>
- <a href="https://stanfordmlgroup.github.io/competitions/mura/">MURA</a>: released as JPEG, DICOM version is hidden I guess

## Papers
- 

## packages & Software

- **From Scratch:**
    - numpy
    - matplotlib: ROI Selection (Rectangle, Circle, inhomogeaneous shapes???) OR automatically detect objects and make regions using thresholds such as OTSU OR more advanced ROI detection such as U-Net.
    - scikit-image: image analysis
    - pydicom, nibabel, etc: loading DICOM images
    - opencv
    - scipy: advanced math (FFT for MTF calculations)

- **Other:**
    - MedPy: Medical Image Processing
    - Mahotas
    - Napari
    - Syris???

## Check and Notes
- Edge Spread Funciton
- Modulation Transfer Function (MTF)
- Spatial Frequency Response
- Simulating noise, blur, ...
- Dose Limit???
- CNR requires two ROIs (e.g. lesion vs. background) and SNR requires a single ROI (e.g. a tissue region).