
# ------------------------------------------------------------------------------ #
#
# kWAR project
# code by Richard Conti, Fall 2018
# kWAR functions by Steve Wang, 2013
# Richard would like to thank Isaac Kleisle Murphy for significant help in the Players To Examine function
#
# v1 12/27/2018 Richard 
# v2 1/04/2019 Steve made minor revisions in main for loop and elsewhere
#
# ------------------------------------------------------------------------------ #



setwd("~/Documents/Research/Baseball/kWAR/Richard Conti Fall 2018")

#install.packages(c("dplyr", "gtools", "plyr", "rvest", "tidyr", "xml2"))
library(rvest)
library(xml2)
library(dplyr)
library(tidyr)

# First, go to
# https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2018&month=0&season1=1871&ind=0&team=0&rost=0&age=0&filter=&players=0
# click on Export Data to download data as a csv file; save it in the working directory





# -------------------------- Function definitions ------------------------------ #


Players_To_Examine<-function(file_csv, top_n){
  # file_csv is the name of the file, as a character. Be sure to include a .csv
  # top_n means take the first 50 or 100 from original FG spreadsheet
  full_df<-read.csv(file_csv)[c(1:top_n),]%>%arrange(desc(WAR))
  id_list<-as.numeric(unique(full_df$playerid))
  
  #make final dataframe
  Full_list<-as.data.frame(do.call(bind_rows, lapply(id_list, FG_WAR_Scraper)))
}


# Helpful Player ID list: http://crunchtimebaseball.com/baseball_map.html
# just give the function a player's FG ID, for example:
# >>> MikeZunino_WAR<-FG_WAR_Scraper(13265)

FG_WAR_Scraper<-function(playerID){
  
  #build FG URL
  url<-paste0("https://www.fangraphs.com/statss.aspx?playerid=",as.character(playerID))
  #download.file(url, destfile = "scrapedpage.html", quiet=TRUE)
  webpage<-read_html(url)
  
  #print(html_nodes(webpage, "table"))
  
  #table node index can change depending on: the era when someone played, position (pitcher/hitter), or your custom settings
  #thus, this program just looks through the tables until it finds one with a WAR column.
  for (node in 7:length(html_nodes(webpage, "table"))){
    df <- webpage %>%
      #extract nodes
      html_nodes(.,"table") %>%
      #select table with WAR values
      .[node]%>%
      #create tables
      html_table(fill = TRUE)%>%
      #extract from list
      .[[1]]
    
    #if we do have the war column
    if("WAR" %in% colnames(df)){
      df<-df%>%
        #get rid of minors and projections
        #add new projection systems here
        filter(!is.na(WAR),
               Team!="Depth Charts",
               Team!="Steamer",
               substr(Team,1,4)!="Fans",
               Team!="ZiPS",
               Team!="THE BAT",
               Team!="ATC")%>%
        #eliminate split seasons
        group_by(Season)%>%
        arrange(Season,Team)%>%
        filter(row_number()==1)%>%
        ungroup()%>%
        mutate(Season=ifelse(Season=="Total", 0, Season),
               Season=as.numeric(Season),
               WAR=as.numeric(as.character(WAR)))
      
      selectvec<-c(nrow(df), 1:(nrow(df)-1))
      
      df2<-df[selectvec,]%>%
        #add player's name
        mutate(player_name=playerID,
               Yr=row_number()-1)%>%
        select(player_name,Yr, WAR)%>%
        spread(.,key=Yr,value = WAR)
      
      
      return(df2)
      break
    }
  }
}


war <- function(x)  {
  return( sum(x) )
}


# return career Wins Above k for player x
wak <- function(x,k)  {
  return( sum(pmax(x-k,0)) )
}


# returns a vector of Wins Above k for a range of k values for player x
wakvec <- function(x)  {
  krange <- seq(-2,15,.5)            # range of k values
  vec <- rep(NA, length(krange))     # initialize empty vector
  for(i in 1:length(krange))
    vec[i] <- wak(x,krange[i])
  return(vec)
}




# ------------------------------ Main program ---------------------------------- #

numtopplayers <- 100   # number of players to download from FG top fWAR list

# filename below is the file downloaded from FG web site (see above)
# note: this is slow and can take a few minutes
PLfull <- Players_To_Examine("FanGraphs Leaderboard.csv", numtopplayers)
head(PLfull)
PL <- PLfull[,-c(1,2)]  # omit player ID and total WAR


# from our fangraphs file of top hitters
# cross checked w BR, one indicates HOF, zero indicates nonHOF (for 1-100)
hof <- c(1,0,1,1,1,1,1,1,1,1
         ,1,1,0,1,1,1,1,1,1,1
         ,1,1,1,1,1,1,1,0,1,1
         ,1,1,0,1,1,1,0,1,1,1
         ,1,0,1,1,1,1,1,0,1,1
         ,1,1,1,1,1,1,0,1,0,0
         ,1,1,0,1,1,1,0,1,1,0
         ,0,1,1,1,1,0,1,1,1,0
         ,1,0,1,1,0,0,0,0,0,0
         ,0,1,1,1,1,1,1,1,0,1)
hofcolor = 2
nonhofcolor = 4


# make plot of top players
plot(NULL, xlim=c(0,12), ylim=c(0,170), ylab="Wins above k WAR", xlab="k")
krange <- seq(-2,15,.5)
for (i in 1:numtopplayers)  {
  mycolor <- ifelse(hof[[i]], hofcolor, nonhofcolor)
  lines(krange, wakvec(na.omit((as.vector(unlist(PL[i,]))))), col=mycolor)
  #xsum <- rowSums(play[i,])
  #text(0,xsum, new[[i,1]], cex=0.6, pos=4, col="red")
}
abline(v=0, col="gray")


# make plot of selected players
myset <- c(50, 105, 87,177)   # FG fWAR ranks
plot(NULL, xlim=c(0,8), ylim=c(0,80), ylab="Wins above k WAR", xlab="k")
krange <- seq(-2,15,.5)
j <- 1
for (i in myset)  {
  lines(krange, wakvec(na.omit((as.vector(unlist(PL[i,]))))), col=j)
  j <- j + 1
}
abline(v=0, col="gray")


save.image("workspace.Rdata")

