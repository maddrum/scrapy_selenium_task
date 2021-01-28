import scrapy


class OponeoTaskItem(scrapy.Item):
    tyre_model = scrapy.Field()
    speed_index = scrapy.Field()
    load_index = scrapy.Field()
