import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtCore import Qt, QRectF, QTimer
from Fractals import Fractals

class MandelbrotWidget(QWidget):
    def __init__(self, parent=None, width=600, height=800):
        super().__init__(parent)
        self.fractals = Fractals()
        self.color_map = self.load_color_map()
        self.center = (0, 0)
        self.zoom = .5
        self.width = width
        self.height = height
        self.depth = 200
        self.power = 2.0
        self.image = None
        self.current_resolution = (int(.25*self.width), int(.25*self.height))  # Start with a low resolution
        self.setFixedSize(self.width, self.height)
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.progressiveRender)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image is None:
            # Draw a blank background or a "Loading" message
            painter.fillRect(self.rect(), Qt.black)
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter, "Rendering...")
            self.startProgressiveRender()
        else:
            painter.drawImage(self.rect(), self.image)

    def startProgressiveRender(self):
        if not self.render_timer.isActive():
            self.current_resolution = (int(.25*self.width), int(.25*self.height))
            self.render_timer.start(0)  # Start immediately

    def progressiveRender(self):
        scale_width = 2 / (self.zoom * self.width)
        scale_height = 2 / (self.zoom * self.height)
        x_min = self.center[0] - self.width / 2 * scale_width
        x_max = self.center[0] + self.width / 2 * scale_width
        y_min = self.center[1] - self.height / 2 * scale_height
        y_max = self.center[1] + self.height / 2 * scale_height

        escape_depths = self.fractals.generateMandelbrot(
            (x_min, x_max), (y_min, y_max), 
            self.current_resolution[0], self.current_resolution[1], 
            self.depth, self.power
        )

        self.updateImage(escape_depths)
        self.update()

        if self.current_resolution[0] < self.width and self.current_resolution[1] < self.height:
            cur_res_width = min(self.current_resolution[0] * 2, self.width)
            cur_res_height = min(self.current_resolution[1] * 2, self.height)
            self.current_resolution = (cur_res_width, cur_res_height)
        else:
            self.render_timer.stop()

    def updateImage(self, escape_depths):
        image = QImage(self.current_resolution[0], self.current_resolution[1], QImage.Format_RGB32)
        for y in range(self.current_resolution[1]):
            for x in range(self.current_resolution[0]):
                color = QColor(*self.color_map[escape_depths[y][x]%len(self.color_map)])
                image.setPixel(x, y, color.rgb())
        self.image = image.scaled(self.width, self.height)

    def wheelEvent(self, event):
        zoom_factor = 1.5
        if event.angleDelta().y() > 0:
            self.zoom *= zoom_factor
            self.depth = int(self.depth*1.02)
        else:
            self.zoom /= zoom_factor
            self.depth = int(self.depth*1.02)

        print(self.zoom)
        print(self.depth)
        self.image = None
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            scale_x = 2.0 / (self.zoom * self.width)
            scale_y = 2.0 / (self.zoom * self.height)
            dx = (x - self.width / 2) * scale_x
            dy = (y - self.height / 2) * scale_y
            self.center = (self.center[0] + dx, self.center[1] + dy)
            self.image = None
            self.update()

    def load_color_map(self, map_file = "./color_maps/color_grad.txt"):
        # Load Color Map (probably create a color map class)
        color_map = {}
        with open(map_file, "r+") as fr:
            file_lines = fr.readlines() 
            colors = [c.split(",") for c in file_lines]  
            color_map = {i:(int(c[0]), int(c[1]), int(c[2])) for i,c in enumerate(colors)}
        return color_map

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mandelbrot Explorer")
        self.mandelbrot_widget = MandelbrotWidget(self)
        self.setCentralWidget(self.mandelbrot_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())