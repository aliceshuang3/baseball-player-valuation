import csv
import requests
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import json

# keys for the MLB API
mlbapi_keys = ['name_display_first_last','position','player_id']

# Names of the top 300 players
top_300_players =["Keith Hernandez","Cupid Childs","Ozzie Smith","Jeff Kent","Brian Downing","Rickey Henderson","Reggie Smith","Ernie Banks","Carlton Fisk","Luke Appling","Darryl Strawberry","Harry Hooper","George Gore","Jesse Burkett","Tommy Leach","Boog Powell","Joe Cronin","Mike Cameron","Max Carey","Robin Ventura","Tris Speaker","Curtis Granderson","Chipper Jones","Mel Ott","Joe Mauer","Willie Mays","George Burns","Dolph Camilli","Carlos Beltran","Scott Rolen","Miguel Cabrera","Ron Cey","Larry Doyle","John Olerud","Yogi Berra","Dale Murphy","Gabby Hartnett","Billy Williams","Joe Torre","Nap Lajoie","Fred Lynn","Torii Hunter","Ryan Braun","Luis Gonzalez","Brett Butler","Jason Giambi","Joe Gordon","Joe Morgan","Joe Kelley","Hardy Richardson","Jimmy Rollins","Enos Slaughter","Bobby Grich","Jackie Robinson","Willie Stargell","Jack Fournier","Frank Robinson","George Sisler","Richie Ashburn","Andruw Jones","Phil Rizzuto","Eddie Collins","Honus Wagner","Jeff Bagwell","Kiki Cuyler","Paul Waner","George Brett","Larry Walker","Adrian Beltre","Joe Judge","Heinie Manush","Bob Johnson","Edd Roush","Earl Averill","Mike Schmidt","Ted Simmons","Willie Randolph","Bobby Wallace","Stan Hack","Al Oliver","Rafael Palmeiro","Lou Whitaker","Sal Bando","Tim Raines","Wade Boggs","Carl Yastrzemski","J.D. Drew","Jim Fregosi","Bob Elliott","Andy Van Slyke","Julio Franco","Paul Molitor","Mickey Mantle","Eddie Murray","Bill Dickey","Mike Trout","Ken Griffey Jr.","Jim Thome","Tony Lazzeri","Lou Gehrig","Ian Kinsler","Lance Parrish","Dave Winfield","John McGraw","Johnny Bench","Dixie Walker","Willie Keeler","Pete Rose","Joe Jackson","Ben Zobrist","Al Simmons","Hank Aaron","Hanley Ramirez","Barry Bonds","Davey Lopes","Rusty Staub","Ken Boyer","Jake Beckley","Bobby Doerr","Evan Longoria","Rod Carew","Ryne Sandberg","Pete Browning","Ty Cobb","Jack Glasscock","Paul Hines","Al Kaline","Ron Santo","Eddie Mathews","Jose Cruz","Andrew McCutchen","Ken Singleton","Toby Harrah","Mark McGwire","Babe Herman","Cal Ripken","Orlando Cepeda","Ed Delahanty","Dave Parker","Johnny Damon","Nellie Fox","Tony Fernandez","Harry Stovey","Frank Thomas","Heinie Groh","Rabbit Maranville","Dave Bancroft","David Wright","Duke Snider","Jose Canseco","Deacon White","Hugh Duffy","Jack Clark","Carl Crawford","Johnny Evers","Willie Davis","Sam Crawford","Will Clark","Jim Edmonds","Tony Gwynn","Bill Dahlen","Todd Helton","Sherry Magee","Babe Ruth","Ellis Burks","Buddy Bell","Pee Wee Reese","Rogers Hornsby","Arky Vaughan","Bill Terry","Andre Dawson","George Van Haltren","Omar Vizquel","Ben Chapman","Hank Greenberg","Ed Konetchy","Billy Herman","Hack Wilson","Gene Tenace","Charlie Gehringer","Matt Holliday","Brooks Robinson","Cesar Cedeno","Harmon Killebrew","Bert Campaneris","Frank Baker","Ted Williams","Sam Rice","Chuck Klein","Roberto Clemente","Ivan Rodriguez","Mike Piazza","Nomar Garciaparra","Kirby Puckett","Jake Daubert","Earle Combs","Luis Aparicio","Dan Brouthers","Roy Thomas","Travis Jackson","Alex Rodriguez","Jose Reyes","Alan Trammell","Vladimir Guerrero","Goose Goslin","Jimmy Wynn","Hughie Jennings","Jimmy Collins","Buck Ewing","Charlie Keller","Stan Musial","Derek Jeter","Graig Nettles","Mark Teixeira","Art Fletcher","Johnny Mize","George Davis","Dustin Pedroia","Carlos Delgado","Frankie Frisch","Robinson Cano","Moises Alou","Lou Boudreau","Tony Perez","Devon White","Sam Thompson","Fred McGriff","Bobby Bonds","Gary Sheffield","Tony Phillips","Mike Griffin","Bid McPhee","Vern Stephens","Zack Wheat","Larry Gardner","Norm Cash","Kenny Lofton","Gil Hodges","David Ortiz","Robin Yount","Willie McCovey","Barry Larkin","Wally Berger","Dwight Evans","Mark Grace","Lance Berkman","Lou Brock","Dick Allen","Billy Hamilton","Mike Tiernan","Ichiro Suzuki","Ralph Kiner","Bobby Veach","Elmer Flick","Roberto Alomar","Chet Lemon","Roger Connor","Cap Anson","Joey Votto","Vada Pinson","Frank Chance","Reggie Jackson","Buddy Myer","Chase Utley","Minnie Minoso","Lave Cross","Craig Biggio","Edgar Martinez","Darrell Evans","Jim O'Rourke","Joe Sewell","Ernie Lombardi","Joe Tinker","Matt Williams","Jimmy Ryan","Jimmie Foxx","Augie Galan","Roger Peckinpaugh","Sammy Sosa","Manny Ramirez","Harry Heilmann","Brian Giles","Larry Doby","Jorge Posada","Albert Pujols","Bill Freehan","George Foster","Mickey Cochrane","Joe DiMaggio","Gary Carter","Fred Tenney","Jimmy Sheckard","Fielder Jones","King Kelly","Jim Rice","Fred Clarke","Bobby Abreu","Rocky Colavito","Bernie Williams"]

