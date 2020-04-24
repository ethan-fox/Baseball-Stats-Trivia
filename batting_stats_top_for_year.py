import pandas as pd
import sys

global SECRET_YEAR
global QUERY_STAT
global allPeople
global allTeams

def format_for_table(rawTable):
    formattedDF = pd.DataFrame(columns=['Player', 'Team', QUERY_STAT])

    for i, row in rawTable.iterrows():
        currPlayerID = row['playerID']
        currTeamID = row['teamID']

        playerMetadata = allPeople[allPeople['playerID'] == currPlayerID].iloc[0]
        teamMetadata = allTeams[(allTeams['teamID'] == currTeamID)]
        teamNameForYear = teamMetadata[(teamMetadata['yearID']) == SECRET_YEAR].iloc[0]['name']
        formattedDF = formattedDF.append({
            'Player': f'{playerMetadata["nameFirst"]} {playerMetadata["nameLast"]}',
            'Team': teamNameForYear,
            QUERY_STAT: row[QUERY_STAT]
        }, ignore_index=True)

    return formattedDF

if (len(sys.argv) != 3):
    print('ERROR! please enter a stat to query on')
    print('FORMAT:\n$ python3 batting_stats_top_for_year.py <LG> <STAT>')
    sys.exit(0)

SECRET_YEAR = 1983
QUERY_STAT = sys.argv[2]
QUERY_LG = sys.argv[1]
TOP_X = 10

allPeople = pd.read_csv('./core/People.csv')
allTeams = pd.read_csv('./core/Teams.csv')
allBatting = pd.read_csv('./core/Batting.csv')

filterByYear = allBatting[allBatting['yearID'] == SECRET_YEAR]

ALL_TOP = filterByYear.sort_values(by=[QUERY_STAT], ascending=False)

LG_TOP = ALL_TOP[ALL_TOP['lgID'] == QUERY_LG]

RAW_LG_TOP_X = LG_TOP[['playerID', 'teamID', QUERY_STAT]][0:TOP_X]

formatted_LG_TOP_X = format_for_table(RAW_LG_TOP_X)

print('GUESS THE YEAR!')
print(f'STAT: {QUERY_STAT}')
print(f'{QUERY_LG} TOP {TOP_X}')
print(formatted_LG_TOP_X)


