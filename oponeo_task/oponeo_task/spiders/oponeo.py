import scrapy
from bs4 import BeautifulSoup
from oponeo_task.items import OponeoTaskItem


class OponeoSpider(scrapy.Spider):
    name = 'oponeo'
    allowed_domains = ['oponeo.pl']
    start_urls = None

    def __init__(self):
        super(OponeoSpider).__init__()
        self.start_urls = self.generate_link()

    def input_data(self):
        return ['todo', ]

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
