from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from LabeledEntryBoxWidget import LabeledEntryBoxWidget
from DropdownWidget import DropdownWidget

class ConfigWidget(QWidget):
    def __init__(self, parent=None, width=600, height=800):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.label = QLabel("Configuration")
        
         # Create widgets
        self.power_entry = LabeledEntryBoxWidget("Power", "2", self)
        self.zoom_entry = LabeledEntryBoxWidget("Zoom", ".5", self)
        self.center_label = QLabel("Center Location")
        self.center_x_entry = LabeledEntryBoxWidget("x", "0", self)
        self.center_y_entry = LabeledEntryBoxWidget("y", "0", self)
        self.fractal_dropdown = DropdownWidget("Fractal Type", ["1","2","3"], self)
        self.col_map_dropdown = DropdownWidget("Color Map", ["Name1","Name2","Name3"], self)
        self.res_dropdown = DropdownWidget("Resolution", ["600x400","1000x800","1920x1080"], self)
        self.gen_button = QPushButton("Generate Fractal")
        self.save_button = QPushButton("Save Image")
        self.new_map_button = QPushButton("Generate New Color Map")
        self.reset_button = QPushButton("Reset All")
        
        center_h_layout = QHBoxLayout()
        center_h_layout.addWidget(self.center_x_entry)
        center_h_layout.addWidget(self.center_y_entry)

        center_v_layout = QVBoxLayout()
        center_v_layout.addWidget(self.center_label, alignment=QtCore.Qt.AlignCenter)
        center_v_layout.addLayout(center_h_layout)
        center_v_layout.setContentsMargins(0,0,0,0)

        v_layout = QVBoxLayout()
        # v_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.power_entry)
        v_layout.addWidget(self.zoom_entry)
        v_layout.addLayout(center_v_layout)
        v_layout.addWidget(self.fractal_dropdown)
        v_layout.addWidget(self.col_map_dropdown)
        v_layout.addWidget(self.res_dropdown)
        v_layout.addWidget(self.gen_button)
        v_layout.addWidget(self.save_button)
        v_layout.addWidget(self.new_map_button)
        v_layout.addWidget(self.reset_button)
        v_layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(v_layout)
        
        self.setFixedSize(self.width, self.height)

        # Connect button click to a method
        self.gen_button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        print("correct")
    
    def mousePressEvent(self, event):
        print("Mouse event")