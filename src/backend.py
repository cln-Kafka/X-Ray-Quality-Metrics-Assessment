from PyQt6.QtWidgets import QFileDialog, QMainWindow
import cv2
import matplotlib.pyplot as plt
from x_ray_simulator_ui import XRaySimulator_Ui
import webbrowser
from matplotlib.widgets import RectangleSelector


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

        # Initialize UI connections
        self.init_UI_connections()

    def init_UI_connections(self):
        # Menus
        self.ui.actionImport_Image.triggered.connect(self.import_image)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionDocumentation.triggered.connect(self.open_documentation)
        # Controls
        self.ui.evaluate_quality_btn.clicked.connect(self.evaluate_quality)
        self.ui.simulate_parameters_btn.clicked.connect(self.simulate_parameters)
        self.ui.actionRectangle_ROI.triggered.connect(self.draw_rectangle_roi)

    def import_image(self):
        # Open file dialog if file_path is not provided
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "Images",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.ppm *.pgm)",
        )

        if self.file_path and isinstance(self.file_path, str):
            # Read the matrix, convert to rgb
            self.imported_image = cv2.imread(self.file_path, 1)
            self.imported_image = cv2.cvtColor(self.imported_image, cv2.COLOR_BGR2RGB)
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

    def draw_rectangle_roi(self):
        """
        Description:
            - Allows the user to draw a rectangle on the displayed image and saves the ROI.
            - Only enables drawing if the actionRectangle_ROI button is checked.
        """
        if self.imported_image is None:
            return

        if self.ui.actionRectangle_ROI.isChecked():
            ax = self.ui.image_display_figure_canvas.figure.axes[0]

            # Create and activate the RectangleSelector
            self.rectangle_selector = RectangleSelector(
                ax,
                self.on_select_rect_roi,
                useblit=True,
                button=[1],  # Left mouse button
                minspanx=5,
                minspany=5,
                spancoords="pixels",
                interactive=True,
            )

            # Refresh canvas to reflect the selector
            self.ui.image_display_figure_canvas.draw()
        else:
            # Disable the RectangleSelector if the button is unchecked
            if hasattr(self, "rectangle_selector") and self.rectangle_selector.active:
                self.rectangle_selector.set_active(False)

    def evaluate_quality(self):
        pass

    def simulate_parameters(self):
        pass

    def close(self):
        return super().close()

    def open_documentation(self):
        webbrowser.open("https://github.com/cln-Kafka/X-Ray-Task/blob/main/README.md")
