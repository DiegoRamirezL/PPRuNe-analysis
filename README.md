# PPRuNe-analysis
## Professional Pilots Rumours Network
The Professional Pilots Rumour Network ([PPRuNe](https://www.pprune.org/)) is an aviation website dedicated to airline pilots to share rumours and news.

## Database architecture
To conduct a thorough analysis of the PPRuNe, the forums have to be stored in database. To represent the website four tables have been created :
- EL_PPRUNE_FORUM
- EL_PPRUNE_THREAD
- EL_PPRUNE_POST
- EL_PPRUNE_ORGANIZATION

For more information, see the Vertabelo model of the database architecture.

## Initial
### Webscraping
The first step is to webscrape forums to extract threads and posts from the website. archive_scraping.py is used to get an entire forum from the website archive.

### Analysis
Then, all the scripts beginning by initial have been run to conduct the topic classification, the organization recognition and the sentiment analysis.

## Daily
### Webscraping
Each day, the script named daily_scraping.py needs to be run to keep our database up to date with the forums.

### Analysis
After the daily scraping, the script named daily_analysis.py needs to be run to analyse the new threads and posts in database. This script will import the three scripts :
- daily_topic_classification.py
- daily_organization_recognition.py
- daily_sentiment_analysis.py

When finished, it sets the value MODIFIED_BY and MODIFIED_DATE in the thread and post tables to something not null. This ensures that we know which threads and posts have been analyzed.
