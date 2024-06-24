from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF
import sys

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_zoom = 1
        self.min_zoom = .5
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

    def fitInView(self, rect, keep_aspect_ratio=False):
        if not rect.isNull():
            self.setSceneRect(rect)
            unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.viewport().rect()
            scene_rect = self.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.scale(factor*2, factor*2)
            self.centerOn(rect.center())

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
            self.current_zoom *= zoom_factor
        elif self.current_zoom > self.min_zoom:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
            self.current_zoom /= zoom_factor
