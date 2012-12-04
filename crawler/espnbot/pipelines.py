import sqlite3
from scrapy import log
from scrapy.exceptions import DropItem

class sqlite_pipeline(object):
    """Drop the GameItem into a SQLite database"""

    def process_item(self, item, spider):
        tabledata = tuple(item.keys() + item.values())
        insert_cmd = 'INSERT INTO \'bb_games_stats\' ({0}) VALUES ({1})'
        insert_cmd = insert_cmd.format((','.join(item.keys())), (','.join('?'*len(item.keys()) )) )
        insert_strng = insert_cmd.replace('?', '%s') % tuple(item.values())
        try: 
            self.db_cursor.execute(insert_cmd, tuple(item.values() ))
        except sqlite3.IntegrityError:
            raise DropItem()
        self.db_connection.commit()
        return item

    def open_spider(self, spider):
        # similar examples seem to put this in __init__, but seems like it goes here
        self.db_connection = sqlite3.connect('ncaa_bb.db')
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS bb_games_stats 
            (Id INTEGER UNIQUE, home_name TEXT, home_FGM INTEGER, home_FGA INTEGER, home_3PM INTEGER, home_3PA INTEGER, home_FTM INTEGER, home_FTA INTEGER,
             home_OREB INTEGER, home_AST INTEGER, home_STL INTEGER, home_BLK INTEGER, home_TO INTEGER, home_PF INTEGER, home_PTS INTEGER,
            visit_name TEXT, visit_FGM INTEGER, visit_FGA INTEGER, visit_3PM INTEGER, visit_3PA INTEGER, visit_FTM INTEGER, visit_FTA INTEGER, 
            visit_OREB INTEGER, visit_AST INTEGER, visit_STL INTEGER, visit_BLK INTEGER, visit_TO INTEGER, visit_PF INTEGER, visit_PTS INTEGER,
            url TEXT, date TEXT)
        ''')

