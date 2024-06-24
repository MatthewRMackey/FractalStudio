from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt, QRectF
from fractals.Mandelbrot import Mandelbrot
from ZoomableGraphicsWindow import ZoomableGraphicsView
import sys
import random

class FractalGrid(QWidget):
    def __init__(self, width, height, pixel_size=1):
        super().__init__()
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.fractal = Mandelbrot(h_sgmts=self.height, w_sgmts=self.width)
        self.load_color_map()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.graphics_view = ZoomableGraphicsView(self)
        layout.addWidget(self.graphics_view)

        self.setGeometry(100, 100, self.width, self.height)

        self.color_fractal()

    def color_fractal(self):
        for x in range(len(self.fractal.escapes)):
            for y in range(len(self.fractal.escapes[x])):
                rect = QGraphicsRectItem(QRectF(y * self.pixel_size, x * self.pixel_size, self.pixel_size, self.pixel_size))
                color = QColor(*self.col_map[self.fractal.escapes[x][y]])
                rect.setBrush(color)
                rect.setPen(QPen(Qt.NoPen))  # No border for the pixels
                self.graphics_view.scene.addItem(rect)

        # Set the scene rect to encompass all pixels
        self.graphics_view.setSceneRect(0, 0, self.width * self.pixel_size, self.height * self.pixel_size)

    def load_color_map(self, map_file = "./color_maps/color_grad.txt"):
        # Load Color Map (probably create a color map class)
        with open("./color_maps/color_grad.txt", "r+") as fr:
            file_lines = fr.readlines() 
            colors = [c.split(",") for c in file_lines]  
            self.col_map = {i:(int(c[0]), int(c[1]), int(c[2])) for i,c in enumerate(colors)}