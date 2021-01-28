import json
import os
import scrapy
from bs4 import BeautifulSoup
from oponeo_task.items import OponeoTaskItem


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
        """ TODO Link generator based on initial parameters"""
        link = ['https://www.oponeo.pl/wybierz-opony/s=1/letnie/t=1/osobowe/r=1/255-40-r18']
        return link

    @staticmethod
    def get_raw_text(text):
        raw_text = BeautifulSoup(text, 'lxml').text
        return raw_text

    def parse(self, response, **kwargs):
        sub_info = response.css('.productName > h3 > a')
        yield from response.follow_all(sub_info, self.parse_search_result)

    def parse_search_result(self, response):
        tyre_model = self.get_raw_text(str(response.css('.model').get()))
        speed_index = self.get_raw_text(str(response.css('div.data:nth-child(8)').get()))
        load_index = self.get_raw_text(str(response.css('div.data:nth-child(10)').get()))
        result = OponeoTaskItem()
        result['tyre_model'] = tyre_model
        result['speed_index'] = speed_index
        result['load_index'] = load_index
        return result
