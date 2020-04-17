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

if (len(sys.argv) != 2):
    print('ERROR! please enter a stat to query on')
    print('FORMAT:\n$ python3 stats_top_for_year.py HR')
    sys.exit(0)

SECRET_YEAR = 1975
QUERY_STAT = sys.argv[1]
TOP_X = 10

allPeople = pd.read_csv('./core/People.csv')
allTeams = pd.read_csv('./core/Teams.csv')
allBatting = pd.read_csv('./core/Batting.csv')

filterByYear = allBatting[allBatting['yearID'] == SECRET_YEAR]

ALL_TOP = filterByYear.sort_values(by=[QUERY_STAT], ascending=False)

AMERICAN_TOP = ALL_TOP[ALL_TOP['lgID'] == 'AL']
NATIONAL_TOP = ALL_TOP[ALL_TOP['lgID'] == 'NL']

RAW_AL_TOP_X = AMERICAN_TOP[['playerID', 'teamID', QUERY_STAT]][0:TOP_X]
RAW_NL_TOP_X = NATIONAL_TOP[['playerID', 'teamID', QUERY_STAT]][0:TOP_X]

formatted_AL_TOP_X = format_for_table(RAW_AL_TOP_X)
formatted_NL_TOP_X = format_for_table(RAW_NL_TOP_X)

print(f'STAT: {QUERY_STAT}')
print(f'AL TOP {TOP_X}')
print(formatted_AL_TOP_X)
print(f'NL TOP {TOP_X}')
print(formatted_NL_TOP_X)

