# Baseball Player Valuation

WAR (Wins Above Replacement) is a metric that tries to "measure all of a baseball player's on-field contributions using a single numerical value." A player's individual WAR score is meant to represent how valuable a player is to a team. The goal of this project is to provide a tool that can represent a player's cumulative WAR value over a certain value (k). This will make it easier to compare the WAR of two or more players.


### Creating the Project

At the beginning of the project, we had to familiarize ourselves with what WAR was and so we used the following websites: 
* https://www.beyondtheboxscore.com/2014/1/10/5291950/basic-sabermetrics-wins-above-replacement-war-fwar-bwar-warp
* https://slate.com/culture/2015/04/war-defined-how-to-understand-baseballs-most-important-and-convoluted-stat.html
* https://www.fangraphs.com/graphsw.aspx?playerid2=&playerid3=&playerid4=&playerid5=

### These were the steps that we decided to take to create this project
1. Scrape fangraphs.com for the WAR values of each player into a csv file.
2. Use the MLB Data API to gain additional information about each player.
3. Use the Data-Driven Documents (D3.js) library to make the visualization of the war value using the csv file


### Tools

  ##### Scraping Tools
  * Beautiful Soup 4 (Python Library) - https://pypi.org/project/beautifulsoup4/
  * Pandas (Python Data Analysis Library) - https://pandas.pydata.org/

  ##### Baseball Data
  * fangraphs.com - https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=1871&ind=0&team=0&rost=0&age=0&filter=&players=0
  * MLB Data API - https://appac.github.io/mlb-data-api-docs/

  ##### Data Visualization Tools
  * D3.js - https://d3js.org/

### Acknowledgments

This project was funded by the Swarthmore Projects for Educational Exploration and Development (SPEED) program at Swarthmore College.

We'd like to thank Nabil Kashyap,  Doug Willen, the Swarthmore Librarians, and the rest of Swarthmore ITS for continuously supporting the SPEED interns throughout the creation of this project. We'd also like to thank Steve Wang for proposing the project.
