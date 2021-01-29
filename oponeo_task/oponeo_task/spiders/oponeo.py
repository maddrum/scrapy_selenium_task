import json
import os
import time

import scrapy
from bs4 import BeautifulSoup
from oponeo_task.items import OponeoTaskItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class OponeoSpider(scrapy.Spider):
    name = 'oponeo'
    allowed_domains = ['oponeo.pl']
    start_urls = None

    def __init__(self, category=None, *args, **kwargs):
        super(OponeoSpider).__init__()
        self.input_data = self.get_input_data()
        self.start_urls = self.generate_link()

    @staticmethod
    def get_input_data():
        """Reads data from input_json file"""
        json_file = '../../input_data.json'
        if not os.path.isfile(json_file):
            raise IOError('Input data file "input_data.json" is not found.')
        with open(json_file) as input_file:
            input_data = json.load(input_file)
            input_file.close()
        print(f'Input data: {input_data}')
        return input_data

    def generate_link(self):
        """ This method generates scrape link based on inputs, except for extra load. """
        link = 'https://www.oponeo.pl/wybierz-opony/'
        # seasons
        seasons = {
            'winter': 'zimowe',
            'summer': 'letnie',
            'all-season': 'caloroczne',
        }
        if len(self.input_data['season']) != 0:
            try:
                link += f's=1/{seasons[self.input_data["season"]]}/'
            except KeyError:
                raise KeyError('Not valid options for season found.')
        # makers
        if len(self.input_data['makers']) != 0:
            input_data_makers = ','.join(self.input_data['makers']).lower()
            link += f'p=1/{input_data_makers}/'
        # tyre sizes
        if self.input_data['width'] and self.input_data['height'] and self.input_data['diameter']:
            link += f'r=1/{self.input_data["width"]}-{self.input_data["height"]}-r{self.input_data["diameter"]}/'
        # speed index
        if self.input_data['speed-index']:
            link += f'ip=1/{self.input_data["speed-index"].lower()}/'
        # load index
        if self.input_data['weight-index']:
            link += f'in=1/{self.input_data["weight-index"]}/'
        # run-flat
        if self.input_data['run-flat']:
            link += f'o=1/run-flat/'
        print(f'Base scrape link (without XL parameter): {link}')
        return [link]

    @staticmethod
    def get_raw_text(text):
        raw_text = BeautifulSoup(text, 'lxml').text
        return raw_text

    def parse(self, response, **kwargs):
        # initialize selenium webdriver
        current_path = os.path.split(__file__)[0]
        driver_path = os.path.join(current_path, 'driver', 'chromedriver_v88.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(executable_path=driver_path, desired_capabilities=desired_capabilities)
        driver.get(response.url)
        # splash screen remove
        time.sleep(60)
        no_button = driver.find_element_by_css_selector('span.button.no')
        webdriver.ActionChains(driver).move_to_element(no_button).click(no_button).perform()
        # apply XL parameter with altering response
        if self.input_data['extra-load']:
            reinforced_click = driver.find_element_by_class_name('reinforced')
            reinforced_click.click()
            time.sleep(5)
            response = response.replace(body=driver.page_source)
        # run with respect of pagination
        next_page = 2
        has_pagination = True
        while True:
            # check for pagination
            pagination = driver.find_element_by_class_name('blPages')
            try:
                pagination.find_element_by_tag_name('li')
            except NoSuchElementException:
                has_pagination = False
            sub_info = response.css('.productName > h3 > a::attr("href")')
            yield from response.follow_all(sub_info, self.parse_search_result)
            # break if only 1 page of results/no pagination/
            if not has_pagination:
                break
            # click on next page if present
            next_link_id = f'_ctPgrp_pi{next_page}i'
            try:
                next_link = driver.find_element_by_id(next_link_id)
            except NoSuchElementException:
                break
            webdriver.ActionChains(driver).move_to_element(next_link).click(next_link).perform()
            time.sleep(5)
            response = response.replace(body=driver.page_source)
            time.sleep(5)
            next_page += 1
        driver.close()

    def parse_search_result(self, response):
        scraped_tyre_model = str(response.css('.model').get())
        scraped_speed_index = str(response.css('div.data:nth-child(8)').get())
        scraped_load_index = str(response.css('div.data:nth-child(10)').get())
        tyre_model = self.get_raw_text(scraped_tyre_model)
        speed_index = self.get_raw_text(scraped_speed_index)
        load_index = self.get_raw_text(scraped_load_index)
        result = OponeoTaskItem()
        result['tyre_model'] = tyre_model
        result['speed_index'] = speed_index
        result['load_index'] = load_index
        return result
