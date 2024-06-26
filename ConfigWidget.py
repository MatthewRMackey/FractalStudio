from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout


class ConfigWidget(QWidget):
    def __init__(self, parent=None, width=600, height=800):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.label = QLabel("Configuration")
        
         # Create widgets
        self.power_label = QLabel("Power")
        self.line_edit = QLineEdit("2")
        self.button = QPushButton("Generate Fractal")
        self.display_depth = QLineEdit("Zoom = .5")

        # Create layouts
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.power_label)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(self.button)
        
        v_layout = QVBoxLayout()
        v_layout.addLayout(title_layout)
        v_layout.addLayout(h_layout)
        
        self.setLayout(v_layout)
        
        self.setFixedSize(self.width, self.height)

        # Connect button click to a method
        self.button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        print("correct")