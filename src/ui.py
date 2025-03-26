from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class XRaySimulator_Ui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(618, 878)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_widget_vlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_widget_vlayout.setContentsMargins(9, 0, -1, -1)
        self.central_widget_vlayout.setObjectName("central_widget_vlayout")
        self.warning_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.warning_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.warning_label.setObjectName("warning_label")
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
        self.image_simulator_groupbox_gridlayout = QtWidgets.QGridLayout(
            self.image_simulator_groupBox
        )
        self.image_simulator_groupbox_gridlayout.setObjectName(
            "image_simulator_groupbox_gridlayout"
        )
        self.kVp_label = QtWidgets.QLabel(parent=self.image_simulator_groupBox)
        self.kVp_label.setObjectName("kVp_label")
        self.image_simulator_groupbox_gridlayout.addWidget(self.kVp_label, 0, 0, 1, 1)
        self.mAs_label = QtWidgets.QLabel(parent=self.image_simulator_groupBox)
        self.mAs_label.setObjectName("mAs_label")
        self.image_simulator_groupbox_gridlayout.addWidget(self.mAs_label, 1, 0, 1, 1)
        self.image_simulator_section_vlayout.addWidget(self.image_simulator_groupBox)
        self.simulate_parameters_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.simulate_parameters_btn.setObjectName("evaluate_quality_btn_2")
        self.image_simulator_section_vlayout.addWidget(self.simulate_parameters_btn)
        self.controls_hlayout.addLayout(self.image_simulator_section_vlayout)
        self.metrics_section_vlayout = QtWidgets.QVBoxLayout()
        self.metrics_section_vlayout.setObjectName("metrics_section_vlayout")
        self.quality_metrics_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.quality_metrics_groupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.quality_metrics_groupBox.setObjectName("quality_metrics_groupBox")
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
        self.metrics_section_vlayout.addWidget(self.evaluate_quality_btn)
        self.controls_hlayout.addLayout(self.metrics_section_vlayout)
        self.central_widget_vlayout.addLayout(self.controls_hlayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionRectangle_ROI = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("assets/icons/rectangle_roi.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionRectangle_ROI.setIcon(icon)
        self.actionRectangle_ROI.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionRectangle_ROI.setObjectName("actionRectangle_ROI")
        self.actionImport_Image = QtGui.QAction(parent=MainWindow)
        self.actionImport_Image.setObjectName("actionImport_Image")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDocumentation = QtGui.QAction(parent=MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.menuFile.addAction(self.actionImport_Image)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionRectangle_ROI)

        # Create the matplotlib canvas inside the frame
        self.image_display_frame_vlayout = QtWidgets.QVBoxLayout(
            self.image_display_frame
        )
        self.image_display_frame_vlayout.setObjectName("image_display_frame_vlayout")
        self.image_display_figure = plt.figure()
        self.image_display_figure_canvas = FigureCanvas(self.image_display_figure)
        self.image_display_frame_vlayout.addWidget(self.image_display_figure_canvas)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.warning_label.setText(
            _translate(
                "MainWindow",
                "Warning: Simulation parameters changed, re-click the evaluation quality button.",
            )
        )
        self.image_simulator_groupBox.setTitle(
            _translate("MainWindow", "Image Simulator")
        )
        self.kVp_label.setText(_translate("MainWindow", "kVp"))
        self.mAs_label.setText(_translate("MainWindow", "mAs"))
        self.simulate_parameters_btn.setText(
            _translate("MainWindow", "Simulate parameters")
        )
        self.quality_metrics_groupBox.setTitle(
            _translate("MainWindow", "Quality Metrics")
        )
        self.cnr_label.setText(_translate("MainWindow", "CNR"))
        self.cnr_value_label.setText(_translate("MainWindow", "0"))
        self.snr_label.setText(_translate("MainWindow", "SNR"))
        self.snr_value_label.setText(_translate("MainWindow", "0"))
        self.spatial_resolution_label.setText(
            _translate("MainWindow", "Spatial Resolution")
        )
        self.spatial_resolution_value_label.setText(_translate("MainWindow", "0"))
        self.evaluate_quality_btn.setText(_translate("MainWindow", "Evaluate Quality"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionRectangle_ROI.setText(_translate("MainWindow", "Rectangle_ROI"))
        self.actionRectangle_ROI.setToolTip(
            _translate(
                "MainWindow",
                "Select a rectangular region of interest. Shortcut is ctrl+R",
            )
        )
        self.actionRectangle_ROI.setCheckable(True)
        self.actionRectangle_ROI.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionImport_Image.setText(_translate("MainWindow", "Import Image"))
        self.actionImport_Image.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionDocumentation.setShortcut(_translate("MainWindow", "Ctrl+D"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = XRaySimulator_Ui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
