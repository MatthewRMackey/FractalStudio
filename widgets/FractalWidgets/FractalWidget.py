from abc import ABCMeta, abstractmethod
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtCore import Qt, QTimer

from util.FractalColorMap import FractalColorMap

# Create a combined metaclass
class QtABCMeta(type(QWidget), ABCMeta):
    pass

class FractalWidget(QWidget, metaclass=QtABCMeta):
    def __init__(self, parent=None, width=600, height=800):
        super().__init__(parent)
        self.color_map = FractalColorMap("Default")
        self.center = (0, 0) #(x,y)
        self.zoom = .5
        self.width = width
        self.height = height
        self.depth = 100
        self.power = 2
        self.image = None
        #TODO change back to .25
        self.current_resolution = (int(1*self.width), int(1*self.height))
        self.setFixedSize(self.width, self.height)
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.progressiveRender)

    @abstractmethod
    def generate(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image is None:
            # Draw a blank background and a "Rendering" message
            painter.fillRect(self.rect(), Qt.black)
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter, "Rendering...")
            self.startProgressiveRender()
        else:
            painter.drawImage(self.rect(), self.image)

    def startProgressiveRender(self):
        if not self.render_timer.isActive():
            #TODO change back to .25
            self.current_resolution = (int(1*self.width), int(1*self.height))
            self.render_timer.start(0)  # Start immediately

    def progressiveRender(self):
        escape_depths = self.generate()

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
        colored_fractal = self.color_map.apply_colormap(escape_depths)
        for y in range(self.current_resolution[1]):
            for x in range(self.current_resolution[0]):
                color = QColor(*colored_fractal[y][x])
                image.setPixel(x, y, color.rgb())
        self.image = image.scaled(self.width, self.height)

    def wheelEvent(self, event):
        zoom_factor = 1.5
        if event.angleDelta().y() > 0:
            self.zoom *= zoom_factor
            #TODO Change from *1
            self.depth = int(self.depth*1)
        else:
            self.zoom /= zoom_factor
            #TODO Change from *1
            self.depth = int(self.depth*1)

        self.image = None
        self.update()
        self.parent().wheelEvent(event)

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
            self.parent().mousePressEvent(event)
