import numpy as np
import math

import pandas as pd


class Elo:
    def __init__(self, games_list, schedule):
        self.games_list = games_list
        self.med_margin = np.median(
            [abs(int(game[1]) - int(game[3])) for game in self.games_list if game[1].isdigit()]
        )
        self.schedule = schedule

    def _distinct_teams(self):
        gl = self.games_list
        teams = []
        for game in gl:
            teams = teams + [game[0], game[2]]
        return list(set(teams))

    def _initial_dict(self):
        teams = self._distinct_teams()
        teams_dict = dict()
        for team in teams:
            teams_dict[team] = dict()
            teams_dict[team]['wins'] = 0
            teams_dict[team]['losses'] = 0
            teams_dict[team]['elo'] = 1000
        self.elo_dict = teams_dict
        return teams_dict

    def _elo_change(self, winner, loser, margin):
        teams_dict = self.elo_dict
        total_games = 0

        for team in [winner, loser]:
            for result in ['wins', 'losses']:
                total_games = total_games + teams_dict[team][result]
        temp_k = (60/ math.log(total_games + 2)) / math.log(self.med_margin + 1)
        win_elo = teams_dict[winner]['elo']
        loser_elo = teams_dict[loser]['elo']
        elo_diff = win_elo - loser_elo
        prior_win_prob = 1/(10**(-elo_diff/400) + 1)
        mov_multiple = math.log(margin + 1) * 2.2/(elo_diff*0.001+2.2)
        elo_change = prior_win_prob*temp_k*mov_multiple
        teams_dict[winner]['elo'] = win_elo + elo_change
        teams_dict[loser]['elo'] = loser_elo - elo_change
        teams_dict[winner]['wins'] += 1
        teams_dict[loser]['losses'] += 1

    def elo_from_list(self, as_dataframe=True):
        self._initial_dict()
        gl = self.games_list
        for game in gl:
            if game[1] == "W":
                self._elo_change(winner=game[0], loser=game[2], margin=self.med_margin)
            elif game[1] == "L":
                self._elo_change(winner=game[2], loser=game[0], margin=self.med_margin)
            elif int(game[1]) > int(game[3]):
                self._elo_change(winner=game[0], loser=game[2], margin=int(game[1]) - int(game[3]))
            elif int(game[3]) > int(game[1]):
                self._elo_change(winner=game[2], loser=game[0], margin=int(game[3]) - int(game[1]))
            print(self.med_margin)

        if as_dataframe:
            df = pd.DataFrame(self.elo_dict).transpose().astype(int).reset_index()
            df.columns = ['Team Name', 'Wins', "Losses", "Rating"]
            return df

        else:
            return self.elo_dict

    def predictions(self):
        elo_dict = self.elo_from_list(as_dataframe=False)
        predictions = []
        for i in range(int(len(self.schedule) / 2)):
            list_index = i * 2
            team_1 = self.schedule[list_index]
            team_2 = self.schedule[list_index + 1]
            team_1_elo = elo_dict[team_1]['elo']
            team_2_elo = elo_dict[team_2]['elo']
            elo_diff = team_1_elo - team_2_elo
            team_1_prob = 1 / (10 ** (-elo_diff / 400) + 1)
            predictions.append([team_1, team_2, team_1_prob])

        return predictions
