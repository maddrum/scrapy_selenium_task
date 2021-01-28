# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class OponeoTaskPipeline:

    def process_item(self, item, spider):
        found_items = [item['tyre_model'], item['speed_index'], item['load_index']]
        print(f'For query: {spider.input_data()} found: {found_items}')
        return item
