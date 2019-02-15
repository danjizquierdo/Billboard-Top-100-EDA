# Mod1-Project
### Team Members 
Abdul Khimani, Daniel Izquierdo

## Project Goals
The motivation is to find the artists who have appeared in Billboard's Top 100 lists for the last nine years and to look for insights into the features of their current top songs.

### Scraping
The first step in this process is to scrape the list of artists for each year from Billboard's website and to pass those into Spotify to retrieve their unique ids and the features of their top songs. In order to do this run the scraper Jupyter Notebook with your own Spotify API access tokens for each endpoint. For information on how to access these tokens check out the billboard_scraper python file. Running the jupyter notebook will collect the data (saved as json files in your working directory) into a pandas DataFrame which is then pickled into your working directory.

### Exploratory Data Analysis
Our initial thoughts, exploration and visualization are catalogued in the EDA Jupyter Notebook. The subsets we found to not be especially distinct and so next steps will involve looking into creating a separate sample and examining differences in data between Top Artists and a random sampling of other Artists.

### Summary
A summary of this process with examples of codes and insights can be found in the Mod1-Project-Presentation powerpoint. A folder of the json files from the web scrapingfor the Top Charts from 2010-2018 have been attached in the tracks folder for easy reference.
