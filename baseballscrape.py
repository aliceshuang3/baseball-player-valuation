import csv
import requests
from bs4 import BeautifulSoup

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

def playersWar(playerid):
    master_list = []

    for i in range(5):
        single_player = []
        url = "https://www.fangraphs.com/statss.aspx?playerid=" + playerid[i][1]
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        tables = soup.find_all('table', {"id": "SeasonStats1_dgSeason11_ctl00"})

        for table in tables:
            tbodys = table.find_all("tbody")
            for tbody in tbodys:
                trs = tbody.find_all("tr")
                for tr in trs:
                    tds = tr.find_all('td')
                    for i in range(1):

                        try: #we are using "try" because the table is not well formatted. This allows the program to continue after encountering an error.
                            war = tds[-1].get_text() # This structure isolate the item by its column in the table and converts it into a string.
                            if war != "\xa0":
                                single_player.append(war)

                        except:
                            continue
        single_player.pop(-1)
        master_list.append(single_player)
    return master_list

def warDictionary(playerid, master_list):
    dictionary_lst = []
    for i in range(5):
        player = {"name": playerid[i][0],
        "war": master_list[i]}
        dictionary_lst.append(player)
        print(player)
    return dictionary_lst

def main():
    playerid = playersToExamine()
    master_list = playersWar(playerid)
    master_dict = warDictionary(playerid, master_list)

main()
