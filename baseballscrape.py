import csv
import requests
from bs4 import BeautifulSoup as bs
import os
import pandas as pd

def playersToExamine():

    playerid = []

    f = open('Fangraphs Leaderboard.csv')
    csv_f = csv.reader(f)

    i = 1
    for row in csv_f:
        player = []
        player.append(row[0])
        player.append(row[-1])
        playerid.append(player)
        if i > 300:
        #top 300 players only
            break
        i += 1

    playerid.pop(0)

    return playerid

def scrapeHTML(playerid):
    if not os.path.exists("HTML_Files"):
        os.makedirs("HTML_Files")

    for i in range(len(playerid)):
        url = "https://www.fangraphs.com/statss.aspx?playerid=" + playerid[i][1]
        r = requests.get(url)

        with open("HTML_Files/" + playerid[i][1]+".html", "w") as html_file:
            html_file.write(r.text)

def scrapeWAR():
    rel_path = "HTML_Files/"
    columns = ['id','season', 'war']
    csv_out = 'test.csv'

    with open(csv_out, 'w') as csv_file:
    # uses dictionary writer method of csv library and
    # writes headers to file
        new_csv = csv.DictWriter(csv_file,fieldnames=columns)
        new_csv.writeheader()

        for i in os.listdir('HTML_Files'):
            if i[-5:] == ".html":
                with open(rel_path + i,'r') as curr_file:
                    soup = bs(curr_file,'lxml')
                    tables = soup.find_all('table', {"id":"SeasonStats1_dgSeason11_ctl00"})
                for table in tables:
                    d = pd.read_html(table.prettify(), flavor="bs4")
                # if the table isn't empty and has a WAR value, add to csv
                # TODO: includes tables that should not be included
                if len(d):
                    if 'WAR' in d[0].columns:
                        curr_row = d[0].to_dict()
                        prev_season = 0
                        filter = ["Depth Charts","Steamer","ZiPS","THE BAT","ATC"]
                        for key in curr_row['Season'].keys():
                        # add values to current csv row
                            if curr_row["Team"][key] not in filter and curr_row["Team"][key][0:4] != "Fans":
                                if str(curr_row['WAR'][key]) == "nan":
                                    continue
                                if prev_season != curr_row['Season'][key]:
                                        row = {}
                                        row['id'] = i[:-5]
                                        if curr_row['Season'][key] != 'Postseason' and curr_row['Season'][key] != 'Total':
                                            row['season'] = curr_row['Season'][key]
                                        else:
                                            continue

                                        row['war'] = curr_row['WAR'][key]
                                        # write row
                                        new_csv.writerow(row)
                                prev_season = curr_row['Season'][key]

def main():
    playerid = playersToExamine()
    scrapeHTML(playerid)
    scrapeWAR()


main()
