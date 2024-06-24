import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSlider
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

from fractals.Mandelbrot import Mandelbrot
from ZoomableGraphicsWindow import ZoomableGraphicsView
from FractalGrid import FractalGrid

class MainWindow(QMainWindow):
    def __init__(self, win_height=800, win_width=1200):
        super().__init__()
        self.win_height = win_height
        self.win_width = win_width
        self.options_panel_width_pct = 20
        self.display_panel_width_pct = 80
        self.display_panel_width = int(self.win_width * self.display_panel_width_pct*.01)
        self.display_panel_height = self.win_height

        self.setWindowTitle("FractalStudio")
        self.setGeometry(100, 100, self.win_width, self.win_height)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.build_options_panel()
        self.build_display_panel()

        # Add panels to main layout with correct proportions
        self.main_layout.addWidget(self.options_panel, self.options_panel_width_pct)
        self.main_layout.addWidget(self.display_panel, self.display_panel_width_pct)

        self.setCentralWidget(self.main_widget)


    def build_options_panel(self):
        # Left panel (20% width)
        self.options_panel = QWidget()
        self.options_layout = QVBoxLayout()
        self.options_panel.setLayout(self.options_layout)

         # Create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)

        # Set the handle color to grey
        # Set the handle color to grey using stylesheet
        self.slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background: grey;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 2px;
            }
        """)

        # Add some buttons and input boxes to left panel
        self.options_layout.addWidget(QPushButton("Button 1"))
        self.options_layout.addWidget(QPushButton("Button 2"))
        self.options_layout.addWidget(QLineEdit())
        self.options_layout.addWidget(self.slider)
        self.options_layout.addStretch()


    def build_display_panel(self):
        self.display_panel = FractalGrid(self.display_panel_width, self.display_panel_height)


############################## TEMPORARY #############################################
    def load_opencv_image(self):
        # Read the image using OpenCV
        pixel_data = self.colorPixels(self.mb.escapes)
    
        # Convert numpy array to QImage
        height, width, channel = pixel_data.shape
        q_img = QImage(width, height, QImage.Format_RGB888)
        # TODO THIS DOESNT WORK
        for x in range(len(pixel_data)):
            for y in range(len(pixel_data[x])):
                q_img.setPixelColor(y, x, QColor(*pixel_data[x][y]))

        # Convert QImage to QPixmap for display
        pixmap = QPixmap.fromImage(q_img)
            
        # Scale the pixmap to fit the label while maintaining aspect ratio
        self.display_panel.setPixmap(pixmap.scaled(
            self.display_panel.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))


#Move build image to each fractal class and return the image

def build_mandel_image(data): 
    # Convert the list to a NumPy array with appropriate data type (uint8 for image pixels)
    image = np.asarray(data, dtype=np.uint8)

    return image
#####################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())