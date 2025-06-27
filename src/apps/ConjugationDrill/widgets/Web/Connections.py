from src.apps.ConjugationDrill.widgets.Web.Functions import Logic
from src.apps.ConjugationDrill.widgets.Web.Layout import Layout as Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic
        
        # self.ui.start_page_btn.clicked.connect(
        #     lambda: self.logic.load_url("https://chatgpt.com/share/685de2e2-e1d8-8003-ac0d-f385815fb7a7")
        #     )
        
        # self.ui.disable_element_btn.clicked.connect(
        #     lambda: self.logic.disable_element("/html/body/div/div/div/div[4]")
        #     )
        
        # self.ui.inject_css_btn.clicked.connect(
        #     lambda:self.logic.inject_css("/html/body/div[1]/div/div[1]/div[2]/main/div/div/div[2]/div[1]/div/div/div[2]/form/div[1]/div/div[2]/div/div[2]/div/button")
        #     )
        
        # self.ui.highlight_elm_btn.clicked.connect(
        #     lambda:self.logic.highlight_element("//div[@id='prompt-textarea']")
        #     )
        
        # self.ui.design_mode_btn.clicked.connect(
        #     self.logic.activate_design_mode
        #     )
        
        # self.ui.devtools_btn.clicked.connect(
        #     self.logic.activate_devtools
        #     )
        
        # self.ui.change_url_btn.clicked.connect(
        #     self.logic.change_url
        #     )


        # self.ui.xpath_btn.clicked.connect(
        #     lambda: self.logic.type_text("//div[@id='prompt-textarea']", "HELLO FROM PYQT6")
        # )

        # self.ui.xpath_btn1.clicked.connect(
        #     lambda: self.logic.click_element("//button[@id='composer-submit-button']")
        # )