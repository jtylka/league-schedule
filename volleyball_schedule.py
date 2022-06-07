# league randomizer
# Joe Tylka, 2022

import random

teams_list = ["Siemens","Abbott","Munich RE","ThermoFisher","Croda"]

def _gen_game_list(teams_list):
    game_list = []
    num_teams = len(teams_list)
    for i in range(num_teams):
        for j in range(i+1,num_teams):
            game_match = [teams_list[i],teams_list[j]]
            random.shuffle(game_match)
            game_list.append(game_match)
    return game_list

def _make_pairs(game_list,teams_list):
    game_pairs = []
    max_skips = len(teams_list) - 4 # two games per day, no doubles, so 4 teams play each day
    skip_counter = dict.fromkeys(teams_list, 0)
    ii = 1
    jj = 0
    while len(game_list) > 0 and jj < len(teams_list)**2:
        jj += 1
        game1 = game_list[0]
        print(f'Day {ii} game 1 = {game1}')

        # first, make sure no team has to play twice on the same day
        possible_games = [game2 for game2 in game_list if game1[0] not in game2 and game1[1] not in game2]
        print(f'Found possible games = {possible_games}')

        # only allow games which won't exceed max skips
        valid_games = []
        for game2 in possible_games:
            missing_teams = _find_missing(teams_list,[*game1,*game2])
            if all(skip_counter[team] < max_skips for team in missing_teams):
                valid_games.append(game2)
        print(f'Found valid games = {valid_games}')

        # now remove the games from the list, update the skip counters, and proceed
        if len(valid_games) > 0:
            random.shuffle(valid_games)
            game2 = valid_games[0]
            print(f'Day {ii} game 2 = {game2}')
            game_pairs.append([game1,game2])

            # then, track which teams get a by-week
            missing_teams = _find_missing(teams_list,[*game1,*game2])
            for team in missing_teams:
                skip_counter[team] += 1
            
            game_list.remove(game1)
            game_list.remove(game2)
            ii += 1
        else:
            random.shuffle(game_list)
        print(f'Current skip counter = {skip_counter}')
    return game_pairs

def _find_missing(listA,listB):
    return [item for item in listA if item not in listB]

if __name__ == "__main__":
    random.shuffle(teams_list)
    game_list = _gen_game_list(teams_list)
    random.shuffle(game_list)
    game_pairs = _make_pairs(game_list,teams_list)
    random.shuffle(game_pairs)
    print(*game_pairs, sep='\n')