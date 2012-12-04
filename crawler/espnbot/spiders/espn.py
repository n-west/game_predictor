# (C) Nathan West
#
# This spider scrapes ESPN.com for results from NCAA D1
# basketball games played during the current year.
# It collects the both team's statistics from their matchup
# and stores them to a SQLite database.
#

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from espnbot.items import GameItem

class EspnSpider(CrawlSpider):
    # Spider crawls ESPN's top 25 NCAA basketball rankings looking for game recaps
    # When it stumbles in to a game recap, grab the game stats for each team and
    # dump in to a SQLite database
    name = "espn"
    allowed_domains = ["espn.go.com"]
    start_urls = ["http://espn.go.com/mens-college-basketball/rankings"]
    rules = [
        Rule(SgmlLinkExtractor(allow=['/mens-college-basketball/team/_/id/'])),
        Rule(SgmlLinkExtractor(allow=['/ncb/recap\?gameId=[0-9]*'])),
        Rule(SgmlLinkExtractor(allow=['/ncb/boxscore\?gameId=[0-9]*']), callback='parse_game_boxscore')
    ]

    def parse_game_boxscore(self, response):
        # Load the game stats in to an Item
        x = HtmlXPathSelector(response)
        game = GameItem()

        game['url'] = response.url
        game['Id'] = game['url'].split('gameId=')[1]
        game['date'] = x.select("//div[@class='game-time-location']/p[1]/text()").extract()[0]

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

