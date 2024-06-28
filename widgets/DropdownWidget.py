from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox

class DropdownWidget(QWidget):
    def __init__(self, label_text, options, parent=None):
        super().__init__(parent)
        
        # Create layout
        layout = QHBoxLayout(self)
        
        # Create and add label
        self.label = QLabel(label_text)
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        
        # Create and add combo box
        self.combo_box = QComboBox()
        self.combo_box.addItems(options)
        layout.addWidget(self.combo_box)
        
        # Adjust margins
        layout.setContentsMargins(0,0,0,0)
        
        # Connect the combo box's currentIndexChanged signal to our custom slot
        self.combo_box.currentIndexChanged.connect(self.selection_changed)
        
    def selection_changed(self, index):
        print(f"Selection changed to: {self.combo_box.currentText()} (index: {index})")
    
    def get_current_selection(self):
        return self.combo_box.currentText()
    
    def set_selection(self, text):
        index = self.combo_box.findText(text)
        if index >= 0:
            self.combo_box.setCurrentIndex(index)