# top 300 players with their fangraphs id
top_300_players_dict = [{'Keith Hernandez': '1005706'},{'Cupid Childs': '1002186'},{'Ozzie Smith': '1012186'},{'Jeff Kent': '1119'},{'Brian Downing': '1003451'},{'Rickey Henderson': '194'},{'Reggie Smith': '1012201'},{'Ernie Banks': '1000512'},{'Carlton Fisk': '1004101'},{'Luke Appling': '1000284'},{'Darryl Strawberry': '1012606'},{'Harry Hooper': '1006002'},{'George Gore': '1004879'},{'Jesse Burkett': '1001682'},{'Tommy Leach': '1007428'},{'Boog Powell': '1010482'},{'Joe Cronin': '1002796'},{'Mike Cameron': '1070'},{'Max Carey': '1001944'},{'Robin Ventura': '854'},{'Tris Speaker': '1012309'},{'Curtis Granderson': '4747'},{'Chipper Jones': '97'},{'Mel Ott': '1009904'},{'Joe Mauer': '1857'},{'Willie Mays': '1008315'},{'George Burns': '1001708'},{'Dolph Camilli': '1001860'},{'Carlos Beltran': '589'},{'Scott Rolen': '970'},{'Miguel Cabrera': '1744'},{'Ron Cey': '1002108'},{'Larry Doyle': '1003467'},{'John Olerud': '1093'},{'Yogi Berra': '1000898'},{'Dale Murphy': '1009355'},{'Gabby Hartnett': '1005458'},{'Billy Williams': '1013975'},{'Joe Torre': '1013133'},{'Nap Lajoie': '1007259'},{'Fred Lynn': '1007872'},{'Torii Hunter': '731'},{'Ryan Braun': '3410'},{'Luis Gonzalez': '55'},{'Brett Butler': '1001772'},{'Jason Giambi': '818'},{'Joe Gordon': '1004874'},{'Joe Morgan': '1009179'},{'Joe Kelley': '1006776'},{'Hardy Richardson': '1010909'},{'Jimmy Rollins': '971'},{'Enos Slaughter': '1012060'},{'Bobby Grich': '1005033'},{'Jackie Robinson': '1011070'},{'Willie Stargell': '1012426'},{'Jack Fournier': '1004264'},{'Frank Robinson': '1011066'},{'George Sisler': '1012021'},{'Richie Ashburn': '1000335'},{'Andruw Jones': '96'},{'Phil Rizzuto': '1011011'},{'Eddie Collins': '1002451'},{'Honus Wagner': '1013485'},{'Jeff Bagwell': '547'},{'Kiki Cuyler': '1002914'},{'Paul Waner': '1013597'},{'George Brett': '1001400'},{'Larry Walker': '455'},{'Adrian Beltre': '639'},{'Joe Judge': '1006644'},{'Heinie Manush': '1008089'},{'Bob Johnson': '1006428'},{'Edd Roush': '1011247'},{'Earl Averill': '1000378'},{'Mike Schmidt': '1011586'},{'Ted Simmons': '1011986'},{'Willie Randolph': '1010694'},{'Bobby Wallace': '1013542'},{'Stan Hack': '1005183'},{'Al Oliver': '1009773'},{'Rafael Palmeiro': '1266'},{'Lou Whitaker': '1013846'},{'Sal Bando': '1000505'},{'Tim Raines': '1406'},{'Wade Boggs': '1001124'},{'Carl Yastrzemski': '1014326'},{'J.D. Drew': '1152'},{'Jim Fregosi': '1004330'},{'Bob Elliott': '1003733'},{'Andy Van Slyke': '1013363'},{'Julio Franco': '87'},{'Paul Molitor': '1009040'},{'Mickey Mantle': '1008082'},{'Eddie Murray': '1009386'},{'Bill Dickey': '1003271'},{'Mike Trout': '10155'},{'Ken Griffey Jr.': '327'},{'Jim Thome': '409'},{'Tony Lazzeri': '1007422'},{'Lou Gehrig': '1004598'},{'Ian Kinsler': '6195'},{'Lance Parrish': '1010021'},{'Dave Winfield': '1014127'},{'John McGraw': '1008542'},{'Johnny Bench': '1000826'},{'Dixie Walker': '1013512'},{'Willie Keeler': '1006747'},{'Pete Rose': '1011217'},{'Joe Jackson': '1006301'},{'Ben Zobrist': '7435'},{'Al Simmons': '1011978'},{'Hank Aaron': '1000001'},{'Hanley Ramirez': '8001'},{'Barry Bonds': '1109'},{'Davey Lopes': '1007750'},{'Rusty Staub': '1012440'},{'Ken Boyer': '1001283'},{'Jake Beckley': '1000754'},{'Bobby Doerr': '1003355'},{'Evan Longoria': '9368'},{'Rod Carew': '1001942'},{'Ryne Sandberg': '1011411'},{'Pete Browning': '1001554'},{'Ty Cobb': '1002378'},{'Jack Glasscock': '1004757'},{'Paul Hines': '1005845'},{'Al Kaline': '1006678'},{'Ron Santo': '1011447'},{'Eddie Mathews': '1008236'},{'Jose Cruz': '1002841'},{'Andrew McCutchen': '9847'},{'Ken Singleton': '1012011'},{'Toby Harrah': '1005384'},{'Mark McGwire': '1008559'},{'Babe Herman': '1005691'},{'Cal Ripken': '1010978'},{'Orlando Cepeda': '1002103'},{'Ed Delahanty': '1003155'},{'Dave Parker': '1010000'},{'Johnny Damon': '185'},{'Nellie Fox': '1004281'},{'Tony Fernandez': '1004002'},{'Harry Stovey': '1012586'},{'Frank Thomas': '255'},{'Heinie Groh': '1005078'},{'Rabbit Maranville': '1008099'},{'Dave Bancroft': '1000503'},{'David Wright': '3787'},{'Duke Snider': '1012230'},{'Jose Canseco': '1001918'},{'Deacon White': '1013860'},{'Hugh Duffy': '1003533'},{'Jack Clark': '1002288'},{'Carl Crawford': '1201'},{'Johnny Evers': '1003876'},{'Willie Davis': '1003088'},{'Sam Crawford': '1002748'},{'Will Clark': '1002318'},{'Jim Edmonds': '1153'},{'Tony Gwynn': '1005166'},{'Bill Dahlen': '1002924'},{'Todd Helton': '432'},{'Sherry Magee': '1007965'},{'Babe Ruth': '1011327'},{'Ellis Burks': '372'},{'Buddy Bell': '1000799'},{'Pee Wee Reese': '1010776'},{'Rogers Hornsby': '1006030'},{'Arky Vaughan': '1013377'},{'Bill Terry': '1012927'},{'Andre Dawson': '1003091'},{'George Van Haltren': '1013357'},{'Omar Vizquel': '411'},{'Ben Chapman': '1002141'},{'Hank Greenberg': '1004996'},{'Ed Konetchy': '1007093'},{'Billy Herman': '1005692'},{'Hack Wilson': '1014083'},{'Gene Tenace': '1012911'},{'Charlie Gehringer': '1004596'},{'Matt Holliday': '1873'},{'Brooks Robinson': '1011055'},{'Cesar Cedeno': '1002100'},{'Harmon Killebrew': '1006905'},{'Bert Campaneris': '1001868'},{'Frank Baker': '1000453'},{'Ted Williams': '1014040'},{'Sam Rice': '1010900'},{'Chuck Klein': '1006991'},{'Roberto Clemente': '1002340'},{'Ivan Rodriguez': '1275'},{'Mike Piazza': '893'},{'Nomar Garciaparra': '190'},{'Kirby Puckett': '1010557'},{'Jake Daubert': '1003005'},{'Earle Combs': '1002478'},{'Luis Aparicio': '1000278'},{'Dan Brouthers': '1001486'},{'Roy Thomas': '1012992'},{'Travis Jackson': '1006314'},{'Alex Rodriguez': '1274'},{'Jose Reyes': '1736'},{'Alan Trammell': '1013157'},{'Vladimir Guerrero': '778'},{'Goose Goslin': '1004893'},{'Jimmy Wynn': '1014313'},{'Hughie Jennings': '1006396'},{'Jimmy Collins': '1002455'},{'Buck Ewing': '1003881'},{'Charlie Keller': '1006768'},{'Stan Musial': '1009405'},{'Derek Jeter': '826'},{'Graig Nettles': '1009517'},{'Mark Teixeira': '1281'},{'Art Fletcher': '1004149'},{'Johnny Mize': '1009014'},{'George Davis': '1003049'},{'Dustin Pedroia': '8370'},{'Carlos Delgado': '1297'},{'Frankie Frisch': '1004364'},{'Robinson Cano': '3269'},{'Moises Alou': '261'},{'Lou Boudreau': '1001234'},{'Tony Perez': '1010188'},{'Devon White': '1013862'},{'Sam Thompson': '1013024'},{'Fred McGriff': '293'},{'Bobby Bonds': '1001157'},{'Gary Sheffield': '114'},{'Tony Phillips': '1010300'},{'Mike Griffin': '1005047'},{'Bid McPhee': '1008675'},{'Vern Stephens': '1012501'},{'Zack Wheat': '1013828'},{'Larry Gardner': '1004528'},{'Norm Cash': '1002043'},{'Kenny Lofton': '246'},{'Gil Hodges': '1005883'},{'David Ortiz': '745'},{'Robin Yount': '1014396'},{'Willie McCovey': '1008423'},{'Barry Larkin': '335'},{'Wally Berger': '1000875'},{'Dwight Evans': '1003865'},{'Mark Grace': '56'},{'Lance Berkman': '548'},{'Lou Brock': '1001458'},{'Dick Allen': '1000137'},{'Billy Hamilton': '1005270'},{'Mike Tiernan': '1013062'},{'Ichiro Suzuki': '1101'},{'Ralph Kiner': '1006923'},{'Bobby Veach': '1013388'},{'Elmer Flick': '1004158'},{'Roberto Alomar': '860'},{'Chet Lemon': '1007518'},{'Roger Connor': '1002537'},{'Cap Anson': '1000272'},{'Joey Votto': '4314'},{'Vada Pinson': '1010360'},{'Frank Chance': '1002131'},{'Reggie Jackson': '1006308'},{'Buddy Myer': '1009415'},{'Chase Utley': '1679'},{'Minnie Minoso': '1008984'},{'Lave Cross': '1002808'},{'Craig Biggio': '549'},{'Edgar Martinez': '1086'},{'Darrell Evans': '1003864'},{"Jim O'Rourke": '1009839'},{'Joe Sewell': '1011766'},{'Ernie Lombardi': '1007718'},{'Joe Tinker': '1013075'},{'Matt Williams': '77'},{'Jimmy Ryan': '1011341'},{'Jimmie Foxx': '1004285'},{'Augie Galan': '1004440'},{'Roger Peckinpaugh': '1010116'},{'Sammy Sosa': '302'},{'Manny Ramirez': '210'},{'Harry Heilmann': '1005590'},{'Brian Giles': '990'},{'Larry Doby': '1003346'},{'Jorge Posada': '841'},{'Albert Pujols': '1177'},{'Bill Freehan': '1004315'},{'George Foster': '1004250'},{'Mickey Cochrane': '1002384'},{'Joe DiMaggio': '1003311'},{'Gary Carter': '1002015'},{'Fred Tenney': '1012916'},{'Jimmy Sheckard': '1011843'},{'Fielder Jones': '1006555'},{'King Kelly': '1006806'},{'Jim Rice': '1010897'},{'Fred Clarke': '1002280'},{'Bobby Abreu': '945'},{'Rocky Colavito': '1002404'},{'Bernie Williams': '857'}]

