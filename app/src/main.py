import sys

from PyQt6.QtWidgets import QApplication

from backend import XRaySimulator_Backend


def main():
    app = QApplication(sys.argv)
    main_window = XRaySimulator_Backend()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
