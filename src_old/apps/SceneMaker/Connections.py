from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        color_names = ["black", "red", "green", "blue", "orange"]
        for color in color_names:
            btn = getattr(self.ui, color, None)
            if isinstance(btn, QPushButton):
                btn.clicked.connect(lambda checked, c=color: self.logic.set_stroke_color(c))


        # for btn, color_name in zip(self.ui.color_buttons, self.ui.color_names):
        #     btn.clicked.connect(lambda checked, c=color_name: self.logic.set_stroke_color(c))
        

        self.ui.add_btn.clicked.connect(self.logic.add_scene)
        self.ui.update_btn.clicked.connect(self.logic.update_scene)
        self.ui.clear_btn.clicked.connect(self.logic.clear_drawing)
        self.ui.delete_btn.clicked.connect(self.logic.delete_scene)
        self.ui.open_player_btn.clicked.connect(self.logic.open_player)

        self.ui.scene_list.currentRowChanged.connect(self.logic.load_scene)

        self.ui.size_slider.valueChanged.connect(self.logic.set_stroke_width)