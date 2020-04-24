import pandas as pd
import sys

global SECRET_YEAR
global allPeople

def format_for_table(rawTable):
    formattedDF = pd.DataFrame(columns=['Player'])

    for i, row in rawTable.iterrows():
        currPlayerID = row['playerID']

        playerMetadata = allPeople[allPeople['playerID'] == currPlayerID].iloc[0]
        formattedDF = formattedDF.append({
            'Player': f'{playerMetadata["nameFirst"]} {playerMetadata["nameLast"]}'
        }, ignore_index=True)

    return formattedDF

if (len(sys.argv) != 3):
    print('ERROR! please enter a stat to query on')
    print('FORMAT:\n$ python3 award_votes.py <LG> <AWARD>')
    sys.exit(0)

SECRET_YEAR = 2015
QUERY_LG = sys.argv[1]
QUERY_AWARD= sys.argv[2]
TOP_X = 10

if (QUERY_AWARD == 'CY'):
    QUERY_AWARD = 'Cy Young'
elif (QUERY_AWARD == 'ROY'):
    QUERY_AWARD = 'Rookie of the Year'

allPeople = pd.read_csv('./core/People.csv')
allAwards = pd.read_csv('./core/AwardsSharePlayers.csv')

filterByYear = allAwards[allAwards['yearID'] == SECRET_YEAR]

LG_VOTE_GETTERS = (filterByYear[filterByYear['lgID'] == QUERY_LG]).sort_values(by=['pointsWon'], ascending=False)

LG_AWARD = LG_VOTE_GETTERS[LG_VOTE_GETTERS['awardID'] == QUERY_AWARD]

if (len(LG_AWARD.index) < TOP_X):
    TOP_X = len(LG_AWARD.index)

LG_AWARD_TOP_X = LG_AWARD[0:TOP_X]

RAW_LG_VOTE_TOP = LG_AWARD[['playerID']][0:TOP_X]

formatted_LG_VOTE_TOP = (format_for_table(RAW_LG_VOTE_TOP)).sample(TOP_X)

print('GUESS THE YEAR!')
print(f'AWARD: {QUERY_AWARD}')
print(f'{QUERY_LG} TOP {TOP_X}')
print(formatted_LG_VOTE_TOP.to_string(index=False))