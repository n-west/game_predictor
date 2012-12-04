import sqlite3
from scrapy import log

class sqlite_pipeline(object):
    """Drop the GameItem into a SQLite database"""

    def process_item(self, item, spider):
#         store_item_command = "INSERT OR ABORT INTO bb_games_stats " \
#         "( url, date, home_name, home_FGM, home_FGA, home_3PM, home_3PA, home_FTM, home_FTA, " \
#         "home_OREB, home_AST, home_STL, home_BLK, home_TO, home_PF, home_PTS, " \
#         "visit_name, visit_FGM, visit_FGA, visit_3PM, visit_3PA, visit_FTM, visit_FTA, " \
#         "visit_OREB, visit_AST, visit_STL, visit_BLK, visit_TO, visit_PF, visit_PTS) " \
#         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" % (
#         item['url'], item['date'],
#         item['home_name'], item['home_FGM'], item['home_FGA'], item['home_3PM'], item['home_3PA'],
#         item['home_FTM'], item['home_FTA'], item['home_OREB'], item['home_AST'], item['home_STL'],
#         item['home_BLK'], item['home_TO'], item['home_PF'], item['home_PTS'],
#         item['visit_name'], item['visit_FGM'], item['visit_FGA'], item['visit_3PM'], item['visit_3PA'],
#         item['visit_FTM'], item['visit_FTA'], item['visit_OREB'], item['visit_AST'], item['visit_STL'],
#         item['visit_BLK'], item['visit_TO'], item['visit_PF'], item['visit_PTS'])
# 
#         self.db_cursor.execute(store_item_command)
#         self.db_connection.commit()
        tabledata = tuple(item.keys() + item.values())
        insert_cmd = 'INSERT INTO \'bb_games_stats\' ({0}) VALUES ({1})'
        insert_cmd = insert_cmd.format((','.join(item.keys())), (','.join('?'*len(item.keys()) )) )
        print insert_cmd.replace('?', '%s')
        insert_strng = insert_cmd.replace('?', '%s') % tuple(item.values())
        print insert_strng
        # self.db_cursor.execute(insert_cmd, tabledata)
        self.db_cursor.execute(insert_cmd, tuple(item.values() ))
        self.db_connection.commit()

    def open_spider(self, spider):
        # similar examples seem to put this in __init__, but seems like it goes here
        self.db_connection = sqlite3.connect('ncaa_bb.db')
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS bb_games_stats 
            (home_name TEXT, home_FGM INTEGER, home_FGA INTEGER, home_3PM INTEGER, home_3PA INTEGER, home_FTM INTEGER, home_FTA INTEGER,
             home_OREB INTEGER, home_AST INTEGER, home_STL INTEGER, home_BLK INTEGER, home_TO INTEGER, home_PF INTEGER, home_PTS INTEGER,
            visit_name TEXT, visit_FGM INTEGER, visit_FGA INTEGER, visit_3PM INTEGER, visit_3PA INTEGER, visit_FTM INTEGER, visit_FTA INTEGER, 
            visit_OREB INTEGER, visit_AST INTEGER, visit_STL INTEGER, visit_BLK INTEGER, visit_TO INTEGER, visit_PF INTEGER, visit_PTS INTEGER,
            url TEXT, date TEXT)
        ''')