# Names of players in the hall of fame
hof_Array = ["Harold Baines","Roy Halladay","Edgar Martinez","Mike Mussina","Mariano Rivera","Lee Smith","Vladimir Guerrero","Trevor Hoffman","Chipper Jones","Jack Morris","Jim Thome","Alan Trammell","Jeff Bagwell","Tim Raines","Ivan Rodriguez","Ken Griffey Jr.","Mike Piazza","Craig Biggio","Randy Johnson","Pedro Martinez","John Smoltz","Tom Glavine","Greg Maddux","Frank Thomas","Deacon White","Barry Larkin","Ron Santo","Roberto Alomar","Bert Blyleven","Andre Dawson","Joe Gordon","Rickey Henderson","Jim Rice","Rich Gossage","Tony Gwynn","Cal Ripken Jr.","Ray Brown","Willard Brown","Andy Cooper","Frank Grant","Pete Hill","Biz Mackey","Jose Mendez","Louis Santop","Bruce Sutter","Mule Suttles","Ben Taylor","Cristobal Torriente","Jud Wilson","Wade Boggs","Ryne Sandberg","Dennis Eckersley","Paul Molitor","Gary Carter","Eddie Murray","Ozzie Smith","Bill Mazeroski","Kirby Puckett","Hilton Smith","Dave Winfield","Carlton Fisk","Bid McPhee","Tony Perez","Turkey Stearnes","George Brett","Orlando Cepeda","Nolan Ryan","Smokey Joe Williams","Robin Yount","George Davis","Larry Doby","Bullet Rogan","Don Sutton","Nellie Fox","Phil Niekro","Willie Wells","Jim Bunning","Bill Foster","Richie Ashburn","Leon Day","Mike Schmidt","Vic Willis","Steve Carlton","Phil Rizzuto","Reggie Jackson","Rollie Fingers","Hal Newhouser","Tom Seaver","Rod Carew","Fergie Jenkins","Tony Lazzeri","Gaylord Perry","Joe Morgan","Jim Palmer","Johnny Bench","Red Schoendienst","Carl Yastrzemski","Willie Stargell","Ray Dandridge","Catfish Hunter","Billy Williams","Bobby Doerr","Ernie Lombardi","Willie McCovey","Lou Brock","Enos Slaughter","Arky Vaughan","Hoyt Wilhelm","Luis Aparicio","Don Drysdale","Rick Ferrell","Harmon Killebrew","Pee Wee Reese","George Kell","Juan Marichal","Brooks Robinson","Hank Aaron","Travis Jackson","Frank Robinson","Bob Gibson","Johnny Mize","Al Kaline","Chuck Klein","Duke Snider","Willie Mays","Hack Wilson","Addie Joss","Eddie Mathews","Ernie Banks","Martin Dihigo","Pop Lloyd","Amos Rusie","Joe Sewell","Oscar Charleston","Roger Connor","Bob Lemon","Freddie Lindstrom","Robin Roberts","Earl Averill","Billy Herman","Judy Johnson","Ralph Kiner","Cool Papa Bell","Jim Bottomley","Whitey Ford","Mickey Mantle","Sam Thompson","Roberto Clemente","Monte Irvin","High Pockets Kelly","Warren Spahn","Mickey Welch","Yogi Berra","Josh Gibson","Lefty Gomez","Sandy Koufax","Buck Leonard","Early Wynn","Ross Youngs","Dave Bancroft","Jake Beckley","Chick Hafey","Harry Hooper","Joe Kelley","Rube Marquard","Satchel Paige","Lou Boudreau","Earle Combs","Jesse Haines","Roy Campanella","Stan Coveleski","Waite Hoyt","Stan Musial","Kiki Cuyler","Goose Goslin","Joe Medwick","Red Ruffing","Lloyd Waner","Ted Williams","Pud Galvin","Luke Appling","Red Faber","Burleigh Grimes","Tim Keefe","Heinie Manush","John Ward","John Clarkson","Elmer Flick","Sam Rice","Eppa Rixey","Bob Feller","Jackie Robinson","Edd Roush","Max Carey","Billy Hamilton","Zack Wheat","Sam Crawford","Joe Cronin","Hank Greenberg","Home Run Baker","Joe DiMaggio","Gabby Hartnett","Ted Lyons","Ray Schalk","Dazzy Vance","Bill Dickey","Rabbit Maranville","Bill Terry","Chief Bender","Dizzy Dean","Al Simmons","Bobby Wallace","Harry Heilmann","Paul Waner","Jimmie Foxx","Mel Ott","Mordecai Brown","Charlie Gehringer","Kid Nichols","Herb Pennock","Pie Traynor","Mickey Cochrane","Frankie Frisch","Lefty Grove","Carl Hubbell","Jesse Burkett","Frank Chance","Jack Chesbro","Johnny Evers","Tommy McCarthy","Joe McGinnity","Eddie Plank","Joe Tinker","Rube Waddell","Ed Walsh","Roger Bresnahan","Dan Brouthers","Fred Clarke","Jimmy Collins","Ed Delahanty","Hugh Duffy","Hughie Jennings","King Kelly","Jim O'Rourke","Rogers Hornsby","Cap Anson","Eddie Collins","Buck Ewing","Lou Gehrig","Willie Keeler","Old Hoss Radbourn","George Sisler","Pete Alexander","Nap Lajoie","Tris Speaker","Cy Young","Ty Cobb","Walter Johnson","Christy Mathewson","Babe Ruth","Honus Wagner"]

