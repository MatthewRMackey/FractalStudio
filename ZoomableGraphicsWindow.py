from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF, QPoint
import sys

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_zoom = 1
        self.min_zoom = .5
        self.is_scrolling = False
        self.mouse_pos = QPoint(0,0)
        self.center = QPoint(0,0)
        self.w_min = 0
        self.w_max = parent.width
        self.h_min = 0
        self.h_max = parent.height
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Enable mouse tracking
        self.setMouseTracking(True)
        
        # Set view behavior
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
            self.current_zoom *= zoom_factor
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
            self.current_zoom /= zoom_factor

    def mouseMoveEvent(self, event):
        try:
            self.mouse_pos = self.mapToScene(event.pos())
            super().mouseMoveEvent(event)
            self.parent().mouseMoveEvent(event)
        
        except Exception as e:
            print(f"Error getting mouse position: {e}")
    
    def resetZoom(self):
        self.scale(1/self.current_zoom,1/self.current_zoom)
        self.current_zoom = 1