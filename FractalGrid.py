from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QRectF, QPoint
from fractals.Mandelbrot import Mandelbrot
from ZoomableGraphicsWindow import ZoomableGraphicsView
import sys
import random

class FractalGrid(QWidget):
    def __init__(self, width, height, pixel_size=1):
        super().__init__()
        self.setMouseTracking(True)
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.fractal = Mandelbrot(h_sgmts=self.height, w_sgmts=self.width, m_depth=250)
        self.load_color_map()
        self.initUI()
        self.mouse_pos = QPoint()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.graphics_view = ZoomableGraphicsView(self)
        layout.addWidget(self.graphics_view)

        self.setGeometry(100, 100, self.width, self.height)

        self.color_fractal()

    def color_fractal(self):
        image = QImage(self.width, self.height, QImage.Format_RGB32)
        for x in range(len(self.fractal.escapes)):
            for y in range(len(self.fractal.escapes[x])):
                color = QColor(*self.col_map[self.fractal.escapes[x][y]%len(self.col_map)])
                image.setPixelColor(y, x, color)

        pixmap = QPixmap.fromImage(image)
        if self.pixel_size > 1:
            pixmap = pixmap.scaled(self.width * self.pixel_size, self.height * self.pixel_size)

        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.graphics_view.scene.addItem(pixmap_item)
        self.graphics_view.setSceneRect(pixmap_item.boundingRect())

    def load_color_map(self, map_file = "./color_maps/color_grad.txt"):
        # Load Color Map (probably create a color map class)
        with open(map_file, "r+") as fr:
            file_lines = fr.readlines() 
            colors = [c.split(",") for c in file_lines]  
            self.col_map = {i:(int(c[0]), int(c[1]), int(c[2])) for i,c in enumerate(colors)}

    def wheelEvent(self, event):
        if self.graphics_view.current_zoom > 4:
            center_offset = (self.mouse_pos.x()/self.width, self.mouse_pos.y()/self.height)
            i_len = self.fractal.i_range[1]-self.fractal.i_range[0]
            r_len = self.fractal.r_range[1]-self.fractal.r_range[0]
            new_i_len = i_len/self.graphics_view.current_zoom
            new_r_len = r_len/self.graphics_view.current_zoom
            new_center = (self.fractal.r_range[0] + center_offset[0]*r_len,
                          self.fractal.i_range[0] + center_offset[1]*i_len)
            self.fractal.r_range = (new_center[0]-new_r_len/2, new_center[0]+new_r_len/2)
            self.fractal.i_range = (new_center[1]-new_i_len/2, new_center[1]+new_i_len/2)
            self.fractal.m_depth *= 2
            self.fractal.generateManEscapes()
            self.color_fractal()
            self.graphics_view.resetZoom()

    def mouseMoveEvent(self, event):
        try:
            self.mouse_pos = event.pos()
            super().mouseMoveEvent(event)
        
        except Exception as e:
            print(f"Error getting mouse position: {e}")