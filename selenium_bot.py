import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class OponeoBot():
    DRIVER_PATH = None
    driver = None

    def __init__(self, vehicle_type=None, season=None, makers=None, tyre_width=None, tyre_height=None,
                 tyre_diameter=None, weight_index=None, speed_index=None, run_flat=False, extra_load=False):
        super().__init__()
        self.vehicle_type = vehicle_type
        self.season = season
        self.makers = makers
        self.tyre_width = tyre_width
        self.tyre_height = tyre_height
        self.tyre_diameter = tyre_diameter
        self.weight_index = weight_index
        self.speed_index = speed_index
        self.run_flat = run_flat
        self.extra_load = extra_load
        # initialize driver
        self.init_driver()
        # apply initial parameters
        if self.tyre_width is not None:
            self.select_tyre_width()

    def init_driver(self):
        current_path = os.path.split(__file__)[0]
        self.DRIVER_PATH = os.path.join(current_path, 'driver', 'chromedriver_v88.exe')
        self.driver = webdriver.Chrome(self.DRIVER_PATH)
        self.driver.get('https://www.oponeo.pl/wybierz-opony/s=1/zimowe/t=1/osobowe/r=1/205-55-r16')

    def select_tyre_width(self):
        tyre_width = Select(self.driver.find_element_by_id('_ctTS_ddlDimWidth'))
        tyre_width.select_by_visible_text(self.tyre_width)


a = OponeoBot(tyre_width='355')
