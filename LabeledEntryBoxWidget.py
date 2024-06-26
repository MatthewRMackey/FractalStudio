from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

class LabeledEntryBoxWidget(QWidget):
    def __init__(self, label_text, default_value, parent=None):
        super().__init__(parent)
        
        # Create widgets
        self.label = QLabel(label_text)
        self.line_edit = QLineEdit(default_value)
        
        # Create layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.line_edit)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(v_layout)