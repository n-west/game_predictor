game\_predictor
==============

Grab data from ESPN.com for game-by-game stats for NCAA D1 basketball, then make predictions on the winner


# Current Status
The crawler is working and storing results. 
Possibly add a max depth in the config and randomize download intervals. 

Time to get some predictions

# Crawler
    cd crawler
    scrapy crawl espn

The results will appear in ncaa\_bb.db

# Predictor
Currently only on paper
