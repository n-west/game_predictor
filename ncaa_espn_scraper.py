#!/bin/python
#
# (C) Nathan West
#
# This spider scrapes ESPN.com for results from NCAA D1
# basketball games played during a given year.
# It collects the both team's statistics from their matchup
# and stores them to a sqlite database.
#

from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import sqlite3

class GameItem(Item):
    url = Field()
    date = Field()
    home_name = Field()
    visit_name = Field()
    date = Field()
    home_FGM = Field()
    home_FGA = Field()
    home_3PM = Field()
    home_3PA = Field()
    home_FTM = Field()
    home_FTA = Field()
    home_OREB = Field()
    home_AST = Field()
    home_STL = Field()
    home_BLK = Field()
    home_TO = Field()
    home_PF = Field()
    home_PTS = Field()
    visit_FGM = Field()
    visit_FGA = Field()
    visit_3PM = Field()
    visit_3PA = Field()
    visit_FTM = Field()
    visit_FTA = Field()
    visit_OREB = Field()
    visit_AST = Field()
    visit_STL = Field()
    visit_BLK = Field()
    visit_TO = Field()
    visit_PF = Field()
    visit_PTS = Field()
    
	
class EspnSpider(CrawlSpider):
    # Spider crawls ESPN's top 25 NCAA basketball rankings looking for game recaps
    # When it stumbles in to a game recap, grab the game stats for each team and
    # dump in to a SQLite database
    name = "espn"
    allowed_domains = ["espn.go.com"]
    start_urls = ["http://espn.go.com/mens-college-basketball/rankings"]
