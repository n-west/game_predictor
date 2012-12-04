# Scrapy settings for espnbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'espnbot'
BOT_VERSION = '1.1'

ITEM_PIPELINES = ['espnbot.pipelines.sqlite_pipeline']
SPIDER_MODULES = ['espnbot.spiders']
NEWSPIDER_MODULE = 'espnbot.spiders'
DEFAULT_ITEM_CLASS = 'espnbot.items.GameItem'
USER_AGENT = 'bracketology/%s' % (BOT_VERSION)
LOG_LEVEL = 'INFO'
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 0.5
DEPTH_LIMIT = 7

