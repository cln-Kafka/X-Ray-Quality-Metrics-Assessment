from PyQt6.QtWidgets import QFileDialog, QMainWindow
import cv2
from matplotlib import pyplot as plt
import numpy as np
from ui import XRaySimulator_Ui
import webbrowser
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
        self.original_image = None
        self.normalized_image = None
        self.current_image = None
        self.rectangular_roi_image = None
        self.background_roi_image = None
        # Simulation Parameters
        self.mA_value = 200
        self.noise_type = "poisson"
        self.kVp_value = 100
        self.motion_blur_angle = 0
        self.motion_blur_kernel_size = 15
        self.high_pass_filter_radius = 30
        # Constants
        self.ref_mA = 200
        self.ref_kVp = 100

        # Initialize UI connections
        self.init_UI_connections()

    def init_UI_connections(self):
        # Menus
        self.ui.actionImport_Image.triggered.connect(self.import_image)
        self.ui.actionSave_Image.triggered.connect(self.save_simulated_image)
        self.ui.actionSynthesize_Image.triggered.connect(self.synthesize_image)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionDocumentation.triggered.connect(self.open_documentation)
        # Controls
        self.ui.evaluate_quality_btn.clicked.connect(self.evaluate_quality)
        self.ui.simulate_changes_btn.clicked.connect(self.simulate_changes)
        self.ui.actionRectangle_ROI.triggered.connect(self.draw_rectangle_roi)
        self.ui.actionReset.triggered.connect(self.reset)
        # Sliders
        self.ui.motion_blur_kernel_size_slider.valueChanged.connect(
            self.update_motion_kernel_label
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
            self.original_image = cv2.imread(self.file_path, cv2.IMREAD_GRAYSCALE)

            if self.original_image is not None:
                self.enable_controls(enabled=True)
                self.preprocess_imported_image()

    def preprocess_imported_image(self):
        """
        Normalize the image to the range [0, 1] and display it.
        """
        # Ensure the image is in float32 format for proper normalization
        self.original_image = self.original_image.astype(np.float32)

        # Normalize the image to the range [0, 1]
        self.normalized_image = cv2.normalize(
            self.original_image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX
        )

        # Update the current image to the normalized image
        self.current_image = self.normalized_image

        # Display the image
        self.display_image(self.current_image)

    def display_image(self, image):
        """
        Description:
            - Plots the given image on the canvas
        """
        if image is None:
            return

        self.ui.image_display_figure_canvas.figure.clear()
        ax = self.ui.image_display_figure_canvas.figure.add_subplot(111)

        ax.imshow(image, cmap="gray")  # Display the image
        ax.axis("off")
        ax.set_title("Imported X-Ray Image")

        # Adjust layout for better display
        self.ui.image_display_figure_canvas.figure.subplots_adjust(
            left=0.05, right=0.95, bottom=0.05, top=0.95
        )

        # Ensure the updated image is shown
        self.ui.image_display_figure_canvas.draw()

    def on_select_rect_roi(self, eclick, erelease):
        x_min, x_max = int(eclick.xdata), int(erelease.xdata)
        y_min, y_max = int(eclick.ydata), int(erelease.ydata)

        # Ensure valid ROI coordinates
        x_min, x_max = sorted((x_min, x_max))
        y_min, y_max = sorted((y_min, y_max))

        # Extract and save the ROI
        self.rectangular_roi_image = self.current_image[y_min:y_max, x_min:x_max]

        # Create a mask of the same size as the imported image
        self.background_roi_image = self.current_image.copy()
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
        if self.original_image is None:
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

    def simulate_changes(self):
        # Get simulation parameters from UI
        self.mA_value = self.ui.mA_value_spinbox.value()
        self.noise_type_new = self.ui.noise_type_combobox.currentText().lower()
        self.kVp_value = self.ui.kVp_value_spinbox.value()
        self.motion_blur_angle = self.ui.motion_blur_angle_slider.value()
        self.motion_blur_kernel_size = self.ui.motion_blur_kernel_size_slider.value()

        # Make a copy of the normalized image to modify
        simulated_image = (self.normalized_image * 255).astype(np.uint8)

        # Derive noise level from mA: lower mA yields higher noise variance
        noise_std = 0.1 * np.sqrt(self.ref_mA / self.mA_value)

        # Derive contrast factor from kVp: lower kVp increases contrast.
        contrast_factor = self.ref_kVp / self.kVp_value

        # Apply noise
        if self.ui.noise_checkbox.isChecked():
            simulated_image = sim.add_noise(
                simulated_image,
                noise_type=self.noise_type_new,
                noise_factor=noise_std,
            )

        # Apply contrast adjustment
        if self.ui.contrast_checkbox.isChecked():
            simulated_image = sim.adjust_contrast(
                simulated_image, factor=contrast_factor
            )

        # Apply motion blur
        if self.ui.motion_blur_checkbox.isChecked():
            simulated_image = sim.add_motion_blur(
                simulated_image,
                kernel_size=self.motion_blur_kernel_size,
                angle=self.motion_blur_angle,
            )

        # Normalize back to [0, 1] for display
        simulated_image = simulated_image.astype(np.float32) / 255.0

        # Update the current image to the simulated image
        self.current_image = simulated_image

        # Enable the save and reset buttons
        self.ui.actionSave_Image.setEnabled(True)
        self.ui.actionReset.setEnabled(True)
        # Show the warning
        self.ui.warning_label.setText(
            "[Warning] Image's parameters were modified! Please click 'Evaluate Metrics' again."
        )
        self.ui.warning_label.show()

        # Display the simulated image
        self.display_image(self.current_image)

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
        self.ui.mA_value_spinbox.setValue(200)
        self.ui.noise_type_combobox.setCurrentIndex(0)
        self.ui.motion_blur_angle_slider.setValue(0)
        self.ui.motion_blur_kernel_size_slider.setValue(15)
        self.ui.kVp_value_spinbox.setValue(100)

        # Reimport and display the original image from self.file_path
        self.original_image = cv2.imread(self.file_path, 1)
        self.preprocess_imported_image()

        # Hide the warning label
        self.ui.warning_label.hide()

        # Enable the ROI button and disable the reset button
        self.ui.actionReset.setEnabled(False)

    def synthesize_image(self):
        phantom = np.zeros((256, 256))
        phantom[80:150, 80:150] = 0.5  # Soft tissue
        phantom[100:130, 100:130] = 1.0  # Bone

        self.current_image = phantom
        self.enable_controls(True)

        self.display_image(self.current_image)

    def enable_controls(self, enabled=True):
        self.ui.toolBar.setEnabled(enabled)
        self.ui.evaluate_quality_btn.setEnabled(enabled)
        self.ui.quality_metrics_groupBox.setEnabled(enabled)
        self.ui.image_simulator_groupBox.setEnabled(enabled)
        self.ui.simulate_changes_btn.setEnabled(enabled)

    def update_motion_kernel_label(self):
        self.motion_blur_kernel_size = self.ui.motion_blur_kernel_size_slider.value()
        self.ui.motion_blur_kernel_size_label.setText(
            f"Motion Blur Kernel: {self.motion_blur_kernel_size}"
        )

    def close(self):
        return super().close()

    def open_documentation(self):
        webbrowser.open("https://github.com/cln-Kafka/X-Ray-Task/blob/main/README.md")

    def save_simulated_image(self):
        """
        Open a file dialog to save the currently simulated image.
        """
        if self.current_image is None:
            return

        # Convert the image to uint8 for saving
        save_image = (self.current_image * 255).astype(np.uint8)

        # Open file dialog to choose save location
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Simulated Image",
            "simulated_image.png",
            "Image Files (*.png *.jpg *.jpeg *.bmp)",
        )

        if save_path:
            try:
                # Save the image
                cv2.imwrite(save_path, save_image)
                # Optionally, show a success message
                self.ui.warning_label.setText(
                    f"Image saved successfully at {save_path}"
                )
                self.ui.warning_label.show()
            except Exception as e:
                # Show error message if saving fails
                self.ui.warning_label.setText(f"Error saving image: {str(e)}")
                self.ui.warning_label.show()
