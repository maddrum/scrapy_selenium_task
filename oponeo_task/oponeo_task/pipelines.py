class OponeoTaskPipeline:

    def process_item(self, item, spider):
        found_items = [item['tyre_model'], item['speed_index'], item['load_index']]
        print(f'Found: {found_items}')
        return item