def playersToExamine():
    """
    Purpose: Open csv with players info from best to worst and
    Params: none
    Return: array of arrays [ [playername, playerid] ]
    """

    playerid = []

    f = open('Fangraphs Leaderboard.csv')
    csv_f = csv.reader(f)

    # loop through csv file
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

    print(playerid)
    return playerid

def saveHTML(playerid):
    """
    Purpose: Copy the html pages of each player and save locally
    Params: list of player ids to save
    Return: none. creates html files in folder
    """
    if not os.path.exists("top_300_HTML_Files"):
        os.makedirs("top_300_HTML_Files")

    for i in range(len(playerid)):
        url = "https://www.fangraphs.com/statss.aspx?playerid=" + playerid[i][1]
        r = requests.get(url)

        with open("top_300_HTML_Files/" + playerid[i][1]+".html", "w") as html_file:
            html_file.write(r.text)

def scrapeWAR():
    """
    Purpose: Scrape the war values of each player from the local folder
    Params: none
    Return: none. writes csv file
    """

    rel_path = "top_300_HTML_Files/"
    columns = ['id','season', 'war'] # column headers
    csv_out = 'top_300_players.csv' # csv to output

    with open(csv_out, 'w') as csv_file:
    # uses dictionary writer method of csv library and
    # writes headers to file

        new_csv = csv.DictWriter(csv_file,fieldnames=columns)
        new_csv.writeheader() #write head to csv file

        # loop through all html files and use bs4 to find the table with their war stats
        for i in os.listdir('top_300_HTML_Files'):
            if i[-5:] == ".html":
                with open(rel_path + i,'r') as curr_file:
                    soup = bs(curr_file,'lxml')
                    tables = soup.find_all('table', {"id":"SeasonStats1_dgSeason11_ctl00"})
                for table in tables:
                    d = pd.read_html(table.prettify(), flavor="bs4")
                # if the table isn't empty and has a WAR value, add to csv
                if len(d):
                    if 'WAR' in d[0].columns:
                        curr_row = d[0].to_dict()
                        prev_season = 0
                        filter = ["Depth Charts","Steamer","ZiPS","THE BAT","ATC"]
                        for key in curr_row['Season'].keys():
                        # add values to current csv row and skip invalid values
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
def playerList():
    """
    Purpose: Creates csv file with additional info on baseball players from MLB API
    Params: none
    Return: none
    """

    # constants
    names = []
    base_url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&name_part='"
    columns = ['Name', 'FGL ID','MLB ID', 'Team','Position', 'IN_HOF'] # column header
    csv_out = 'top_300_additional_info_players.csv' # csv to be written
    # open leaderboard with player name list
    with open('Fangraphs Leaderboard.csv','r') as file:

        # read csv, skip header row
        csv_file = csv.reader(file)
        next(csv_file)

        # use the MLB API to search for player based on player name
        for row in csv_file:

            r = requests.get(base_url + row[0] + "'" )
            # print("On row:", r.text, "\n")
            data = json.loads(r.text)


            try:
                if data['search_player_all']['queryResults']['row'][mlbapi_keys[0]] in top_300_players:
                    names.append(data)

            except:
                continue


    with open(csv_out, 'w') as csv_file:
        new_csv = csv.DictWriter(csv_file,fieldnames=columns)
        new_csv.writeheader()

        # for each player, write the csv file row with their info
        for data in names:
            row = {}
            name = data['search_player_all']['queryResults']['row'][mlbapi_keys[0]]
            row[columns[0]] = name
            for player in top_300_players_dict:
                if name in player:
                    row[columns[1]] = player[name]
            row[columns[2]] = data['search_player_all']['queryResults']['row']["player_id"]
            row[columns[3]] = data['search_player_all']['queryResults']['row']['team_full']
            row[columns[4]] = data['search_player_all']['queryResults']['row']['position']
            if name in hof_Array:
                row[columns[5]] = True
            else:
                row[columns[5]] = False



            new_csv.writerow(row)


    # TODO:
    # - Check for duplication/disambiguation
    # - Write to csv

    # print(names[0])
def main():
    # playerid = playersToExamine()
    # saveHTML(playerid)
    # scrapeWAR()
    # playerList()
if __name__ == "__main__":
    main()
