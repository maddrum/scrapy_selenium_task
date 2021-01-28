BOT_NAME = 'oponeo_task'

SPIDER_MODULES = ['oponeo_task.spiders']
NEWSPIDER_MODULE = 'oponeo_task.spiders'
LOG_LEVEL = 'ERROR'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'oponeo_task.pipelines.OponeoTaskPipeline': 300,
}
