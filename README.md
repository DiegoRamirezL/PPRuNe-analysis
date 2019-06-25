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
Then, all the scripts beginning by initial have been run to conduct the topic classification, the organization recognition and the sentiment analysis. These files consists of :

- initial_cleaning.py : For each post in EL_PPRUNE_POST. The text of the posts will have the punctuation, stop words(ie. "to","and", "of") removed and the words lemmatized ("led" will be "lead", etc).

- initial_topic_classification.py : This scripts works with the cleaned posts done in the cleaning script. It extracts the dictionnary of topics which consists of 10 lists of 25 words that have the most co-occurrences togheter. The dictionnary can be manually modified if the user considers that the topics can be improved. The posts for each thread are grouped togheter and considering the topic that has the maximum number of matched words, a thread has a topic assigned.

- initial_organization_recognition.py : This script extract for in each post of the forum the organizations mentioned. Then ,with a process of wikification (ie. find the wikipedia link of the extracted organization), the organization extracted are matched to the EL_S_ORGANIZATION.

- initial_sentiment_analysis : This script computes the sentiment and polarity of each individual post using the textblob package in python.

## Daily
### Webscraping
Each day, the script named daily_scraping.py needs to be run to keep our database up to date with the forums. In order to do so, the date of the last post in EL_PPRUNE_POST is compared to the date of the last post in a specific forum of the website. The posts between those 2 dates are then webscrapped. 

### Analysis
After the daily scraping, the script named daily_analysis.py needs to be run to analyse the new threads and posts in database. 
This script will import the three scripts :
- daily_topic_classification.py : This script works with the dictionnary defined in "initial_topic_classification.py"
- daily_organization_recognition.py
- daily_sentiment_analysis.py

When finished, it sets the value MODIFIED_BY and MODIFIED_DATE in the thread and post tables to something not null. This ensures that we know which threads and posts have been analyzed.
