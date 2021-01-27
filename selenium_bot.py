import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


class OponeoBot():
    DRIVER_PATH = None
    driver = None
    parameters_ids = {}

    def __init__(self, season=None, makers=None, tyre_width=None, tyre_height=None,
                 tyre_diameter=None, weight_index=None, speed_index=None, run_flat=False, extra_load=False, **kwargs):
        super().__init__()
        self.season = season
        self.makers = makers
        self.tyre_width = tyre_width
        self.tyre_height = tyre_height
        self.tyre_diameter = tyre_diameter
        self.weight_index = weight_index
        self.speed_index = speed_index
        self.run_flat = run_flat
        self.extra_load = extra_load
        self.kwargs = kwargs
        # initialize driver
        self.init_driver()
        # generate parameters dictionary
        self.generate_initial_parameters()
        # apply initial parameters
        self.apply_initial_parameters()
        self.test_element()

    def init_driver(self):
        current_path = os.path.split(__file__)[0]
        self.DRIVER_PATH = os.path.join(current_path, 'driver', 'chromedriver_v88.exe')
        self.driver = webdriver.Chrome(self.DRIVER_PATH)
        self.driver.get('https://www.oponeo.pl/wybierz-opony/s=1/zimowe/t=1/osobowe/r=1/205-55-r16')

    def generate_initial_parameters(self):
        """Define initial key:value parameters. New parameters could be handled with kwargs"""
        # apply initial parameters
        if self.tyre_width is not None:
            self.parameters_ids['_ctTS_ddlDimWidth'] = self.tyre_width
        if self.tyre_height is not None:
            self.parameters_ids['_ctTS_ddlDimRatio'] = self.tyre_height
        if self.tyre_diameter is not None:
            self.parameters_ids['_ctTS_ddlDimDiameter'] = self.tyre_diameter

    def apply_initial_parameters(self):
        for element_id in self.parameters_ids:
            self._dropdown_select_by_id(element_id=element_id, element_value=self.parameters_ids[element_id])
            time.sleep(2)

    def _dropdown_select_by_id(self, element_id, element_value):
        parameter = Select(self.driver.find_element_by_id(element_id))
        parameter.select_by_visible_text(element_value)

    def test_element(self):
        parameter = self.driver.find_elements_by_class_name('dropdown')
        print(dir(parameter[1]))
        parameter[2].click()


a = OponeoBot(tyre_width='205', tyre_height='65', tyre_diameter='16')
