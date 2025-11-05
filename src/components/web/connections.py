from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        self._map_widgets(component)
        self.logic = logic
        
        self.start_page_btn.clicked.connect(
            lambda: self.logic.load_url("https://open.spotify.com/embed/playlist/37i9dQZEVXcRbPtT6vrrSL")
            )
        
        self.disable_element_btn.clicked.connect(
            lambda: self.logic.disable_element("/html/body/div/div/div/div[4]")
            )
        
        self.inject_css_btn.clicked.connect(
            lambda:self.logic.inject_css("/html/body")
            )
        
        self.highlight_elm_btn.clicked.connect(
            lambda:self.logic.highlight_element("/html/body/div/div/div/div[1]/div[1]/div")
            )
        
        self.design_mode_btn.clicked.connect(
            self.logic.activate_design_mode
            )
        
        self.devtools_btn.clicked.connect(
            self.logic.activate_devtools
            )
        
        self.change_url_btn.clicked.connect(
            self.logic.change_url
            )
        