#    start_urls = ["http://espn.go.com/ncb/boxscore?gameId=323300197"]
    rules = [
        Rule(SgmlLinkExtractor(allow=['/mens-college-basketball/team/_/id/'])),
        Rule(SgmlLinkExtractor(allow=['/ncb/recap\?gameId=[0-9]*'])),
        Rule(SgmlLinkExtractor(allow=['/ncb/boxscore\?gameId=[0-9]*']), callback='parse_game_boxscore')
    ]
    # ITEM_PIPELINES = [sqlite_pipeline]
    
    def parse_game_boxscore(self, response):
        # Load the game stats in to an Item
        x = HtmlXPathSelector(response)
        game = GameItem()

        game['url'] = response.url        
        game['date'] = x.select("//div[@class='game-time-location']/p[1]/text()").extract()

        game['home_name'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/thead[1]/tr[1]/th[1]/text()").extract()[0]
        home_FGMA_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[3]/text()").extract()[0]
        home_FGMA_A_lst = home_FGMA_A_str.split('-')
        game['home_FGM'] = home_FGMA_A_lst[0]
        game['home_FGA'] = home_FGMA_A_lst[1]
        home_3PM_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[4]/text()").extract()[0]
        home_3PM_A_lst = home_3PM_A_str.split('-')
        game['home_3PM'] = home_3PM_A_lst[0]
        game['home_3PA'] = home_3PM_A_lst[1]
        home_FTMA_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[5]/text()").extract()[0]
        home_FTMA_A_lst = home_FTMA_A_str.split('-')
        game['home_FTM'] = home_FTMA_A_lst[0]
        game['home_FTA'] = home_FTMA_A_lst[1]
        game['home_OREB'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[6]/text()").extract()[0]
        game['home_AST'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[7]/text()").extract()[0]
        game['home_STL'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[8]/text()").extract()[0]
        game['home_BLK'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[9]/text()").extract()[0]
        game['home_TO'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[10]/text()").extract()[0]
        game['home_PF'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[11]/text()").extract()[0]
        game['home_PTS'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[12]/text()").extract()[0]

        game['visit_name'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/thead[4]/tr[@class='team-color-strip']/th/text()").extract()[0]
        visit_FGMA_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[3]/text()").extract()[0]
        visit_FGMA_A_lst = visit_FGMA_A_str.split('-')
        game['visit_FGM'] = home_FGMA_A_lst[0]
        game['visit_FGA'] = visit_FGMA_A_lst[1]
        visit_3PM_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[4]/text()").extract()[0]
        visit_3PM_A_lst = visit_3PM_A_str.split('-')
        game['visit_3PM'] = visit_3PM_A_lst[0]
        game['visit_3PA'] = visit_3PM_A_lst[1]
        visit_FTMA_A_str = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[5]/text()").extract()[0]
        visit_FTMA_A_lst = visit_FTMA_A_str.split('-')
        game['visit_FTM'] = visit_FTMA_A_lst[0]
        game['visit_FTA'] = visit_FTMA_A_lst[1]
        game['visit_OREB'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[6]/text()").extract()[0]
        game['visit_AST'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[7]/text()").extract()[0]
        game['visit_STL'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[8]/text()").extract()[0]
        game['visit_BLK'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[9]/text()").extract()[0]
        game['visit_TO'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[10]/text()").extract()[0]
        game['visit_PF'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[11]/text()").extract()[0]
        game['visit_PTS'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[12]/text()").extract()[0]

        self.log('boxscore captured for %s vs %s' % (game['home_name'], game['visit_name']))
        return game

class sqlite_pipeline(object):
    def __init__():
        pass

    def process_item(self, item, spider):
        store_item_command = "INSERT OR ABORT INTO bb_games_stats " \
        "( url, date, home_name, home_FGM, home_FGA, home_3PM, home_3PA, home_FTM, home_FTA, " \
        "home_OREB, home_AST, home_STL, home_BLK, home_TO, home_PF, home_PTS, " \
        "visit_name, visit_FGM, visit_FGA, visit_3PM, visit_3PA, visit_FTM, visit_FTA, " \
        "visit_OREB, visit_AST, visit_STL, visit_BLK, visit_TO, visit_PF, visit_PTS) " \
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" % (
        item['url'], item['date'], 
        item['home_name'], item['home_FGM'], item['home_FGA'], item['home_3PM'], item['home_3PA'], 
        item['home_FTM'], item['home_FTA'], item['home_OREB'], item['home_AST'], item['home_STL'], 
        item['home_BLK'], item['home_TO'], item['home_PF'], item['home_PTS'], 
        item['visit_name'], item['visit_FGM'], item['visit_FGA'], item['visit_3PM'], item['visit_3PA'], 
        item['visit_FTM'], item['visit_FTA'], item['visit_OREB'], item['visit_AST'], item['visit_STL'], 
        item['visit_BLK'], item['visit_TO'], item['visit_PF'], item['visit_PTS'])
    
        self.db_cursor.execute(store_item_command)
        self.db_connection.commit()
        
    def open_spider(self,spider):
        # similar examples seem to put this in __init__, but seems like it goes here
        self.db_connection = sqlite3.connect('ncaa_bb.db')
        self.db_cursor = db_connection.cursor()
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS bb_games_stats 
            (home_name TEXT, home_FGM INTEGER, home_FGA INTEGER, home_3PM INTEGER, home_3PA INTEGER, home_FTM INTEGER, home_FTA INTEGER,
             home_OREB INTEGER, home_AST INTEGER, home_STL INTEGER, home_BLK INTEGER, home_TO INTEGER, home_PF INTEGER, home_PTS INTEGER,
            visit_name TEXT, visit_FGM INTEGER, visit_FGA INTEGER, visit_3PM INTEGER, visit_3PA INTEGER, visit_FTM INTEGER, visit_FTA INTEGER, 
            visit_OREB INTEGER, visit_AST INTEGER, visit_STL INTEGER, visit_BLK INTEGER, visit_TO INTEGER, visit_PF INTEGER, visit_PTS INTEGER,
            url TEXT, date TEXT)
        ''')
    def close_spider(self, spider):
        self.db_connection.commit()
        self.db_connection.close()



