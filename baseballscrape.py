import csv
import requests
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import numpy

def playersToExamine():

    playerid = []

    f = open('Fangraphs Leaderboard.csv')
    csv_f = csv.reader(f)


    for row in csv_f:
        player = []
        player.append(row[0])
        player.append(row[-1])
        playerid.append(player)

    playerid.pop(0)

    return playerid

def scrapeHTML(playerid):
    for i in range(len(playerid)):
        single_player = []
        url = "https://www.fangraphs.com/statss.aspx?playerid=" + playerid[i][1]
        r = requests.get(url)

        with open(playerid[i][1]+".html", "w") as html_file:
            html_file.write(r.text)

def scrapeWAR():
    rel_path = "HTML_Files/"
    columns = ['id','season', 'war']
    rows = []
    csv_out = 'test.csv'
    with open(csv_out, 'w') as csv_file:
    # uses dictionary writer method of csv library and
    # writes headers to file
        new_csv = csv.DictWriter(csv_file,fieldnames=columns)
        new_csv.writeheader()
        for i in os.listdir('HTML_Files'):
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
                    #prev_season = 0
                    for key in curr_row['Season'].keys():
                    # add values to current csv row
                        #if prev_season != curr_row['Season'][key]:
                            row = {}
                            row['id'] = i[:-5]
                            if curr_row['Season'][key] != 'Postseason' and curr_row['Season'][key] != 'Total':
                                row['season'] = curr_row['Season'][key]
                            else:
                                continue

                            row['war'] = curr_row['WAR'][key]
                            # write row
                            new_csv.writerow(row)

                        #prev_season = curr_row['Season'][key]
"""
    # with open(playersWAR) as csv_file
    # for i in range(1):
    path = "HTML_Files"
    all_html = os.listdir(path)
    col_headers = ["Season",	"Team",	"G",	"PA",	"HR",	"R",	"RBI",	"SB",	"BB%",	"K%",	"ISO",	"BABIP",	"AVG",	"OBP",	"SLG",	"wOBA",	"wRC+",	"BsR",	"Off",	"Def",	"WAR"]
    rows = []
    for page in all_html:

        if page[-5:] == ".html":
            with open(path+"/"+page, "r") as curr_file:
                soup = BeautifulSoup(curr_file, "lxml")
            table = soup.find(id="SeasonStats1_dgSeason11_ctl00")
            tbody = table.find_all("tbody")
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
            row = {}

            i = 0
            for td in tds:
                row[col_headers[i]] = td.text
                i++
        rows.append(row)
    print(rows)





        for table in tables:
             tbodys = table.find_all("tbody")
             for tbody in tbodys:
                 trs = tbody.find_all("tr")
                 for tr in trs:
                     tds = tr.find_all('td')
                     for j in range(1):

                         try: #we are using "try" because the table is not well formatted. This allows the program to continue after encountering an error.
                             war = tds[-1].get_text() # This structure isolate the item by its column in the table and converts it into a string.
                             if war != "\xa0":
                                 single_player.append(war)

                         except:
                             continue
         if len(single_player) !=0:
             single_player.pop(-1)
         master_list.append(single_player)
     return master_list
"""

def main():
    playerid = playersToExamine()
    scrapeWAR()

    """
    playerid = playersToExamine()
    master_list = playersWar(playerid)
    master_dict = warDictionary(playerid, master_list)
    with open('players_war.csv', mode='w') as csv_file:
        fieldnames = ['name', 'war']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for player in master_dict:
            writer.writerow({'name': player["name"], 'war': player["war"]})
    with open('players_info.csv', mode='w') as csv_file:
        fieldnames = ['name', 'war']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for player in master_dict:
            writer.writerow({'id': player["id"], 'name': player["name"], hof: player["hof"]})

    """


main()
