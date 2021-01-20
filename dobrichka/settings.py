BOT_NAME = 'dobrichka'

SPIDER_MODULES = ['dobrichka.spiders']
NEWSPIDER_MODULE = 'dobrichka.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'dobrichka.pipelines.DobrichkaPipeline': 100,

}