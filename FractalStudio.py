import sys
import os

import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

from Widgets.OptionsWidget import OptionsWidget
from Widgets.FractalWidgets.MandelbrotWidget import MandelbrotWidget
from Widgets.FractalWidgets.JuliaWidget import JuliaWidget

FRACTAL_TYPES = {
    'Mandelbrot' : 'M',
    'Julia' : 'J',
    'Sirepiński Triangle' : 'ST' ,
}

class MainWindow(QMainWindow):
    def __init__(self,  win_width=600, win_height=400):
        super().__init__()
        self.win_width = win_width if win_width > 600 else 600
        self.win_height = win_height if win_height > 400 else 400
        self.panel_margin = 20
        self.options_panel_width = 200-self.panel_margin
        self.options_panel_height = self.win_height - self.panel_margin
        self.display_panel_width = self.win_width-self.options_panel_width - self.panel_margin
        self.display_panel_height = self.win_height - self.panel_margin

        self.setWindowTitle("FractalStudio")
        self.setGeometry(100, 100, self.win_width, self.win_height)
        self.setFixedSize(self.win_width, self.win_height)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.f_type = "Mandelbrot"
        self.build_options_panel()
        self.build_display_panel(self.f_type)

        # Add panels to main layout with correct proportions
        self.main_layout.addWidget(self.options_panel)
        self.main_layout.addWidget(self.display_panel)

        self.setCentralWidget(self.main_widget)


    def build_options_panel(self):
        self.options_panel = OptionsWidget(self, self.options_panel_width, self.options_panel_height)
        self.options_panel.gen_button.clicked.connect(self.on_gen_button_click)
        self.options_panel.reset_button.clicked.connect(self.on_reset_button_click)
        self.options_panel.save_button.clicked.connect(self.on_save_button_click)


    def build_display_panel(self, f_type="Mandelbrot"):
        if FRACTAL_TYPES[f_type] == "M":
            self.display_panel = MandelbrotWidget(self, self.display_panel_width, self.display_panel_height)
        elif FRACTAL_TYPES[f_type] == "J":
            self.display_panel = JuliaWidget(self, self.display_panel_width, self.display_panel_height, 
                                            c=complex(float(self.options_panel.center_x_entry.line_edit.text()), 
                                                      float(self.options_panel.center_y_entry.line_edit.text())))

    def on_gen_button_click(self):
        # Build correct type of fractal if changing types
        new_f_type = self.options_panel.fractal_dropdown.get_current_selection()
        display_panel = self.display_panel
        options_panel = self.options_panel
        
        if new_f_type != self.f_type:
            self.f_type = new_f_type
            self.build_display_panel(self.f_type)
            display_panel = self.display_panel
            self.options_panel.center_x_entry.line_edit.setText("0.0")
            self.options_panel.center_y_entry.line_edit.setText("0.0")
            self.options_panel.zoom_entry.line_edit.setText(".5")
            # Remove old fractal display and add new display and reset options
            # TODO when adding the c entry box, it will be updated here after adding options back
            deleted_display = self.main_layout.itemAt(1).widget()
            self.main_layout.removeWidget(deleted_display)
            deleted_display.deleteLater()
            self.main_layout.addWidget(self.display_panel)

        else:
            # Change display variables based on inputs 
            # TODO This should update c whenever that entry box is added
            display_panel.zoom = float(options_panel.zoom_entry.line_edit.text())
            display_panel.center = (float(options_panel.center_x_entry.line_edit.text()), float(options_panel.center_y_entry.line_edit.text()))
        
        display_panel.depth = int(options_panel.depth_entry.line_edit.text())
        display_panel.power = float(options_panel.power_entry.line_edit.text())
        display_panel.color_map.map_name = options_panel.col_map_dropdown.get_current_selection()
        display_panel.color_map.color_map = display_panel.color_map.build_color_map()
        #TODO This needs to be changed to update somehow
        display_panel.startProgressiveRender()

    def on_reset_button_click(self):
        deleted_options = self.main_layout.itemAt(0).widget()
        deleted_display = self.main_layout.itemAt(1).widget()
        self.main_layout.removeWidget(deleted_options)
        deleted_options.deleteLater()
        self.main_layout.removeWidget(deleted_display)
        deleted_display.deleteLater()
        self.build_options_panel()
        self.build_display_panel()
        self.main_layout.addWidget(self.options_panel)
        self.main_layout.addWidget(self.display_panel)
    
    def on_save_button_click(self):

        escape_depths = self.display_panel.generate()

        # OpenCV uses BGR format, so convert RGB to BGR
        escape_depths = np.array(escape_depths)
        colored_points = self.display_panel.color_map.apply_colormap(escape_depths).astype(np.uint8)
        bgr_array = cv2.cvtColor(colored_points, cv2.COLOR_RGB2BGR)
        
        # Count existing files and save
        directory = "./media/imgs/"+self.f_type+"/"
        os.makedirs(directory, exist_ok=True)
        existing_files = len([f for f in os.listdir(directory) if f.startswith('output_image_') and f.endswith('.png')])
        filename = directory+f'output_image_{existing_files}.png'
        cv2.imwrite(filename, bgr_array)


    def wheelEvent(self, event):
        self.options_panel.zoom_entry.line_edit.setText(str(self.display_panel.zoom))

    def mousePressEvent(self, event):
        self.options_panel.center_x_entry.line_edit.setText(str(self.display_panel.center[0]))
        self.options_panel.center_y_entry.line_edit.setText(str(self.display_panel.center[1]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(win_width=1200, win_height=1000)
    window.show()
    sys.exit(app.exec_())