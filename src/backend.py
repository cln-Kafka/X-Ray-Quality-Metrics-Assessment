from PyQt6.QtWidgets import QFileDialog, QMainWindow
import cv2
import numpy as np
from ui import XRaySimulator_Ui
import webbrowser
from skimage import exposure
from matplotlib.widgets import RectangleSelector
import core.metrics_calculation as mc
import core.simulation as sim


class XRaySimulator_Backend(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = XRaySimulator_Ui()
        self.ui.setupUi(self)

        # Parameters
        self.cnr = 0
        self.snr = 0
        self.spatial_resolution = 0
        # Image
        self.file_path = None
        self.imported_image = None
        self.rectangular_roi_image = None
        self.background_roi_image = None
        # Simulation Parameters
        self.noise_value = 0
        self.noise_type = "poisson"
        self.blur_sigma_x = 0
        self.blur_sigma_y = 0
        self.contrast_factor = 0
        self.contrast_method = "gamma"

        # Initialize UI connections
        self.init_UI_connections()

    def init_UI_connections(self):
        # Menus
        self.ui.actionImport_Image.triggered.connect(self.import_image)
        self.ui.actionSynthesize_Image.triggered.connect(self.synthesize_image)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionDocumentation.triggered.connect(self.open_documentation)
        # Controls
        self.ui.evaluate_quality_btn.clicked.connect(self.evaluate_quality)
        # self.ui.simulate_parameters_btn.clicked.connect(self.simulate_parameters)
        self.ui.actionRectangle_ROI.triggered.connect(self.draw_rectangle_roi)
        self.ui.actionReset.triggered.connect(self.reset)
        # Spinboxes and Comboboxes
        self.ui.noise_level_spinbox.valueChanged.connect(self.add_noise)
        self.ui.noise_type_combobox.currentIndexChanged.connect(self.add_noise)
        self.ui.blur_sigma_x_spinbox.valueChanged.connect(self.add_blur)
        self.ui.blur_sigma_y_spinbox.valueChanged.connect(self.add_blur)
        self.ui.contrast_factor_spinbox.valueChanged.connect(self.adjust_contrast)
        self.ui.contrast_method_combobox.currentIndexChanged.connect(
            self.adjust_contrast
        )

    def import_image(self):
        # Open file dialog if file_path is not provided
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "assets/data",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.ppm *.pgm)",
        )

        if self.file_path and isinstance(self.file_path, str):
            # Read the matrix, convert to rgb
            self.imported_image = cv2.imread(self.file_path, 1)
            if self.imported_image is not None:
                self.enable_controls(enabled=True)
                self.preprocess_imported_image()

    def enable_controls(self, enabled=True):
        self.ui.toolBar.setEnabled(enabled)
        self.ui.evaluate_quality_btn.setEnabled(enabled)
        self.ui.quality_metrics_groupBox.setEnabled(enabled)
        self.ui.image_simulator_groupBox.setEnabled(enabled)

    def preprocess_imported_image(self):
        # Convert the image to RGB format
        self.imported_image = cv2.cvtColor(self.imported_image, cv2.COLOR_BGR2RGB)

        # Normalize the image to the range [0, 1]
        self.imported_image = exposure.rescale_intensity(
            self.imported_image, out_range=(0, 1)
        )
        # Display the image
        self.display_image(self.imported_image)

    def display_image(self, image):
        """
        Description:
            - Plots the given image on the canvas
        """
        if image is None:
            return

        self.ui.image_display_figure_canvas.figure.clear()
        ax = self.ui.image_display_figure_canvas.figure.add_subplot(111)

        ax.imshow(image)  # Display the image
        ax.axis("off")
        ax.set_title("Imported X-Ray Image")

        # Adjust layout for better display
        self.ui.image_display_figure_canvas.figure.subplots_adjust(
            left=0.05, right=0.95, bottom=0.05, top=0.95
        )

        # Ensure the updated image is shown
        self.ui.image_display_figure_canvas.draw()

    # Callback function to capture ROI coordinates
    def on_select_rect_roi(self, eclick, erelease):
        x_min, x_max = int(eclick.xdata), int(erelease.xdata)
        y_min, y_max = int(eclick.ydata), int(erelease.ydata)

        # Ensure valid ROI coordinates
        x_min, x_max = sorted((x_min, x_max))
        y_min, y_max = sorted((y_min, y_max))

        # Extract and save the ROI
        self.rectangular_roi_image = self.imported_image[y_min:y_max, x_min:x_max]

        # Create a mask of the same size as the imported image
        self.background_roi_image = self.imported_image.copy()
        self.background_roi_image[y_min:y_max, x_min:x_max] = 0

        # Show the warning label to inform the user
        self.ui.warning_label.setText(
            "[Warning] ROI changed! Please click 'Evaluate Metrics' again."
        )
        self.ui.warning_label.show()

        # Enable or disable the hide button based on ROI existence
        self.ui.actionReset.setEnabled(self.rectangular_roi_image is not None)

    def draw_rectangle_roi(self):
        """
        Description:
            - Allows the user to draw a rectangle on the displayed image and saves the ROI.
            - Only enables drawing if the actionRectangle_ROI button is checked.
            - Re-enables interaction with the existing ROI if it was previously drawn.
        """
        if self.imported_image is None:
            return

        if self.ui.actionRectangle_ROI.isChecked():
            ax = self.ui.image_display_figure_canvas.figure.axes[0]

            # If a RectangleSelector already exists, re-enable it
            if hasattr(self, "rectangle_selector") and self.rectangle_selector:
                self.rectangle_selector.set_active(True)
            else:
                # Create and activate a new RectangleSelector
                self.rectangle_selector = RectangleSelector(
                    ax,
                    self.on_select_rect_roi,
                    useblit=True,
                    button=[1],  # Left mouse button
                    minspanx=5,
                    minspany=5,
                    spancoords="pixels",
                    interactive=True,
                    props=dict(
                        facecolor="#01a28e",
                        edgecolor="white",
                        alpha=0.4,
                        fill=True,
                    ),
                )

            # Refresh canvas to reflect the selector
            self.ui.image_display_figure_canvas.draw()
        else:
            # Disable the RectangleSelector if the button is unchecked
            if hasattr(self, "rectangle_selector") and self.rectangle_selector.active:
                self.rectangle_selector.set_active(False)

    def evaluate_quality(self):
        if self.rectangular_roi_image is None:
            return

        self.cnr = mc.compute_roi_cnr(
            self.rectangular_roi_image,
            self.background_roi_image,
        )
        self.snr = mc.compute_roi_snr(
            self.rectangular_roi_image,
            self.background_roi_image,
        )
        self.spatial_resolution = mc.compute_roi_resolution(
            self.rectangular_roi_image,
        )

        self.ui.cnr_value_label.setText(f"{self.cnr:.2f}")
        self.ui.snr_value_label.setText(f"{self.snr:.2f}")
        self.ui.spatial_resolution_value_label.setText(f"{self.spatial_resolution:.2f}")

        self.ui.warning_label.hide()

    def add_noise(self):
        if self.imported_image is None:
            return

        self.noise_value = self.ui.noise_level_spinbox.value()
        self.noise_type = self.ui.noise_type_combobox.currentText().lower()

        self.imported_image = sim.add_noise(
            image=self.imported_image,
            noise_level=self.noise_value,
            noise_type=self.noise_type,
        )

        # Enable the reset button
        self.ui.actionReset.setEnabled(True)
        # Show the warning
        self.ui.warning_label.setText(
            "[Warning] Noise added! Please click 'Evaluate Metrics' again."
        )
        self.ui.warning_label.show()

        self.display_image(self.imported_image)

    def add_blur(self):
        if self.imported_image is None:
            return

        self.blur_sigma_x = self.ui.blur_sigma_x_spinbox.value()
        self.blur_sigma_y = self.ui.blur_sigma_y_spinbox.value()

        self.imported_image = sim.apply_gaussian_blur(
            image=self.imported_image,
            blur_sigma_x=self.blur_sigma_x,
            blur_sigma_y=self.blur_sigma_y,
        )

        # Enable the reset button
        self.ui.actionReset.setEnabled(True)
        # Show the warning
        self.ui.warning_label.setText(
            "[Warning] Image blurred! Please click 'Evaluate Metrics' again."
        )
        self.ui.warning_label.show()

        self.display_image(self.imported_image)

    def adjust_contrast(self):
        if self.imported_image is None:
            return

        self.contrast_factor = self.ui.contrast_factor_spinbox.value()
        self.contrast_method = self.ui.contrast_method_combobox.currentText().lower()

        self.imported_image = sim.adjust_contrast(
            image=self.imported_image,
            contrast_factor=self.contrast_factor,
            method=self.contrast_method,
        )

        # Enable the reset button
        self.ui.actionReset.setEnabled(True)
        # Show the warning
        self.ui.warning_label.setText(
            "[Warning] Image's contrast was modified! Please click 'Evaluate Metrics' again."
        )
        self.ui.warning_label.show()

        self.display_image(self.imported_image)

    def reset(self):
        """
        Hides the ROI by clearing the RectangleSelector and refreshing the canvas.
        """
        # set the ROI button to unchecked if it is checked
        if self.ui.actionRectangle_ROI.isChecked():
            self.ui.actionRectangle_ROI.setChecked(False)

        if hasattr(self, "rectangle_selector") and self.rectangle_selector:
            # Deactivate and clear the RectangleSelector
            self.rectangle_selector.set_active(False)
            self.rectangle_selector.update()
            self.rectangle_selector = None

        # Clear the ROI data
        self.rectangular_roi_image = None
        self.background_roi_image = None

        # Refresh the canvas to remove the ROI visualization
        self.ui.image_display_figure_canvas.figure.clear()

        # Reset the metrics values, the sliders and labels
        self.ui.cnr_value_label.setText("0.00")
        self.ui.snr_value_label.setText("0.00")
        self.ui.spatial_resolution_value_label.setText("0.00")
        self.ui.noise_level_spinbox.setValue(0)
        self.ui.noise_type_combobox.setCurrentIndex(0)
        self.ui.blur_sigma_x_spinbox.setValue(0)
        self.ui.blur_sigma_y_spinbox.setValue(0)
        self.ui.contrast_factor_spinbox.setValue(0)
        self.ui.contrast_method_combobox.setCurrentIndex(0)

        # Reimport and display the original image from self.file_path
        self.imported_image = cv2.imread(self.file_path, 1)
        self.preprocess_imported_image()

        # Hide the warning label
        self.ui.warning_label.hide()

        # Enable the ROI button and disable the reset button
        self.ui.actionReset.setEnabled(False)

    def synthesize_image(self):
        phantom = np.zeros((256, 256))
        phantom[80:150, 80:150] = 0.5  # Soft tissue
        phantom[100:130, 100:130] = 1.0  # Bone

        self.display_image(phantom)

    def close(self):
        return super().close()

    def open_documentation(self):
        webbrowser.open("https://github.com/cln-Kafka/X-Ray-Task/blob/main/README.md")
