import sys

import numpy as np
import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSlider
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

from widgets.ConfigWidget import ConfigWidget
from widgets.MandelbrotWidget import MandelbrotWidget
from util.FractalColorMap import FractalColorMap


class MainWindow(QMainWindow):
    def __init__(self,  win_width=600, win_height=400):
        super().__init__()
        self.win_width = win_width if win_width > 600 else 600
        self.win_height = win_height if win_height > 400 else 400
        self.panel_margin = 20
        self.config_panel_width = 200-self.panel_margin
        self.config_panel_height = self.win_height - self.panel_margin
        self.display_panel_width = self.win_width-self.config_panel_width - self.panel_margin
        self.display_panel_height = self.win_height - self.panel_margin

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
        self.config_panel.gen_button.clicked.connect(self.on_gen_button_click)
        self.config_panel.reset_button.clicked.connect(self.on_reset_button_click)
        self.config_panel.save_button.clicked.connect(self.on_save_button_click)


    def build_display_panel(self):
        self.display_panel = MandelbrotWidget(self, self.display_panel_width, self.display_panel_height)

    def on_gen_button_click(self):
        display_panel = self.display_panel
        config_panel = self.config_panel
        #TODO fix change resolution... doesn't work
        new_resolution = config_panel.res_dropdown.get_current_selection().split("x")
        display_panel.depth = int(config_panel.depth_entry.line_edit.text())
        display_panel.power = float(config_panel.power_entry.line_edit.text())
        display_panel.zoom = float(config_panel.zoom_entry.line_edit.text())
        display_panel.center = (float(config_panel.center_x_entry.line_edit.text()), float(config_panel.center_y_entry.line_edit.text()))
        # self.display_panel.fractals #TODO Need to abstract fractal so this can be changed from mandel to julia to Sierpinski Triangles
        display_panel.color_map.name = config_panel.col_map_dropdown.get_current_selection()
        display_panel.color_map.color_map = display_panel.color_map.build_color_map(display_panel.depth)
        display_panel.startProgressiveRender()

    def on_reset_button_click(self):
        deleted_widget = self.main_layout.itemAt(1).widget()
        self.main_layout.removeWidget(deleted_widget)
        deleted_widget.deleteLater()
        self.build_display_panel()
        self.main_layout.addWidget(self.display_panel)
    
    def on_save_button_click(self):

        # Calculate function params
        display_panel = self.display_panel
        scale_width = 2 / (display_panel.zoom * display_panel.width)
        scale_height = 2 / (display_panel.zoom * display_panel.height)
        x_min = display_panel.center[0] - display_panel.width / 2 * scale_width
        x_max = display_panel.center[0] + display_panel.width / 2 * scale_width
        y_min = display_panel.center[1] - display_panel.height / 2 * scale_height
        y_max = display_panel.center[1] + display_panel.height / 2 * scale_height

        # RGB 2D map
        escape_depths = display_panel.fractals.generateMandelbrot(
            (x_min, x_max), (y_min, y_max), 
            display_panel.current_resolution[0], display_panel.current_resolution[1], 
            display_panel.depth, display_panel.power
        )

        # OpenCV uses BGR format, so convert RGB to BGR
        escape_depths = np.array(escape_depths)
        bgr_array = cv2.cvtColor(display_panel.color_map.apply_colormap(escape_depths, display_panel.depth), cv2.COLOR_RGB2BGR)
        
        # Count existing files and save
        os.makedirs("./imgs/mandelbrot/", exist_ok=True)
        existing_files = len([f for f in os.listdir("./imgs/mandelbrot/") if f.startswith('output_image_') and f.endswith('.png')])
        filename = f'./imgs/mandelbrot/output_image_{existing_files}.png'
        cv2.imwrite(filename, bgr_array)

    def wheelEvent(self, event):
        self.config_panel.zoom_entry.line_edit.setText(str(self.display_panel.zoom))

    def mousePressEvent(self, event):
        self.config_panel.center_x_entry.line_edit.setText(str(self.display_panel.center[0]))
        self.config_panel.center_y_entry.line_edit.setText(str(self.display_panel.center[1]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(win_width=1200, win_height=1000)
    window.show()
    sys.exit(app.exec_())