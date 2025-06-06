from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class XRaySimulator_Ui(object):
    def setupUi(self, XRaySimulator_mainwindow: QtWidgets.QMainWindow):
        XRaySimulator_mainwindow.setObjectName("XRaySimulator_Ui")
        XRaySimulator_mainwindow.setFixedSize(618, 890)
        XRaySimulator_mainwindow.setWindowIcon(
            QtGui.QIcon("assets/icons/x-ray-simulator-app-icon.png")
        )
        # Apply custom styles
        custom_stylesheet = """
        QSpinBox, QComboBox, QDoubleSpinBox, QSlider {
            selection-background-color: #01a28e; /* Change highlight color */
        }
        """
        XRaySimulator_mainwindow.setStyleSheet(custom_stylesheet)

        self.centralwidget = QtWidgets.QWidget(parent=XRaySimulator_mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_vlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_widget_vlayout.setObjectName("central_widget_vlayout")
        self.central_widget_vlayout.setContentsMargins(9, 0, 9, 9)
        self.warning_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.warning_label.setEnabled(True)
        self.warning_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.warning_label.setStyleSheet("background-color: #F94944; color: white;")
        self.warning_label.setIndent(4)
        self.warning_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
            | QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.warning_label.setObjectName("warning_label")
        self.warning_label.hide()
        self.central_widget_vlayout.addWidget(self.warning_label)
        self.image_display_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.image_display_frame.setMinimumSize(QtCore.QSize(600, 600))
        self.image_display_frame.setMaximumSize(QtCore.QSize(600, 600))
        self.image_display_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.image_display_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.image_display_frame.setObjectName("image_display_frame")
        self.central_widget_vlayout.addWidget(self.image_display_frame)
        self.controls_hlayout = QtWidgets.QHBoxLayout()
        self.controls_hlayout.setObjectName("controls_hlayout")
        self.image_simulator_section_vlayout = QtWidgets.QVBoxLayout()
        self.image_simulator_section_vlayout.setObjectName(
            "image_simulator_section_vlayout"
        )
        self.image_simulator_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.image_simulator_groupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_simulator_groupBox.setObjectName("image_simulator_groupBox")
        self.image_simulator_groupBox.setEnabled(False)
        self.image_simulator_groupbox_gridlayout = QtWidgets.QGridLayout(
            self.image_simulator_groupBox
        )
        self.image_simulator_groupbox_gridlayout.setObjectName(
            "image_simulator_groupbox_gridlayout"
        )

        ##### =========== Labels =========== #####
        self.mA_value_label = QtWidgets.QLabel(parent=self.image_simulator_groupBox)
        self.mA_value_label.setObjectName("mA_value_label")
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.mA_value_label, 0, 0, 1, 1
        )

        self.noise_type_label = QtWidgets.QLabel(parent=self.image_simulator_groupBox)
        self.noise_type_label.setObjectName("noise_type_label")
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.noise_type_label, 0, 2, 1, 1
        )

        self.kVp_value_label = QtWidgets.QLabel(parent=self.image_simulator_groupBox)
        self.kVp_value_label.setObjectName("kVp_value_label")
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.kVp_value_label, 1, 0, 1, 1
        )

        self.motion_blur_kernel_size_label = QtWidgets.QLabel(
            parent=self.image_simulator_groupBox
        )
        self.motion_blur_kernel_size_label.setObjectName("motion_blur_kernel_size")
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.motion_blur_kernel_size_label, 1, 2, 1, 1
        )

        self.motion_blur_angle_label = QtWidgets.QLabel(
            parent=self.image_simulator_groupBox
        )
        self.motion_blur_angle_label.setObjectName("method_blur_angle_label")
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.motion_blur_angle_label, 2, 0, 1, 1
        )

        ##### =========== Spinboxes and Comboboxes =========== #####
        self.mA_value_spinbox = QtWidgets.QSpinBox(parent=self.image_simulator_groupBox)
        self.mA_value_spinbox.setObjectName("mA_value_spinbox")
        self.mA_value_spinbox.setValue(200)
        self.mA_value_spinbox.setMinimum(10)
        self.mA_value_spinbox.setMaximum(600)
        self.mA_value_spinbox.setSingleStep(1)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.mA_value_spinbox, 0, 1, 1, 1
        )

        self.noise_type_combobox = QtWidgets.QComboBox(
            parent=self.image_simulator_groupBox
        )
        self.noise_type_combobox.setObjectName("noise_type_combobox")
        self.noise_type_combobox.addItem("Poisson")
        self.noise_type_combobox.addItem("Gaussian")
        self.noise_type_combobox.setCurrentIndex(0)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.noise_type_combobox, 0, 3, 1, 1
        )

        self.kVp_value_spinbox = QtWidgets.QSpinBox(
            parent=self.image_simulator_groupBox
        )
        self.kVp_value_spinbox.setObjectName("kVp_value_spinbox")
        self.kVp_value_spinbox.setValue(40)
        self.kVp_value_spinbox.setMinimum(5)
        self.kVp_value_spinbox.setMaximum(200)
        self.kVp_value_spinbox.setSingleStep(1)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.kVp_value_spinbox, 1, 1, 1, 1
        )

        self.motion_blur_kernel_size_slider = QtWidgets.QSlider(
            parent=self.image_simulator_groupBox
        )
        self.motion_blur_kernel_size_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.motion_blur_kernel_size_slider.setObjectName(
            "motion_blur_kernel_size_slider"
        )
        self.motion_blur_kernel_size_slider.setValue(15)
        self.motion_blur_kernel_size_slider.setMinimum(3)
        self.motion_blur_kernel_size_slider.setMaximum(30)
        self.motion_blur_kernel_size_slider.setSingleStep(2)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.motion_blur_kernel_size_slider, 1, 3, 1, 1
        )

        self.motion_blur_angle_slider = QtWidgets.QSpinBox(
            parent=self.image_simulator_groupBox
        )
        self.motion_blur_angle_slider.setObjectName("motion_blur_angle_slider")
        self.motion_blur_angle_slider.setValue(0)
        self.motion_blur_angle_slider.setMinimum(0)
        self.motion_blur_angle_slider.setMaximum(360)
        self.motion_blur_angle_slider.setSingleStep(5)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.motion_blur_angle_slider, 2, 1, 1, 1
        )

        # Checkboxes
        self.noise_checkbox = QtWidgets.QCheckBox("Noise")
        self.noise_checkbox.setChecked(False)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.noise_checkbox, 3, 0, 1, 1
        )
        self.contrast_checkbox = QtWidgets.QCheckBox("Contrast")
        self.contrast_checkbox.setChecked(False)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.contrast_checkbox, 3, 1, 1, 1
        )
        self.motion_blur_checkbox = QtWidgets.QCheckBox("Motion Blur")
        self.motion_blur_checkbox.setChecked(False)
        self.image_simulator_groupbox_gridlayout.addWidget(
            self.motion_blur_checkbox, 3, 2, 1, 2
        )

        self.image_simulator_section_vlayout.addWidget(self.image_simulator_groupBox)

        self.simulate_changes_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.simulate_changes_btn.setObjectName("simulate_changes_btn")
        self.simulate_changes_btn.setEnabled(False)
        self.simulate_changes_btn.setStyleSheet(
            """
            QPushButton:enabled {
                background-color: #01a28e; /* Enabled background color */
                color: white; /* Enabled text color */
                font-weight: bold;
            }
            """
        )
        self.image_simulator_section_vlayout.addWidget(self.simulate_changes_btn)

        self.controls_hlayout.addLayout(self.image_simulator_section_vlayout)
        self.metrics_section_vlayout = QtWidgets.QVBoxLayout()
        self.metrics_section_vlayout.setObjectName("metrics_section_vlayout")
        self.quality_metrics_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.quality_metrics_groupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.quality_metrics_groupBox.setObjectName("quality_metrics_groupBox")
        self.quality_metrics_groupBox.setEnabled(False)
        self.quality_metrics_groupbox_gridLayout = QtWidgets.QGridLayout(
            self.quality_metrics_groupBox
        )
        self.quality_metrics_groupbox_gridLayout.setObjectName(
            "quality_metrics_groupbox_gridLayout"
        )
        self.cnr_label = QtWidgets.QLabel(parent=self.quality_metrics_groupBox)
        self.cnr_label.setObjectName("cnr_label")
        self.quality_metrics_groupbox_gridLayout.addWidget(self.cnr_label, 0, 0, 1, 1)
        self.cnr_value_label = QtWidgets.QLabel(parent=self.quality_metrics_groupBox)
        self.cnr_value_label.setObjectName("cnr_value_label")
        self.quality_metrics_groupbox_gridLayout.addWidget(
            self.cnr_value_label, 0, 1, 1, 1
        )
        self.snr_label = QtWidgets.QLabel(parent=self.quality_metrics_groupBox)
        self.snr_label.setObjectName("snr_label")
        self.quality_metrics_groupbox_gridLayout.addWidget(self.snr_label, 1, 0, 1, 1)
        self.snr_value_label = QtWidgets.QLabel(parent=self.quality_metrics_groupBox)
        self.snr_value_label.setObjectName("snr_value_label")
        self.quality_metrics_groupbox_gridLayout.addWidget(
            self.snr_value_label, 1, 1, 1, 1
        )
        self.spatial_resolution_label = QtWidgets.QLabel(
            parent=self.quality_metrics_groupBox
        )
        self.spatial_resolution_label.setObjectName("spatial_resolution_label")
        self.quality_metrics_groupbox_gridLayout.addWidget(
            self.spatial_resolution_label, 2, 0, 1, 1
        )
        self.spatial_resolution_value_label = QtWidgets.QLabel(
            parent=self.quality_metrics_groupBox
        )
        self.spatial_resolution_value_label.setObjectName(
            "spatial_resolution_value_label"
        )
        self.quality_metrics_groupbox_gridLayout.addWidget(
            self.spatial_resolution_value_label, 2, 1, 1, 1
        )
        self.metrics_section_vlayout.addWidget(self.quality_metrics_groupBox)
        self.evaluate_quality_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.evaluate_quality_btn.setObjectName("evaluate_quality_btn")
        self.evaluate_quality_btn.setEnabled(False)
        self.evaluate_quality_btn.setStyleSheet(
            """
            QPushButton:enabled {
                background-color: #01a28e; /* Enabled background color */
                color: white; /* Enabled text color */
                font-weight: bold;
            }
            """
        )
        self.metrics_section_vlayout.addWidget(self.evaluate_quality_btn)
        self.controls_hlayout.addLayout(self.metrics_section_vlayout)
        self.central_widget_vlayout.addLayout(self.controls_hlayout)
        XRaySimulator_mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=XRaySimulator_mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        XRaySimulator_mainwindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=XRaySimulator_mainwindow)
        self.statusbar.setObjectName("statusbar")
        XRaySimulator_mainwindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=XRaySimulator_mainwindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setEnabled(False)
        XRaySimulator_mainwindow.addToolBar(
            QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar
        )
        self.actionRectangle_ROI = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionRectangle_ROI.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("assets/icons/rectangle_roi.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionRectangle_ROI.setIcon(icon)
        self.actionRectangle_ROI.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionRectangle_ROI.setObjectName("actionRectangle_ROI")
        self.actionImport_Image = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionImport_Image.setObjectName("actionImport_Image")
        self.actionSave_Image = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionSynthesize_Image = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionSynthesize_Image.setObjectName("actionSynthesize_Image")
        self.actionExit = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDocumentation = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionReset = QtGui.QAction(parent=XRaySimulator_mainwindow)
        self.actionReset.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("assets/icons/reset.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionReset.setIcon(icon1)
        self.actionReset.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionReset.setObjectName("actionReset")
        self.menuFile.addAction(self.actionImport_Image)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionSynthesize_Image)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionRectangle_ROI)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionReset)

        # Create the matplotlib canvas inside the frame
        self.image_display_frame_vlayout = QtWidgets.QVBoxLayout(
            self.image_display_frame
        )
        self.image_display_frame_vlayout.setObjectName("image_display_frame_vlayout")
        self.image_display_figure = plt.figure()
        self.image_display_figure_canvas = FigureCanvas(self.image_display_figure)
        self.image_display_frame_vlayout.addWidget(self.image_display_figure_canvas)

        self.retranslateUi(XRaySimulator_mainwindow)
        QtCore.QMetaObject.connectSlotsByName(XRaySimulator_mainwindow)

    def retranslateUi(self, XRaySimulator_Ui):
        _translate = QtCore.QCoreApplication.translate
        XRaySimulator_Ui.setWindowTitle(
            _translate("XRaySimulator_Ui", "XRaySimulator_Ui")
        )
        self.warning_label.setText(
            _translate(
                "XRaySimulator_Ui",
                "[Warning] ROI changed! Please click 'Evaluate Metrics' again.",
            )
        )
        self.image_simulator_groupBox.setTitle(
            _translate("XRaySimulator_Ui", "Image Simulator")
        )

        self.mA_value_label.setText(_translate("XRaySimulator_Ui", "mA value"))

        self.noise_type_label.setText(_translate("XRaySimulator_Ui", "Noise Type"))
        self.motion_blur_kernel_size_label.setText(
            _translate("XRaySimulator_Ui", "Motion Blur Kernel: 15")
        )
        self.motion_blur_angle_label.setText(
            _translate("XRaySimulator_Ui", "Motion Blur Angle")
        )
        self.kVp_value_label.setText(_translate("XRaySimulator_Ui", "kVp value"))
        self.simulate_changes_btn.setText(
            _translate("XRaySimulator_Ui", "Simulate Changes")
        )
        self.quality_metrics_groupBox.setTitle(
            _translate("XRaySimulator_Ui", "Quality Metrics")
        )
        self.cnr_label.setText(_translate("XRaySimulator_Ui", "CNR"))
        self.cnr_value_label.setText(_translate("XRaySimulator_Ui", "0.00"))
        self.snr_label.setText(_translate("XRaySimulator_Ui", "SNR"))
        self.snr_value_label.setText(_translate("XRaySimulator_Ui", "0.00"))
        self.spatial_resolution_label.setText(
            _translate("XRaySimulator_Ui", "Spatial Resolution")
        )
        self.spatial_resolution_value_label.setText(
            _translate("XRaySimulator_Ui", "0.00")
        )
        self.evaluate_quality_btn.setText(
            _translate("XRaySimulator_Ui", "Evaluate Quality")
        )
        self.menuFile.setTitle(_translate("XRaySimulator_Ui", "File"))
        self.menuHelp.setTitle(_translate("XRaySimulator_Ui", "Help"))
        self.toolBar.setWindowTitle(_translate("XRaySimulator_Ui", "toolBar"))
        self.actionRectangle_ROI.setText(
            _translate("XRaySimulator_Ui", "Rectangle_ROI")
        )
        self.actionRectangle_ROI.setToolTip(
            _translate(
                "XRaySimulator_Ui",
                "Select a rectangular region of interest. Shortcut is ctrl+R",
            )
        )
        self.actionRectangle_ROI.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+R"))
        self.actionImport_Image.setText(_translate("XRaySimulator_Ui", "Import Image"))
        self.actionImport_Image.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+I"))
        self.actionSave_Image.setText(_translate("XRaySimulator_Ui", "Save Image"))
        self.actionSave_Image.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+S"))
        self.actionSynthesize_Image.setText(
            _translate("XRaySimulator_Ui", "Synthesize Image")
        )
        self.actionExit.setText(_translate("XRaySimulator_Ui", "Exit"))
        self.actionExit.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+Q"))
        self.actionDocumentation.setText(
            _translate("XRaySimulator_Ui", "Documentation")
        )
        self.actionDocumentation.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+D"))
        self.actionReset.setText(_translate("XRaySimulator_Ui", "Reset"))
        self.actionReset.setToolTip(
            _translate(
                "XRaySimulator_Ui",
                "Delete the ROI and reset the image. Shortcut is ctrl+Shift+R",
            )
        )
        self.actionReset.setShortcut(_translate("XRaySimulator_Ui", "Ctrl+Shift+R"))
