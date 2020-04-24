import pandas as pd
import sys

global SECRET_YEAR
global GAMES_TAG
global QUERY_POS
global QUERY_LG
global allPeople
global allTeams

def sort_players_by_games_started(fielders_list):
    return sorted(fielders_list, key=lambda player: player[GAMES_TAG], reverse=True)


def format_for_table(raw_table):
    formattedDF = pd.DataFrame(columns=['Player', 'Team', 'POS', 'PLATOON'])

    for i, row in raw_table.iterrows():
        currPlayerID = row['playerID']
        currTeamID = row['teamID']

        playerMetadata = allPeople[allPeople['playerID'] == currPlayerID].iloc[0]
        teamMetadata = allTeams[(allTeams['teamID'] == currTeamID)]
        teamNameForYear = teamMetadata[(teamMetadata['yearID']) == SECRET_YEAR].iloc[0]['name']
        formattedDF = formattedDF.append({
            'Player': f'{playerMetadata["nameFirst"]} {playerMetadata["nameLast"]}',
            'Team': teamNameForYear,
            'POS': row['POS'],
            'PLATOON': row['PLATOON']
        }, ignore_index=True)

    return formattedDF

if (len(sys.argv) != 3):
    print('ERROR! please enter a stat to query on')
    print('FORMAT:\n$ python3 starters_for_year.py <LG> <POS>')
    sys.exit(0)

SECRET_YEAR = 2012
GAMES_TAG = 'GS'
QUERY_LG = sys.argv[1]
QUERY_POS = sys.argv[2]

allPeople = pd.read_csv('./core/People.csv')
allTeams = pd.read_csv('./core/Teams.csv')
allFielding = pd.read_csv('./core/Fielding.csv')

if (QUERY_POS in ['LF', 'RF', 'CF']):
    allFielding = pd.read_csv('./core/FieldingOFsplit.csv')

fieldingMap = {}

filterByYear = allFielding[allFielding['yearID'] == SECRET_YEAR]
filterByLeague = filterByYear[filterByYear['lgID'] == QUERY_LG]
filterByPosition = filterByLeague[filterByLeague['POS'] == QUERY_POS]

if (SECRET_YEAR < 1954):
    GAMES_TAG = 'G'

for i, row in filterByPosition.iterrows():

    if row['teamID'] not in fieldingMap:
        fieldingMap[row['teamID']] = []

    fieldingMap[row['teamID']].append(row[['playerID', GAMES_TAG]])


raw_starters = pd.DataFrame(columns=['playerID', 'teamID', 'POS', 'PLATOON'])

for team in fieldingMap:
    players_sorted_by_gs = sort_players_by_games_started(fieldingMap[team])
    defaultStarter = players_sorted_by_gs[0]
    platoon_bool = ''
    if int(defaultStarter[GAMES_TAG]) < 90:
        platoon_bool = '(PLATOON)'
    raw_starters = raw_starters.append({
        'playerID': defaultStarter['playerID'],
        'teamID': team,
        'POS': QUERY_POS,
        'PLATOON': platoon_bool
    }, ignore_index=True)
    # Add platoon as well
    if (platoon_bool != '') and (QUERY_POS != 'P'):
        backupStarter = players_sorted_by_gs[1]
        raw_starters = raw_starters.append({
            'playerID': backupStarter['playerID'],
            'teamID': team,
            'POS': QUERY_POS,
            'PLATOON': platoon_bool
        }, ignore_index=True)

formatted_starters = format_for_table(raw_starters)

print('GUESS THE YEAR!')
print(f'LEAGUE: {QUERY_LG}')
print(formatted_starters)