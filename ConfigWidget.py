from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from LabeledEntryBoxWidget import LabeledEntryBoxWidget
from DropdownWidget import DropdownWidget

class ConfigWidget(QWidget):
    def __init__(self, parent=None, width=200, height=600):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.label = QLabel("Configuration")
        
         # Create widgets
        self.power_entry = LabeledEntryBoxWidget("Power", "2", self)
        self.zoom_entry = LabeledEntryBoxWidget("Zoom", ".5", self)
        self.depth_entry = LabeledEntryBoxWidget("Depth", "100", self)
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
        v_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.depth_entry)
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

        # Button function connects
        self.gen_button.clicked.connect(self.on_gen_button_click)
        self.gen_button.clicked.connect(self.on_save_button_click)
        self.gen_button.clicked.connect(self.on_colmap_button_click)
        self.gen_button.clicked.connect(self.on_reset_button_click)
    
    def on_gen_button_click(self):
        #TODO DONT KNOW WHAT TO DO HERE HELP ME
        # Disgusting I know
        self.parent().regenerate_fractal((-2,2), (-2,2), 600, 600, 10, 3)
    
    def on_save_button_click(self):
        print("save")

    def on_colmap_button_click(self):
        print("colmap")

    def on_reset_button_click(self):
        print("reset")

    def mousePressEvent(self, event):
        print("Mouse event")