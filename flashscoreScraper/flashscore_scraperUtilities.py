import CONSTANTS_FLASHSCORE

class Match:
    def __init__(self,id, homeTeam, awayTeam,date,time,sport,competition,importance):
        self.id = id,
        self.homeTeam =homeTeam
        self.awayTeam = awayTeam
        self.date = date
        self.time = time
        self.sport =sport
        self.competition =competition
        self.importance = importance


def merge_list(list):
    new_list = []
    for  inner_list in list:
        for item in inner_list:
            new_list.append(item)

    return new_list

def generateMatch(el,sport,competition):
    id = el.get("id")
    tempHome = el.find("div",class_="event__participant--home").text
    if(tempHome in CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS.keys()):
        homeTeam = CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[tempHome]
    else:
        homeTeam = tempHome

    tempAway = el.find("div",class_="event__participant--away").text
    if(tempAway in CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS.keys()):
        awayTeam = CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[tempAway]
    else:
        awayTeam = tempAway

    dateTime = el.find("div",class_="event__time").text
    date = dateTime.split(" ")[0]
    t = dateTime.split(" ")[1]
    importance = calculateImportance(homeTeam,awayTeam,sport,competition)
    return Match(id,homeTeam,awayTeam,date,t,CONSTANTS_FLASHSCORE.FLASCORE_SPORTS_NAMING[sport],
    CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS_NAMING[str(sport + " "+ competition)],importance)
    

def mustSaveMatch(match):
    allImportantTeamsNames = CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS.values()

    return match.homeTeam in allImportantTeamsNames  or match.awayTeam in allImportantTeamsNames

#Calculate how important this match is for us
def calculateImportance(homeTeam,awayTeam,sport,competition):
    if(homeTeam in CONSTANTS_FLASHSCORE.FLASHSCORE_NEARBY_TEAMS):
        return "very high"

    allImportantTeamsNames = CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS.values()

    if(homeTeam in allImportantTeamsNames and awayTeam in allImportantTeamsNames):
        #we have a derby
        if(sport=="football"):
            return "medium"

        if(sport=="basketball" and homeTeam=="ΟΛΥΜΠΙΑΚΟΣ" and awayTeam=="ΠΑΝΑΘΗΝΑΙΚΟΣ"):
            return "medium"
        
        return "low"

    if("europe" in competition):
        #european matches
        if(awayTeam in allImportantTeamsNames):
            return "high"
        else:
            if(sport in ["football","basketball"]):
                return "medium"
            else:
                return "low"
    
    return "low"