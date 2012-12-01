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

class GameItem(Item):
    url = Field()
    home_name = Field()
    visit_name = Field()
    date = Field()
    home_FGMA_A = Field()
    home_3PM_A = Field()
    home_FTM_A = Field()
    home_OREB = Field()
    home_AST = Field()
    home_STL = Field()
    home_BLK = Field()
    home_TO = Field()
    home_PF = Field()
    home_PTS = Field()
    visit_FGMA_A = Field()
    visit_3PM_A = Field()
    visit_FTM_A = Field()
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

#    def parse_team(self, response):
#        # Furnish Request objects for each link to a game recap
#        self.log('Made it to parse_team for %s' % response.url)
#        return Request(url='', callback='parse_game_recap')
#
#    def parse_game_recap(self, response):
#        self.log('Made it to parse_game_recap for %s' % response.url)
#        # Furnish Request object for the boxscore, which contains the stats
    
    def parse_game_boxscore(self, response):
        # Load the game stats in to an Item
        x = HtmlXPathSelector(response)
        game = GameItem()
        game['url'] = response.url        
        game['home_name'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/thead[1]/tr[1]/th[1]/text()").extract()
        game['home_FGMA_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[3]/text()").extract()
        game['home_3PM_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[4]/text()").extract()
        game['home_FTM_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[5]/text()").extract()
        game['home_OREB'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[6]/text()").extract()
        game['home_AST'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[7]/text()").extract()
        game['home_STL'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[8]/text()").extract()
        game['home_BLK'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[9]/text()").extract()
        game['home_TO'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[10]/text()").extract()
        game['home_PF'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[11]/text()").extract()
        game['home_PTS'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[3]/tr[1]/td[12]/text()").extract()

        game['visit_name'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/thead[4]/tr[@class='team-color-strip']/th/text()").extract()
        game['visit_FGMA_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[3]/text()").extract()
        game['visit_3PM_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[4]/text()").extract()
        game['visit_FTM_A'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[5]/text()").extract()
        game['visit_OREB'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[6]/text()").extract()
        game['visit_AST'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[7]/text()").extract()
        game['visit_STL'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[8]/text()").extract()
        game['visit_BLK'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[9]/text()").extract()
        game['visit_TO'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[10]/text()").extract()
        game['visit_PF'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[11]/text()").extract()
        game['visit_PTS'] = x.select("//div[@id='my-players-table']/div[@class='mod-content']/table/tbody[6]/tr[1]/td[12]/text()").extract()

        self.log('boxscore captured for %s vs %s' % (game['home_name'], game['visit_name']))
        # print "I got into a boxscore page for " + game['home_name'] + " vs " + game['visit_name'] + "\n"
        return game

