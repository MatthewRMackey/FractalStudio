import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSlider
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

from ConfigWidget import ConfigWidget
from MandelbrotWidget import MandelbrotWidget


class MainWindow(QMainWindow):
    def __init__(self, win_height=1000, win_width=1800):
        super().__init__()
        self.win_height = win_height
        self.win_width = win_width
        self.config_panel_width_pct = 19
        self.display_panel_width_pct = 79
        self.panel_height_pct = .98
        self.config_panel_width = int(self.win_width * self.config_panel_width_pct*.01)
        self.config_panel_height = self.win_height * self.panel_height_pct
        self.display_panel_width = int(self.win_width * self.display_panel_width_pct*.01)
        self.display_panel_height = self.win_height * self.panel_height_pct

        self.setWindowTitle("FractalStudio")
        self.setGeometry(100, 100, self.win_width, self.win_height)
        self.setFixedSize(self.win_width, self.win_height)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.build_config_panel()
        self.build_display_panel()

        # Add panels to main layout with correct proportions
        self.main_layout.addWidget(self.config_panel)
        self.main_layout.addWidget(self.display_panel)

        self.setCentralWidget(self.main_widget)


    def build_config_panel(self):
        self.config_panel = ConfigWidget(self, self.config_panel_width, self.config_panel_height)


    def build_display_panel(self):
        self.display_panel = MandelbrotWidget(self, self.display_panel_width, self.display_panel_height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())